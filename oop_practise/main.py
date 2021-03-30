"""
# Создать класс User со следующими атрибутами:
# имя, фамилия, почтовый адрес, мобильный номер, пароль, животные
# Создать геттер и сеттер для пароля.
# Создайте класс Pet и добавьте к нему следующие атрибуты:
# кличка, порода, год рождения, хозяин (User)
# Добавьте список из Pet как атрибут экземпляра для User.
# Создайте несколько экземпляров класса User, добавьте к юзерам 1-4 домашних
животных
"""
from getpass import getpass
from faker import Faker
from string import ascii_letters, digits, punctuation
from random import choice
import requests
from bs4 import BeautifulSoup
import re

fake = Faker(['ru_RU'])


class FakePets:
    url_pets_names = "https://www.petplace.com/article/dogs/pet-care/top-1200-pet-names/"
    url_pets_kinds = "https://www.listsforall.com/best-house-pets/"

    def __init__(self):
        self.html_dom = None
        self.pets_names = None
        self.pets_kinds = None

    def get_html(self, html):
        r = requests.get(html)
        if r.status_code == 200:
            return r.text

    def get_pets_names(self):
        html = self.get_html(self.url_pets_names)
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', class_='single-post-content')
        li_s = content.find_all('li')
        pets_names = [pet.text.strip() for pet in li_s]
        uniq_pets_names = lambda x: list(set(x))
        self.pets_names = uniq_pets_names(pets_names)

    def get_pets_kinds(self):
        pattern = r"\s\(link\)"  # Siamese Fighting Fish (link)
        html = self.get_html(self.url_pets_kinds)
        soup = BeautifulSoup(html, 'lxml')
        h3_s = soup.find_all('h3', text=re.compile(pattern))
        filter_pet_kind = lambda x: re.sub(pattern, "", x)
        self.pets_kinds = [filter_pet_kind(pet_kind.text.strip()) for pet_kind in h3_s]

    def __call__(self, *args, **kwargs):
        self.get_pets_names()
        self.get_pets_kinds()


class Worker:

    @staticmethod
    def fake_password(length=8):
        sources = [ascii_letters, digits, punctuation]
        random_symbol = lambda _: choice(choice(sources))
        return "".join([random_symbol(i) for i in range(length + 1)])

    @staticmethod
    def create_master():
        user_data = {'name': fake.first_name(),
                     'last_name': fake.last_name(),
                     'zip_code': fake.postcode(),
                     # 'password': Worker.fake_password(),
                     'cell': fake.phone_number()
                     }

        master = User(**user_data)

        return master

    @staticmethod
    def create_pet(names, kinds, master):
        """name, kind, birthday, master"""
        pet_data = {'name': choice(names),
                    'kind': choice(kinds),
                    'birthday': fake.date_this_century().strftime('%Y-%m-%d'),
                    'master': master,
                    }

        pet = Pet(**pet_data)

        return pet


class PetNotBelongToMaster(Exception):
    pass


class User:
    def __init__(self, name, last_name, zip_code, cell):
        self.name = name
        self.last_name = last_name
        self.zip_code = zip_code
        self.cell = cell
        # self.password = password
        self._password = None
        self.pets = []

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @classmethod
    def set_password(cls):
        password = getpass('Fill your password: ')
        return password

    def add_pet(self, pet_instance):
        if isinstance(pet_instance, Pet):
            self.pets.append(pet_instance)
        else:
            raise PetNotBelongToMaster

    def __len__(self):
        return len(self.pets)

    def __getitem__(self, item):
        return self.pets[item]

    def __repr__(self):
        return f"<{self.name} {self.last_name}>"


class Pet:
    def __init__(self, name, kind, birthday, master):
        self.name = name
        self.kind = kind
        self.birthday = birthday
        self.master = master if isinstance(master, User) else False

    def __str__(self):
        return f"{self.master}'s Pet {self.kind}>: <{self.name}>"

    def __repr__(self):
        return f'{self.name}'


if __name__ == '__main__':
    masters, pets = [], []

    # Human input
    andrew = User('Andrew', 'Horbach', '20026', '+375298670592')
    andrew.password = andrew.set_password()

    masters.append(andrew)

    tiri = Pet('Tiri', 'Dinosaur', '2021-02-14', andrew)

    andrew.add_pet(tiri)
    # End of Human input

    # create masters
    for _ in range(4):
        master_instance = Worker.create_master()
        master_instance.password = Worker.fake_password()
        masters.append(Worker.create_master())

    # create pets
    fake_pet = FakePets()
    fake_pet()
    fake_names = fake_pet.pets_names
    fake_kinds = fake_pet.pets_kinds

    # add pets to each master
    for master in masters:

        while len(master) < 4:
            pet = Worker.create_pet(fake_names, fake_kinds, master)
            master.add_pet(pet)

        for pet in master.pets:
            print(pet)
