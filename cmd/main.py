from runtime.simulation import Simulation
from runtime.passengers_generator import PassengersGenerator

from models.routes.route import Route
from models.routes.route_stage_station import RouteStageStation
from models.routes.route_stage_segment import RouteStageSegment

from models.stations import Station
from models.segments import Segment
from models.trains import create_train_from_dict
from models.stations.dto import StationConfig
from models.segments.dto import SegmentConfig
from utils import ID


# ---------- Stations ----------
s1 = Station(StationConfig(ID(1), "Одинцово", 500))
s2 = Station(StationConfig(ID(2), "Баковка", 300))
s3 = Station(StationConfig(ID(3), "Сколково", 400))
s4 = Station(StationConfig(ID(4), "Немчиновка", 200))


# ---------- Segments ----------
seg1 = Segment(SegmentConfig(
    station_from=s1,
    station_to=s2,
    distance=3.5,
    max_speed=50.0
))

seg2 = Segment(SegmentConfig(
    station_from=s2,
    station_to=s3,
    distance=2.2,
    max_speed=90.0
))

seg3 = Segment(SegmentConfig(
    station_from=s3,
    station_to=s4,
    distance=4.0,
    max_speed=90.0
))


# ---------- Trains ----------
train1 = create_train_from_dict({
    "type": "passenger",
    "model_name": "Тест-п-1",
    "wagon_count": 3,
    "wagon_capacity": 100,
    "max_speed": 80
})

train2 = create_train_from_dict({
    "type": "passenger",
    "model_name": "Тест-п-2",
    "wagon_count": 3,
    "wagon_capacity": 100,
    "max_speed": 120
})


# ---------- Routes ----------
route1 = Route([
    RouteStageStation(s1, stop_time=10),
    RouteStageSegment(seg1),
    RouteStageStation(s2, stop_time=20),
    RouteStageSegment(seg2),
    RouteStageStation(s3, stop_time=30),
    RouteStageSegment(seg3),
    RouteStageStation(s4, stop_time=10),
])

route2 = Route([
    RouteStageStation(s2, stop_time=20),
    RouteStageSegment(seg2),
    RouteStageStation(s3, stop_time=30),
    RouteStageSegment(seg3),
    RouteStageStation(s4, stop_time=10),
])


# ---------- Simulation ----------
sim = Simulation(render_interval=1)

# пассажиропотоки (чел / сек)
sim.add_station(s1, PassengersGenerator(base_rate=0.4, variation=0.2))
sim.add_station(s2, PassengersGenerator(base_rate=0.6, variation=0.3))
sim.add_station(s3, PassengersGenerator(base_rate=0.3, variation=0.2))
sim.add_station(s4, PassengersGenerator(base_rate=0.2, variation=0.1))

# маршруты
# sim.add_route(route1, train1)
sim.add_route(route2, train2)

# старт
sim.run(sim_seconds_per_real_second=60*60)