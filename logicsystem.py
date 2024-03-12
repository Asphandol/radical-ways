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

app.secret_key = 'mega_secret_key'

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

        # if logic_sys.log_in({'mail': email, 'password': password}):
        #     flash('There are no such data')
        #     return render_template('O_log-in.html')

        return redirect(url_for('choose_way'))

    return render_template('O_log-in.html')

@app.route('/sign_up', methods = ['POST', 'GET'])
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

        if not val.validate_name(name):
            flash('You failed name(fisrt symb- upper)')
            return render_template('O_sign-up.html')

        if not val.validate_surname(surname):
            flash('You failed surname(fisrt sym- upper)')
            return render_template('O_sign-up.html')

        if not val.validate_email(email):
            flash('You failed email(example: aaa@uuu.com)')
            return render_template('O_sign-up.html')

        if not val.validate_password(password):
            flash('You failed password(starts with numb or letter)')
            return render_template('O_sign-up.html')

        dct = {'name': name, 'surnme': surname, 'email':email,
            'password': password}

        if car and licensee:
            dct['car'] = car
            dct['license'] = licensee

        logic_sys.sign_up(dct)
        return redirect(url_for('choose_way'))

    return render_template('O_sign-up.html')

@app.route('/choose_way', methods = ['POST', 'GET'])
def choose_way():
    """
    delets person from app
    """

    city_list = []

    if request.method == 'POST':
        startt = request.form['start']
        end = request.form['end']
        waypoint = request.form['waypoint'] if 'waypoint' in request.form else []

        mapa = Map(startt, end, waypoint)
        city_list = mapa.take_map_data()

        return render_template('M_user.html', city_list = city_list)

    return render_template('M_user.html',city_list = [])

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

    def __init__(self, startt: str, end: str, other_places: list) -> None:
        self.startt = startt
        self.other_places = other_places if other_places else []
        self.end = end

    def take_map_data(self):
        """
        creates the best way beetween multiple places
        """
        lst_places = [self.startt, self.end] + self.other_places

        # dct_dist = self.make_dist(lst_places)
        # way = self.greedy_shortest_path(self.startt, self.end, dct_dist, lst_places)
        # directions_result = gmaps.directions(way[0], \
        # way[-1], waypoints = way[1:-1], mode = "driving")

        # return way
        return lst_places

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
