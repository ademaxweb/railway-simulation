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
from runtime.train_generator import TrainsSchedule, TrainScheduleEntry, ScheduleTime
from utils import ID, Pos

from server.server import Server, InitialData

# ---------- Stations ----------
s1 = Station(StationConfig(ID(1), "Одинцово", 800, Pos(0, 0)))
s2 = Station(StationConfig(ID(2), "Баковка", 500, Pos(2.36, 0)))
s3 = Station(StationConfig(ID(3), "Сколково", 1000, Pos(4.99, 0)))
s3_1 = Station(StationConfig(ID(), "Test", 1000, Pos(4.55, 1.4)))
s4 = Station(StationConfig(ID(4), "Немчиновка", 400, Pos(7.73, 0)))
s5 = Station(StationConfig(ID(5), "Сетунь", 500, Pos(9.3, 0)))
s6 = Station(StationConfig(ID(6), "Рабочий посёлок", 200, Pos(10.73, 0)))
s7 = Station(StationConfig(ID(7), "Кунцевская", 200, Pos(12.71, 0)))
s8 = Station(StationConfig(ID(8), "Славянский бульвар", 200, Pos(14.19, 0)))
s9 = Station(StationConfig(ID(9), "Фили", 200, Pos(17.43, 0)))
s10 = Station(StationConfig(ID(10), "Тестовская", 200, Pos(19.33, 0)))
s11 = Station(StationConfig(ID(11), "Беговая", 200, Pos(21.02, 0)))
s12 = Station(StationConfig(ID(12), "Белорусский вокзал", 200, Pos(23.68, 0)))



# ---------- Segments ----------
seg1 = Segment(SegmentConfig(
    station_from=s1,
    station_to=s2,
    distance=2.36,
    max_speed=40.46
))

seg2_1 = Segment(SegmentConfig(
    station_from=s2,
    station_to=s3_1,
    distance=2.6,
    max_speed=90
))

# к Сколково
seg2 = Segment(SegmentConfig(
    station_from=s2,
    station_to=s3,
    distance=2.63,
    max_speed=63.12
))

# k Nemchninovke
seg3 = Segment(SegmentConfig(
    station_from=s3,
    station_to=s4,
    distance=2.74,
    max_speed=46.97
))

# k Setuni
seg4 = Segment(SegmentConfig(
    station_from=s4,
    station_to=s5,
    distance=1.57,
    max_speed=62.8
))

# k Rabochemu
seg5 = Segment(SegmentConfig(
    station_from=s5,
    station_to=s6,
    distance=1.43,
    max_speed=34.32
))

# Рабочий посёлок -> Кунцевская: 2 км (tutu)
seg6 = Segment(SegmentConfig(
    station_from=s6,
    station_to=s7,
    distance=1.98,
    max_speed=47.52
))

# Кунцевская -> Славянский бульвар: ~1.4 км (по разнице "до Москвы")
seg7 = Segment(SegmentConfig(
    station_from=s7,
    station_to=s8,
    distance=1.48,
    max_speed=35.52
))

seg8 = Segment(SegmentConfig(
    station_from=s8,
    station_to=s9,
    distance=3.24,
    max_speed=43.2
))

# Фили -> Тестовская: 2 км (tutu)
seg9 = Segment(SegmentConfig(
    station_from=s9,
    station_to=s10,
    distance=1.9,
    max_speed=45.6
))

# Тестовская -> Беговая: ~2 км (по разнице "до Москвы")
seg10 = Segment(SegmentConfig(
    station_from=s10,
    station_to=s11,
    distance=1.69,
    max_speed=28.97
))

# Беговая -> Белорусский вокзал: ~2 км (по разнице "до Москвы")
seg11 = Segment(SegmentConfig(
    station_from=s11,
    station_to=s12,
    distance=2.66,
    max_speed=31.92
))
# ---------- Trains ----------
aero = train_config_from_dict({
    "model_name": "Aэроэкспресс",
    "type": "passenger",
    "max_speed": 160,
    "wagon_count": 6,
    "wagon_capacity": 180
})

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

route1 = Route([
    RouteStageStation(s1, stop_time=60),
    RouteStageSegment(seg1),
    RouteStageStation(s2, stop_time=25),
    RouteStageSegment(seg2_1),
    RouteStageStation(s3_1, stop_time=30)
])

# ---------- Simulation ----------
sim = Simulation(render_interval=1 / 30, start_time=5 * 60 * 60)
em: EventManager = sim.get_event_manager()

# ---------- Server (parallel) ----------
initial_data = InitialData(
    stations=[s1, s2, s3, s3_1, s4, s5, s6, s7, s8, s9, s10, s11, s12],
    segments=[seg1, seg2, seg2_1, seg3, seg4, seg5, seg6, seg7, seg8, seg9, seg10, seg11],
)
server = Server(initial_data, em)
server_thread = threading.Thread(target=server.run, name="server-thread", daemon=True)
server_thread.start()

