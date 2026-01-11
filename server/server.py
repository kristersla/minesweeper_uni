import asyncio
import json
import random
import string
import time
from dataclasses import dataclass, field
from typing import Dict, Optional

import websockets


def generate_code(length=5):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


@dataclass
class Player:
    id: str
    name: str
    status: str = "alive"
    time: Optional[int] = None
    flags: int = 0
    websocket: Optional[websockets.WebSocketServerProtocol] = None


@dataclass
class Room:
    code: str
    host_id: str
    players: Dict[str, Player] = field(default_factory=dict)
    settings: dict = field(default_factory=lambda: {"rows": 10, "cols": 10, "probability": 0.15, "width": 720})
    seed: Optional[int] = None
    start_time: Optional[float] = None

    def lobby_payload(self):
        return {
            "code": self.code,
            "host_id": self.host_id,
            "players": [
                {"id": player.id, "name": player.name, "status": player.status, "flags": player.flags}
                for player in self.players.values()
            ],
            "settings": self.settings,
        }


rooms: Dict[str, Room] = {}


async def broadcast(room: Room, message_type: str, payload: dict):
    message = json.dumps({"type": message_type, "payload": payload})
    await asyncio.gather(
        *[
            player.websocket.send(message)
            for player in room.players.values()
            if player.websocket is not None
        ]
    )


async def handle_message(websocket, message):
    data = json.loads(message)
    message_type = data.get("type")
    payload = data.get("payload", {})

    if message_type == "create_room":
        player_id = payload.get("player_id") or generate_code(8)
        name = payload.get("name", "Player")
        code = generate_code()
        room = Room(code=code, host_id=player_id)
        player = Player(id=player_id, name=name, websocket=websocket)
        room.players[player_id] = player
        rooms[code] = room
        await websocket.send(
            json.dumps({"type": "room_created", "payload": {"player_id": player_id, **room.lobby_payload()}})
        )
        return room, player_id

    if message_type == "join_room":
        code = payload.get("code")
        name = payload.get("name", "Player")
        if code not in rooms:
            await websocket.send(json.dumps({"type": "error", "payload": {"message": "Room not found"}}))
            return None, None
        room = rooms[code]
        player_id = payload.get("player_id") or generate_code(8)
        player = Player(id=player_id, name=name, websocket=websocket)
        room.players[player_id] = player
        await websocket.send(
            json.dumps({"type": "room_joined", "payload": {"player_id": player_id, **room.lobby_payload()}})
        )
        await broadcast(room, "lobby_update", room.lobby_payload())
        return room, player_id

    if message_type == "update_settings":
        code = payload.get("code")
        player_id = payload.get("player_id")
        room = rooms.get(code)
        if not room or room.host_id != player_id:
            return None, None
        room.settings.update(payload.get("settings", {}))
        await broadcast(room, "lobby_update", room.lobby_payload())
        return room, player_id

    if message_type == "start_game":
        code = payload.get("code")
        player_id = payload.get("player_id")
        room = rooms.get(code)
        if not room or room.host_id != player_id:
            return None, None
        for player in room.players.values():
            player.status = "alive"
            player.time = None
            player.flags = 0
        room.seed = random.randint(0, 99999999)
        room.start_time = time.time()
        await broadcast(
            room,
            "game_started",
            {
                "seed": room.seed,
                "settings": room.settings,
                "start_time": room.start_time,
                "players": room.lobby_payload()["players"],
            },
        )
        return room, player_id

    if message_type == "flag_update":
        code = payload.get("code")
        player_id = payload.get("player_id")
        room = rooms.get(code)
        if not room or player_id not in room.players:
            return None, None
        room.players[player_id].flags = int(payload.get("flags", 0))
        await broadcast(room, "game_update", {"players": room.lobby_payload()["players"]})
        return room, player_id

    if message_type == "player_status":
        code = payload.get("code")
        player_id = payload.get("player_id")
        room = rooms.get(code)
        if not room or player_id not in room.players:
            return None, None
        player = room.players[player_id]
        player.status = payload.get("status", player.status)
        player.time = payload.get("time", player.time)
        await broadcast(room, "game_update", {"players": room.lobby_payload()["players"]})
        if all(p.status in ("dead", "finished") for p in room.players.values()):
            players = list(room.players.values())
            has_finished = any(p.status == "finished" for p in players)
            tie = False
            if has_finished:
                leaderboard = sorted(
                    players,
                    key=lambda p: (
                        0 if p.status == "finished" else 1,
                        p.time if p.time is not None else 999999,
                    ),
                )
                ranked_by = "time"
            else:
                leaderboard = sorted(
                    players,
                    key=lambda p: (-p.flags, p.time if p.time is not None else 999999),
                )
                ranked_by = "flags"
                tie = (
                    len(
                        {
                            (p.flags, p.time if p.time is not None else 999999)
                            for p in players
                        }
                    )
                    == 1
                )
            await broadcast(
                room,
                "game_finished",
                {
                    "ranked_by": ranked_by,
                    "tie": tie,
                    "leaderboard": [
                        {
                            "name": p.name,
                            "status": p.status,
                            "time": p.time,
                            "flags": p.flags,
                        }
                        for p in leaderboard
                    ],
                },
            )
        return room, player_id

    return None, None


async def handler(websocket):
    room = None
    player_id = None
    async for message in websocket:
        room, player_id = await handle_message(websocket, message)


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())