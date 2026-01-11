import asyncio
import json
import queue
import threading

import websockets


class NetworkClient:
    def __init__(self, url):
        self.url = url
        self._incoming = queue.Queue()
        self._outgoing = queue.Queue()
        self._connected = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def send(self, message_type, payload=None):
        self._outgoing.put(
            json.dumps({"type": message_type, "payload": payload or {}})
        )

    def get_messages(self):
        messages = []
        while True:
            try:
                messages.append(self._incoming.get_nowait())
            except queue.Empty:
                break
        return messages

    def _run(self):
        asyncio.run(self._main())

    async def _main(self):
        async with websockets.connect(self.url) as websocket:
            self._connected.set()
            receiver = asyncio.create_task(self._receiver(websocket))
            sender = asyncio.create_task(self._sender(websocket))
            await asyncio.wait([receiver, sender], return_when=asyncio.FIRST_COMPLETED)

    async def _receiver(self, websocket):
        async for message in websocket:
            self._incoming.put(json.loads(message))

    async def _sender(self, websocket):
        loop = asyncio.get_event_loop()
        while True:
            message = await loop.run_in_executor(None, self._outgoing.get)
            await websocket.send(message)