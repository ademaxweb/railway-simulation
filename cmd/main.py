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
from utils import ID


# ---------- Stations ----------
s1 = Station(StationConfig(ID(1), "Одинцово", 800))
s2 = Station(StationConfig(ID(2), "Баковка", 500))
s3 = Station(StationConfig(ID(3), "Сколково", 1000))
s4 = Station(StationConfig(ID(4), "Немчиновка", 400))
s5 = Station(StationConfig(ID(5), "Сетунь", 500))
s6 = Station(StationConfig(ID(6), "Рабочий поселок", 200))
s7 = Station(StationConfig(ID(7), "Кунцевская", 200))
s8 = Station(StationConfig(ID(8), "Славянский бульвар", 200))
s9 = Station(StationConfig(ID(9), "Фили", 200))
s10 = Station(StationConfig(ID(10), "Тестовская", 200))
s11 = Station(StationConfig(ID(11), "Беговая", 200))
s12 = Station(StationConfig(ID(12), "Белорусский вокзал", 200))


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
])

# ---------- Simulation ----------
sim = Simulation(render_interval=1, start_time=6.6 * 60 * 60)

# пассажиропотоки (чел / сек)
sim.add_station(s1, PassengersGenerator(base_rate=0.6, variation=0.9, rush_multiplier=5))
sim.add_station(s2, PassengersGenerator(base_rate=0.2, variation=0.2))
sim.add_station(s3, PassengersGenerator(base_rate=0.6, variation=0.7, rush_multiplier=5))
sim.add_station(s4, PassengersGenerator(base_rate=0.2, variation=0.5))
sim.add_station(s5, PassengersGenerator(base_rate=0.4, variation=0.5))

# маршруты
sim.add_train_generator(route, [ivolga, ed4m], 240)


# старт
sim.run(sim_seconds_per_real_second=60, render=True)