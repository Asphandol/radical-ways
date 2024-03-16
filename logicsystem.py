"""
logic system for our customers
"""
import pymongo
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
import googlemaps
import requests
from PIL import Image
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
        client = pymongo.MongoClient("mongodb+srv://melnykpn:Mascara_2006@radicalways.gbpcvjs.mongodb.net/?retryWrites=true&w=majority&appName=Radicalways")
        db = client["Radical_ways"]
        return db["accounts"]

    @property
    def trips_database(self):
        """
        gives an trips database
        """
        client = pymongo.MongoClient("mongodb+srv://Oleg:Oleg@radicalways.gbpcvjs.mongodb.net/?retryWrites=true&w=majority&appName=Radicalways")
        db = client["Radical_ways"]
        return db["trips"]

    def log_in(self, data: dict):
        """
        logging in a person
        """
        return self.get_database.find_one(data)

    def sign_up(self, data: dict):
        """
        helps a new person to sign up
        """
        self.get_database.insert_one(data)

    def add_order(self, waypooints_lst: list):
        """
        adds order in database
        """
        self.trips_database.insert_one(waypooints_lst)

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

        if not (email and password):
            flash('No input data')
            return render_template('O_log-in.html')

        if not bool(logic_sys.log_in({'email': email, 'password': password})):
            flash('There are no such data')
            return render_template('O_log-in.html')

        # session['my_id'] = logic_sys.log_in({'email': email, 'password': password})['_id']
        session['password'] = password
        session['email'] = email

        if 'car' in logic_sys.log_in({'email': email, 'password': password}):

            return redirect(url_for('orders'))

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

        if logic_sys.get_database.find_one({"email" : email}):
            flash('This data already in database')
            return render_template('O_sign-up.html')

        dct = {'name': name, 'surnme': surname, 'email':email,
            'password': password}

        if car and licensee:
            dct['car'] = car
            dct['license'] = licensee

        logic_sys.sign_up(dct)
        # session['my_id'] = logic_sys.log_in({'email': email, 'password': password})['_id']
        session['password'] = password
        session['email'] = email

        if 'car' in dct:
            return redirect(url_for('orders'))
        return redirect(url_for('choose_way'))

    return render_template('O_sign-up.html' )

@app.route('/choose_way', methods = ['POST', 'GET'])
def choose_way():
    """
    delets person from app
    """

    city_list = []

    if request.method == 'POST':
        action = request.form['action']
        startt = request.form['start']
        end = request.form['end']
        waypoint = request.form['allWaypoints'].split(', ') if 'waypoint' in request.form else []

        mapa = Map(startt, end, waypoint)
        city_list = mapa.take_map_data()
        dct_info = {'email': session['email'], 'waypoints_list': city_list, 'in_proccess': False}

        if action == 'button1':
            return render_template('M_user.html', city_list = city_list)

        if action == 'button2':
            logic_sys.add_order(dct_info)
            session['order'] = dct_info
            return redirect(url_for('waiting_driver'))

    return render_template('M_user.html',city_list = [])

@app.route('/driver_waiting', methods = ['POST', 'GET'])
def waiting_driver():
    """
    renders template with until driver do notaccept your request
    """

    action = request.form['action']

    if request.method == 'POST':

        if action == 'button1':
            logic_sys.trips_database.delete_one(session['order'])
            return redirect(url_for('choose_way'))

        if action == 'button2':
            if logic_sys.trips_database.find_one(session['order'])['in_proccess'] is True:
                return redirect(url_for('your_driver'))

            flash('No driver took your order')
            return render_template('V_searching.html')

    return render_template('V_searching.html')

@app.route('/your_driver', methods = ['POST', 'GET'])
def your_driver():
    """
    renders your driver page
    """
    lst_ways = []
    if request.form == 'POST':
        info = session['order']
        mapa = Map(info['start'], info['end'], info['allWaypoints'])
        lst_ways = mapa.take_map_data()
        return render_template('Y_your_driver.html', lst_ways = lst_ways)

    return render_template('Y_your_driver.html', lst_ways = lst_ways)

@app.route('/profile')
def profile():
    """
    profile for our user
    """
    return render_template('V_profile.html')

@app.route('/delete_acccount', methods = ['POST', 'GET'])
def delete():
    '''
    deletes an account
    '''
    if request.method == 'POST':
        password = request.form['password']
        if session['password'] == password:
            logic_sys.get_database.delete_one({'password': password})
            session['password'] = None
            return redirect(url_for('start'))
        else:
            flash('Wrong password')
            return render_template('V_delete_account.html')

    return render_template('V_delete_account.html')

@app.route('/main')
def main():
    '''
    main page
    '''
    return render_template('O_main.html')

@app.route('/get_help')
def get_help():
    '''
    gets help
    '''
    if request.method == 'POST':
        return redirect(url_for('profile'))
    return render_template('V_get_help.html')

@app.route('/change_info')
def change_info(person, change_data):
    """
    changes info about person
    """
    logic_sys.get_database.update_one(person, {"$set": change_data})
    return render_template('V_change_info.html')

@app.route('/driver_page', methods=['POST', 'GET'])
def orders():
    """
    shows all orders for drivers
    """
    order_list = []

    all_orders = list(logic_sys.trips_database.find({}))

    for i in all_orders:
        if len(order_list) != 3 and i['in_proccess'] is False:
            order_list.append(i)
        elif len(order_list) == 3:
            break

    if request.method == 'POST':
        session['order_id'] = request.form.get('orderId')
        logic_sys.trips_database.delete_one(session['order_id'])
        session['order_id']['in_proccess'] = True
        logic_sys.add_order(session['order_id'])
        return redirect(url_for('in_way_proccess'))

    return render_template('M_driver.html', order_list = order_list)

@app.route('/in_way', methods=['POST', 'GET'])
def in_way_proccess():
    """
    represents driver in a way
    """

    lst_ways = []

    if request.method == 'POST':

        action = request.form['action']

        if action == 'button1':
            logic_sys.trips_database.delete_one(session['order_id'])
            return redirect(url_for('orders'))

        if action == 'button2':
            logic_sys.trips_database.delete_one(session['order_id'])
            session['order_id']['in_proccess'] = False
            logic_sys.add_order(session['order_id'])
            return redirect(url_for('orders'))

        if action == 'button3':
            lst_ways = [session['order_id']['start'], session['order_id']['end']]\
             + session['order_id']['waypoints']
            return render_template('O_main.html', lst_ways = lst_ways)

    return render_template('O_main.html', lst_ways = lst_ways)

@app.errorhandler(404)
def page_not_found():
    """
    page is not found erroe
    """
    return render_template('V_not_found.html')

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
