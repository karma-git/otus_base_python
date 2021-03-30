"""
Домашнее задание
Классы и модули

Цель:
В этом ДЗ вы напишите базовый класс и сделаете наследников, которые будут реализовывать различные методы

скопируйте папку homework_02 для этой домашки (Памятка: https://github.com/OtusTeam/BasePython/tree/homeworks)
в модуле exceptions объявите следующие исключения:
LowFuelError
NotEnoughFuel
CargoOverload
доработайте базовый класс base.Vehicle:
добавьте атрибуты weight, started, fuel, fuel_consumption со значениями по умолчанию
добавьте инициализатор для установки weight, fuel, fuel_consumption
добавьте метод start, который, если ещё не состояние started, проверяет, что топлива больше нуля, и обновляет состояние started, иначе выкидывает исключение exceptions.LowFuelError
добавьте метод move, который проверяет, что достаточно топлива для преодоления переданной дистанции, и изменяет количество оставшегося топлива, иначе выкидывает исключение exceptions.NotEnoughFuel
создайте датакласс Engine в модуле engine, добавьте атрибуты volume и pistons
в модуле car создайте класс Car
класс Car должен быть наследником Vehicle
добавьте атрибут engine классу Car
объявите метод set_engine, который принимает в себя экземпляр объекта Engine и устанавливает на текущий экземпляр Car
в модуле plane создайте класс Plane
класс Plane должен быть наследником Vehicle
добавьте атрибуты cargo и max_cargo классу Plane
добавьте max_cargo в инициализатор (переопределите родительский)
объявите метод load_cargo, который принимает число, проверяет, что в сумме с текущим cargo не будет перегруза, и обновляет значение, в ином случае выкидывает исключение exceptions.CargoOverload
объявите метод remove_all_cargo, который принимает число, обнуляет значение cargo и возвращает значение cargo, которое было до обнуления
Критерии оценки:
автоматический тест test_homework_02 проходит
Рекомендуем сдать до: 22.04.2021
"""
from abc import ABC
import exceptions

 
class Vehicle(ABC):

    def __init__(self, weight=0, fuel=100, fuel_consumption=10):
        self.weight = weight
        self.started = False
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if not self.started:
            if self.fuel > 0:
                self.started = True
            else:
                raise exceptions.LowFuelError

    def move(self, distance):
        consumption = distance * self.fuel_consumption
        if self.fuel_consumption > consumption:
            self.fuel -= consumption
        else:
            raise exceptions.NotEnoughFuel



