import asyncio
import json
import threading
import queue
from contextlib import suppress
from typing import Optional, Set, TYPE_CHECKING, Any, List

from models.events.simulation_data_event import SimulationDataUpdate
from models.segments import Segment
from models.stations import Station
from runtime.event_manager import EventManager

from websockets.asyncio.server import serve
from websockets.asyncio.server import ServerConnection as WSConn

class InitialData:
    def __init__(self, stations: List[Station], segments: List[Segment]):
        self._stations = stations
        self._segments = segments

    @property
    def stations(self):
        return self._stations

    @property
    def segments(self):
        return self._segments

    def to_dict(self) -> dict:
        def station_to_dict(station: Station) -> dict:
            return {
                "id": station.id,
                "name": station.name,
                "position": station.pos.to_dict()
            }

        def segment_to_dict(segment: Segment) -> dict:
            return {
                "id": segment.id,
                "from": segment.station_from.id,
                "to": segment.station_to.id,
            }

        return {
            "stations": list(map(lambda x: station_to_dict(x), self.stations)),
            "segments": list(map(lambda x: segment_to_dict(x), self.segments))
        }

class Server:
    """
    WebSocket worker:
    - accepts WS connections
    - broadcasts SimulationDataUpdate to all connections as JSON:
      json.dumps(event.sim_data.to_list(), ensure_ascii=False)
    """

    def __init__(self, d: InitialData, event_manager: EventManager, host: str = "0.0.0.0", port: int = 8765):
        self._initial_data = d
        self._event_manager = event_manager
        self._host = host
        self._port = port

        self._clients: Set[WSConn] = set()
        self._outgoing: "queue.Queue[object]" = queue.Queue()

        self._stop_event = threading.Event()
        self._loop: Optional[asyncio.AbstractEventLoop] = None

        self._event_manager.subscribe(SimulationDataUpdate, self._on_data_update)

    def _on_data_update(self, event: SimulationDataUpdate):
        # handler already exists: enqueue payload for broadcaster
        self._outgoing.put(event.sim_data.to_dict())

    async def _ws_handler(self, websocket: WSConn):
        self._clients.add(websocket)

        payload = {"type": "initial", "payload": self._initial_data.to_dict()}
        try:
            message = json.dumps(payload, ensure_ascii=False)
        except TypeError:
            message = json.dumps(payload, ensure_ascii=False, default=str)

        await websocket.send(message)

        try:
            # keep connection alive; incoming messages are ignored
            async for _ in websocket:
                pass
        finally:
            self._clients.discard(websocket)

    async def _broadcast_json(self, payload: object):
        if not self._clients:
            return

        try:
            message = json.dumps(payload, ensure_ascii=False)
        except TypeError:
            message = json.dumps(payload, ensure_ascii=False, default=str)

        dead = []
        for ws in list(self._clients):
            try:
                await ws.send(message)
            except Exception:
                dead.append(ws)

        for ws in dead:
            self._clients.discard(ws)

    async def _broadcaster(self):
        while not self._stop_event.is_set():
            payload = await asyncio.to_thread(self._outgoing.get)
            if payload is None:
                continue
            payload = {"type": "update", "payload": payload}
            await self._broadcast_json(payload)

    async def _shutdown(self):
        close_tasks = []
        for ws in list(self._clients):
            close_tasks.append(ws.close(code=1001, reason="Server stopping"))
        if close_tasks:
            with suppress(Exception):
                await asyncio.gather(*close_tasks, return_exceptions=True)
        self._clients.clear()

    async def _main(self):
        async with serve(
            self._ws_handler,
            self._host,
            self._port,
            ping_interval=20,
            ping_timeout=20,
            close_timeout=5,
        ):
            broadcaster_task = asyncio.create_task(self._broadcaster())

            await asyncio.to_thread(self._stop_event.wait)

            broadcaster_task.cancel()
            with suppress(asyncio.CancelledError):
                await broadcaster_task

            await self._shutdown()

    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._main())
        finally:
            with suppress(Exception):
                self._loop.close()

    def stop(self):
        self._stop_event.set()
        self._outgoing.put(None)
