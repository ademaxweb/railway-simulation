from utils import Window

w = Window(4)

for i in range(1, 10):
    w.push(i)
    print(w)
