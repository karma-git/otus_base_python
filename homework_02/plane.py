from base import Vehicle
from exceptions import CargoOverload


class Plane(Vehicle):

    def __init__(self, weight, fuel, fuel_consumption, cargo, max_cargo):
        super.__init__(weight, fuel, fuel_consumption)
        self.cargo = cargo
        self.max_cargo = max_cargo

    def load_cargo(self, add_weight):
        if self.cargo + add_weight < self.max_cargo:
            self.cargo += add_weight
        else:
            raise CargoOverload

    def remove_all_cargo(self):
        throw_cargo = self.cargo
        self.cargo = 0
        return throw_cargo

