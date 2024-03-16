"""
logic system for our customers
"""
import pymongo
from flask import Flask, render_template, request, flash, redirect, url_for
import googlemaps
import requests
from validator import Validator

app = Flask(__name__)

API_KEY = "AIzaSyAZLOb5jlcg6kuiu7ovzBg6yAdjwkcqfAA"
gmaps = googlemaps.Client(key=API_KEY)

app.config['SECRET_KEY'] = 'dghskdhfsljhglyufluckjg'

class LogicSystem:
    """
    a logic system class
    """

    @property
    def get_database(self):
        """
        gives an account database
        """
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Radical_ways"]
        return db["accounts"]

    @property
    def trips_database(self):
        """
        gives an trips database
        """
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Radical_ways"]
        return db["trips"]

    def log_in(self, data: dict):
        """
        logging in a person
        """
        if data["mail"] in self.get_database.find_one():
            return True
        if data["mail"] != self.get_database.find_one()[data["password"]]:
            return True
        # data = {"mail": "shtohryn.pn@ucu.edu.ua", "password": "nadvirna4ever"}
        # result = self.get_database.find_one(data)
        # return "Welcome back, " + result['name'].capitalize()
        return False

    def sign_up(self, data: dict):
        """
        helps a new person to sign up
        """
        # data = {"mail": "melnyk.pn@ucu.edu.ua", "password": "watch__us", "is_driver": False}
        self.get_database.insert_one(data)
        return data["name"] + ", Thank you for joining us"

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

logic_sys = LogicSystem()

@app.route('/')
def start():
    """
    starting page
    """
    return render_template('O_start-page.html')

@app.route('/log_in', methods = ['POST', 'GET'])
def logg_in():
    """
    creates an account
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if logic_sys.log_in({'mail': email, 'password': password}):
            flash('wrong data')

    return render_template('O_log-in.html')

@app.route('/delete_acccount')
def delete():
    '''
    deletes an account
    '''
    return render_template('V_delete_account.html')

@app.route('/main')
def main():
    '''
    main page
    '''
    return render_template('O_main.html')

@app.route('/change_info')
def change():
    '''
    changes info
    '''
    return render_template('V_change_info.html')

@app.route('/get_help')
def get_help():
    '''
    gets help
    '''
    return render_template('V_get_help.html')

@app.route('/sign_in', methods = ['POST', 'GET'])
def create_account():
    """
    creates an account
    """

    if request.method == 'POST':

        val = Validator()

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        car = request.form['car']
        licensee = request.form['license']

        if not (val.validate_name(name) and val.validate_surname(surname) and\
        val.validate_email(email) and val.validate_password(password)):
            flash('You failed registration requirement')

        dct = {'name': name, 'surnme': surname, 'email':email,
            'password': password}

        if car and licensee:
            dct['car'] = car
            dct['license'] = licensee

        logic_sys.sign_up(dct)
        return redirect(url_for('choose_way'))

    return render_template('O_sign-in.html')

@app.route('/choose_way')
def choose_way():
    """
    delets person from app
    """
    return render_template('M_user.html')

@app.route('/delete')
def delete_person(data: dict):
    """
    delets person from app
    """
    logic_sys.get_database.delete_one(data)
    return render_template('regestartion.html')

@app.route('/change_info')
def change_info(person, change_data):
    """
    changes info about person
    """
    logic_sys.get_database.update_one(person, {"$set": change_data})

@app.route('/driver_page')
def orders():
    """
    shows all orders for drivers
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

    @app.route('/')
    def take_map_data(self):
        """
        creates the best way beetween multiple places
        """
        if request.method == 'POST':

            start = request.form['start']
            finish = request.form['finish']
            addintional_points = request.form['addintional_points'].split(',')
            lst_places = [start, finish] + addintional_points

            dct_dist = self.make_dist(lst_places)
            way = self.greedy_shortest_path(start, finish, dct_dist, lst_places)
            directions_result = gmaps.directions(way[0], \
            way[-1], waypoints = way[1:-1], mode = "driving")

            return render_template('user_page.html', api_key=API_KEY, directions=directions_result)

    def make_dist(self, lst_places: list):
        """
        makes distances
        """
        base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'

        distances = {}

        for city1 in lst_places:
            distances[city1] = {}
            for city2 in lst_places:
                if city1 != city2:
                    params = {
                        'origins': city1,
                        'destinations': city2,
                        'key': API_KEY
                    }

                    response = requests.get(base_url, params=params)
                    data = response.json()

                    if data['rows'][0]['elements'][0]['status'] == 'OK':
                        distance = data['rows'][0]['elements'][0]['distance']['value']
                        distances[city1][city2] = distance

        return distances

    @staticmethod
    def greedy_shortest_path(graph, start, end, all_points):
        """
        makes a shortest path
        """
        if len(all_points) ==2:
            return [start, end]
        unvisited = set(all_points)
        path = [start]
        current = start
        unvisited.remove(start)

        while unvisited:
            next_node = None
            min_distance = float('inf')

            for neighbor, distance in graph[current].items():
                if neighbor in unvisited and distance < min_distance:
                    next_node = neighbor
                    min_distance = distance

            if next_node is None:
                return None

            path.append(next_node)
            unvisited.remove(next_node)
            current = next_node

        if end not in path:
            return None

        return path

if __name__ == '__main__':
    app.run(debug=True)
