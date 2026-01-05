import threading

from runtime.event_manager import EventManager
from runtime.simulation import Simulation
from runtime.passengers_generator import PassengersGenerator

from models.routes.route import Route
from models.routes.route_stage_station import RouteStageStation
from models.routes.route_stage_segment import RouteStageSegment

from models.stations import Station
from models.segments import Segment
from models.trains import train_config_from_dict, create_train
from models.stations.dto import StationConfig
from models.segments.dto import SegmentConfig
from utils import ID, Pos

from server.server import Server, InitialData

# ---------- Stations ----------
s1 = Station(StationConfig(ID(1), "Одинцово", 800, Pos(0, 0)))
s2 = Station(StationConfig(ID(2), "Баковка", 500, Pos(2.36, 0)))
s3 = Station(StationConfig(ID(3), "Сколково", 1000, Pos(4.99, 0)))
s4 = Station(StationConfig(ID(4), "Немчиновка", 400, Pos(7.73, 0)))
s5 = Station(StationConfig(ID(5), "Сетунь", 500, Pos(9.3, 0)))
s6 = Station(StationConfig(ID(6), "Рабочий посёлок", 200, Pos(10.30, 0)))
s7 = Station(StationConfig(ID(7), "Кунцевская", 200, Pos(12.30, 0)))
s8 = Station(StationConfig(ID(8), "Славянский бульвар", 200, Pos(13.70, 0)))
s9 = Station(StationConfig(ID(9), "Фили", 200, Pos(16.30, 0)))
s10 = Station(StationConfig(ID(10), "Тестовская (Москва-Сити)", 200, Pos(18.30, 0)))
s11 = Station(StationConfig(ID(11), "Беговая", 200, Pos(20.30, 0)))
s12 = Station(StationConfig(ID(12), "Белорусский вокзал", 200, Pos(22.30, 0)))



# ---------- Segments ----------
seg1 = Segment(SegmentConfig(
    station_from=s1,
    station_to=s2,
    distance=2.36,
    max_speed=70.0
))

seg2 = Segment(SegmentConfig(
    station_from=s2,
    station_to=s3,
    distance=2.63,
    max_speed=90.0
))

seg3 = Segment(SegmentConfig(
    station_from=s3,
    station_to=s4,
    distance=2.74,
    max_speed=110.0
))

seg4 = Segment(SegmentConfig(
    station_from=s4,
    station_to=s5,
    distance=1.57,
    max_speed=110.0
))

seg5 = Segment(SegmentConfig(
    station_from=s5,
    station_to=s6,
    distance=1.00,
    max_speed=110.0
))

# Рабочий посёлок -> Кунцевская: 2 км (tutu)
seg6 = Segment(SegmentConfig(
    station_from=s6,
    station_to=s7,
    distance=2.00,
    max_speed=110.0
))

# Кунцевская -> Славянский бульвар: ~1.4 км (по разнице "до Москвы")
seg7 = Segment(SegmentConfig(
    station_from=s7,
    station_to=s8,
    distance=1.40,
    max_speed=110.0
))

seg8 = Segment(SegmentConfig(
    station_from=s8,
    station_to=s9,
    distance=2.60,
    max_speed=110.0
))

# Фили -> Тестовская: 2 км (tutu)
seg9 = Segment(SegmentConfig(
    station_from=s9,
    station_to=s10,
    distance=2.00,
    max_speed=110.0
))

# Тестовская -> Беговая: ~2 км (по разнице "до Москвы")
seg10 = Segment(SegmentConfig(
    station_from=s10,
    station_to=s11,
    distance=2.00,
    max_speed=110.0
))

# Беговая -> Белорусский вокзал: ~2 км (по разнице "до Москвы")
seg11 = Segment(SegmentConfig(
    station_from=s11,
    station_to=s12,
    distance=2.00,
    max_speed=110.0
))
# ---------- Trains ----------
ivolga = train_config_from_dict({
    "model_name": "Иволга",
    "type": "passenger",
    "max_speed": 160,
    "wagon_count": 11,
    "wagon_capacity": 240
})

ed4m = train_config_from_dict({
    "model_name": "ЭД4М",
    "type": "passenger",
    "max_speed": 90,
    "wagon_count": 12,
    "wagon_capacity": 120
})


# ---------- Routes ----------
route = Route([
    RouteStageStation(s1, stop_time=60),
    RouteStageSegment(seg1),
    RouteStageStation(s2, stop_time=25),
    RouteStageSegment(seg2),
    RouteStageStation(s3, stop_time=45),
    RouteStageSegment(seg3),
    RouteStageStation(s4, stop_time=25),
    RouteStageSegment(seg4),
    RouteStageStation(s5, stop_time=25),
    RouteStageSegment(seg5),
    RouteStageStation(s6, stop_time=25),
    RouteStageSegment(seg6),
    RouteStageStation(s7, stop_time=25),
    RouteStageSegment(seg7),
    RouteStageStation(s8, stop_time=25),
    RouteStageSegment(seg8),
    RouteStageStation(s9, stop_time=25),
    RouteStageSegment(seg9),
    RouteStageStation(s10, stop_time=25),
    RouteStageSegment(seg10),
    RouteStageStation(s11, stop_time=25),
    RouteStageSegment(seg11),
    RouteStageStation(s12, stop_time=60),
])

# ---------- Simulation ----------
sim = Simulation(render_interval=1, start_time=6.6 * 60 * 60)
em: EventManager = sim.get_event_manager()

# ---------- Server (parallel) ----------
initial_data = InitialData(
    stations=[s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12],
    segments=[seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11],
)
server = Server(initial_data, em)
server_thread = threading.Thread(target=server.run, name="server-thread", daemon=True)
server_thread.start()

# пассажиропотоки (чел / сек)
sim.add_station(s1, PassengersGenerator(base_rate=0.6, variation=0.9, rush_multiplier=5))
sim.add_station(s2, PassengersGenerator(base_rate=0.2, variation=0.2))
sim.add_station(s3, PassengersGenerator(base_rate=0.6, variation=0.7, rush_multiplier=5))
sim.add_station(s4, PassengersGenerator(base_rate=0.2, variation=0.5))
sim.add_station(s6, PassengersGenerator(base_rate=0.4, variation=0.5))
sim.add_station(s7, PassengersGenerator(base_rate=0.4, variation=0.5))
sim.add_station(s8, PassengersGenerator(base_rate=0.4, variation=0.5))
sim.add_station(s9, PassengersGenerator(base_rate=0.4, variation=0.5))
sim.add_station(s10, PassengersGenerator(base_rate=0.4, variation=0.5))
sim.add_station(s11, PassengersGenerator(base_rate=0.4, variation=0.5))
sim.add_station(s12, PassengersGenerator(base_rate=0.4, variation=0.5))

# маршруты
sim.add_train_generator(route, [ivolga, ed4m], 240)

# старт
sim.run(sim_seconds_per_real_second=5, render=False)
