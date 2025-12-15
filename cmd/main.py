import repositories
import time
from utils import ID

train_repo = repositories.trains.FileTrainRepository("config/train_types")
station_repo = repositories.stations.FileStationRepository("config/stations")
segment_repo = repositories.segments.FileSegmentRepository("config/segments", station_repo)


for seg in segment_repo.get_to_station(station_repo.get_by_id(ID(1004))):
    print(seg)


t = train_repo.get_all()[0]

ticks = 120
while ticks > 0:
    print(f"\r{t.string(True)}", end="", flush=True)
    t.add_person(200)
    time.sleep(1)
    ticks -= 1