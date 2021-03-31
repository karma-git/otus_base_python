"""
создайте класс `Car`, наследник `Vehicle`
"""
from base import Vehicle
from engine import Engine


class Car(Vehicle):
    def __init__(self, weight, fuel, fuel_consumption):
        super().__init__(weight, fuel, fuel_consumption)
        self.engine = None

    def set_engine(self, engine):
        if isinstance(engine, Engine):
            self.engine = engine
# w, f, fc = 0, 1, 2
# # e = Engine(1, 2)
# c = Car(w, f, fc)
# # c.set_engine(e)
# #
# # print(c.weight == w, c.fuel == f, c.fuel_consumption == fc, sep=2*'\n')
# print(isinstance(c, Vehicle))