# пассажиропотоки (чел / сек)
sim.add_station(s1, PassengersGenerator(base_rate=0.28, variation=0.4, rush_multiplier=5), unload_max=0.0) # Одинцово
sim.add_station(s2, PassengersGenerator(base_rate=0.15, variation=0.4, rush_multiplier=3), unload_max=0.02) # Баковка
sim.add_station(s3, PassengersGenerator(base_rate=0.267, variation=0.4, rush_multiplier=5), unload_max=0.05) # Сколково
sim.add_station(s3_1, PassengersGenerator(base_rate=0.06, variation=0.4, rush_multiplier=1.5), unload_min=0.87, unload_max=1) # test
sim.add_station(s4, PassengersGenerator(base_rate=0.1, variation=0.4, rush_multiplier=3), unload_max=0.01) # Немчиновка
sim.add_station(s5, PassengersGenerator(base_rate=0.17, variation=0.4, rush_multiplier=3), unload_min=0.02, unload_max=0.1) # Сетунь
sim.add_station(s6, PassengersGenerator(base_rate=0.19, variation=0.4, rush_multiplier=2), unload_min=0.03, unload_max=0.1) # Рабочий Поселок
sim.add_station(s7, PassengersGenerator(base_rate=0.1, variation=0.4, rush_multiplier=1.1), unload_min=0.4, unload_max=0.6) # Кунцевская
sim.add_station(s8, PassengersGenerator(base_rate=0.1, variation=0.4, rush_multiplier=1.2), unload_min=0.4, unload_max=0.8) # Славянский Бульвар
sim.add_station(s9, PassengersGenerator(base_rate=0.1, variation=0.4, rush_multiplier=1.1), unload_min=0.1, unload_max=0.2) # Фили
sim.add_station(s10, PassengersGenerator(base_rate=0.05, variation=0.4, rush_multiplier=1), unload_min=0.1, unload_max=0.3) # Тестовская
sim.add_station(s11, PassengersGenerator(base_rate=0.05, variation=0.4, rush_multiplier=1), unload_min=0.3, unload_max=0.6) #Беговая
sim.add_station(s12, PassengersGenerator(base_rate=0.1, variation=0.4, rush_multiplier=1.3), unload_min=0.7, unload_max=0.9) #Белорусский

# маршруты
# sim.add_train_generator(route, [ivolga, ed4m], 300)
sim.add_train_scheduled_generator(TrainsSchedule(
    [
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=4, minute=56)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=5, minute=1)),
        TrainScheduleEntry(route=route1, train_config=ed4m, departure_time=ScheduleTime(hour=5, minute=4)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=5, minute=11)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=5, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=5, minute=31)),
        TrainScheduleEntry(route=route1, train_config=ed4m, departure_time=ScheduleTime(hour=5, minute=35)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=5, minute=37)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=5, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=5, minute=46)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=5, minute=56)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=6, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=6, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=6, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=6, minute=17)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=6, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=6, minute=31)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=6, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=6, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=6, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=7, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=7, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=7, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=7, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=7, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=7, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=7, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=7, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=7, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=7, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=8, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=8, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=8, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=8, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=8, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=8, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=8, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=8, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=8, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=8, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=9, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=9, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=9, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=9, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=9, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=9, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=9, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=9, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=9, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=9, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=10, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=10, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=10, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=10, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=10, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=10, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=10, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=10, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=10, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=10, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=11, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=11, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=11, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=11, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=11, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=11, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=11, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=11, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=11, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=11, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=12, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=12, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=12, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=12, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=12, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=12, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=12, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=12, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=12, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=12, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=13, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=13, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=13, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=13, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=13, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=13, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=13, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=13, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=13, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=13, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=14, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=14, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=14, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=14, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=14, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=14, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=14, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=14, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=14, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=14, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=15, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=15, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=15, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=15, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=15, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=15, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=15, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=15, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=15, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=15, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=16, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=16, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=16, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=16, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=16, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=16, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=16, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=16, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=16, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=16, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=17, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=17, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=17, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=17, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=17, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=17, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=17, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=17, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=17, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=17, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=18, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=18, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=18, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=18, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=18, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=18, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=18, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=18, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=18, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=18, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=19, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=19, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=19, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=19, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=19, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=19, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=19, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=19, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=19, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=19, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=20, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=20, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=20, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=20, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=20, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=20, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=20, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=20, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=20, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=20, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=21, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=21, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=21, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=21, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=21, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=21, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=21, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=21, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=21, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=21, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=22, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=22, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=22, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=22, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=22, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=22, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=22, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=22, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=22, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=22, minute=56)),
        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=23, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=23, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=23, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=23, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=23, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=23, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=23, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=23, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=23, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=23, minute=56)),

        # Next hour
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=0, minute=1)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=0, minute=7)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=0, minute=11)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=0, minute=16)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=0, minute=22)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=0, minute=26)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=0, minute=36)),
        TrainScheduleEntry(route=route, train_config=ivolga, departure_time=ScheduleTime(hour=0, minute=41)),
        TrainScheduleEntry(route=route, train_config=ed4m, departure_time=ScheduleTime(hour=0, minute=47)),
        TrainScheduleEntry(route=route, train_config=aero, departure_time=ScheduleTime(hour=0, minute=56)),

    ]
))
# старт
sim.run(sim_seconds_per_real_second=20, render=False)
