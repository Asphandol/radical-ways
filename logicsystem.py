"""
logic system for our customers
"""
import pymongo
import random

class LogicSystem:
    """
    a logic system class
    """
    __not_finished_orders = []

    def delete_person(self, data: dict):
        """
        delets person from app
        """
        self.get_database.delete_one(data)
        return "Account has been successfully deleted"

    def change_info(self):
        """
        changes info about person
        """
        pass

    @property
    def get_database(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Radical_ways"]
        return db["accounts"]

    @property
    def trips_database(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Radical_ways"]
        return db["trips"]

    def log_in(self, data: dict):
        """
        logging in a person
        """
        if data["mail"] in self.get_database.find_one():
            raise TypeError("There is no account with such mail")
        if data["mail"] != self.get_database.find_one()[data["password"]]:
            raise TypeError("There is no account with such mail")
        data = {"mail": "shtohryn.pn@ucu.edu.ua", "password": "nadvirna4ever"}
        result = self.get_database.find_one(data)
        return "Welcome back, " + result['name'].capitalize()

    def sign_up(self, data: dict):
        """
        helps a new person to sign up
        """
        # data = {"mail": "melnyk.pn@ucu.edu.ua", "password": "watch__us", "is_driver": False}
        self.get_database.insert_one(data)
        return data["name"] + ", Thank you for joining us"

    def sign_out(self):
        """
        helps tp sign out person
        """
        pass

    def make_order(self):
        """
        makes an order 
        """
        pass

    def show_map(self):
        """
        shows a map
        """
        pass

class Person:
    """
    a person class
    """
    def __init__(self, name: str, surname: str, email_adress: str, password: str) -> None:

        self.name = name
        self.surname = surname
        self.email_adress = email_adress
        self.password = password
        self.is_registred = True

class User(Person):
    """
    user class
    """

    def __init__(self, name: str, surname: str, email_adress: str, password: str) -> None:

        super().__init__(name, surname, email_adress, password)
        self.is_driver = False

    def make_request(self):
        """
        makes request
        """
        pass

class Driver(Person):
    """
    driver class
    """

    def __init__(self, name: str, surname: str,
                email_adress: str, password: str,
                car: str, license_num: int) -> None:

        super().__init__(name, surname, email_adress, password)

        self.is_driver = True
        self.car = car
        self.license_num = license_num
        self.is_able = True

    def respond(self):
        """
        makes a respond on users rquest
        """
        pass

    def finish_order(self):
        """
        finish users order
        """
        pass

    def accept(self):
        """
        accept users request        
        """
        pass

    def reject(self):
        """
        reject users request
        """
        pass

    def end_session(self):
        """
        ends session with user
        """
        pass

class Order:
    """
    creates an users order
    """
    def __init__(self) -> None:
        self.is_finised = False
        self.__id = random.randint(1, 999999)
        self.__route = None

class Map:
    """
    map class which
    can help with
    paving the way
    """

    def __init__(self, start: str, other_places: list) -> None:
        self.start = start
        self.other_places = other_places

    def create_way(self):
        """
        creates the best way beetween multiple places
        """
        pass

    def display_map(self):
        """
        helps with displaying map
        """
        pass
