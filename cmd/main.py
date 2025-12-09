import models

t = models.trains.PassengerTrain(1, 150)

print(t)

t.set_velocity(120.0)

print(t)