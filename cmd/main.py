import repositories
import models

train_repo = repositories.trains.FileTrainRepository("config/train_types")
station_repo = repositories.stations.FileStationRepository("config/stations")
segment_repo = repositories.segments.FileSegmentRepository("config/segments")

trains = train_repo.get_all()
stations = station_repo.get_all()
segments = segment_repo.get_all()