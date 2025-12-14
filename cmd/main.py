import repositories

train_repo = repositories.trains.FileTrainRepository("config/train_types")
station_repo = repositories.stations.FileStationRepository("config/stations")

trains = train_repo.get_all()
stations = station_repo.get_all()

for s in stations:
    print(s)

for t in trains:
    print(t)