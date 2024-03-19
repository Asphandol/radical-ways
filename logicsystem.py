"""
logic system for our customers
"""
import pymongo
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import googlemaps
import requests
from bson import ObjectId
from PIL import Image
import time
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

val = Validator()

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

        if not email and not password:
            flash('No input data')
            return render_template('O_log-in.html')

        if not email:
            flash('You need to input email')
            return render_template('O_log-in.html')

        if not password:
            flash('You need to input password')
            return render_template('O_log-in.html')

        if not bool(logic_sys.log_in({'email': email, 'password': password})):
            flash('There are no such data')
            return render_template('O_log-in.html')

        session['my_id'] = str(logic_sys.log_in({'email': email, 'password': password})['_id'])

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

        dct = {'name': name, 'surname': surname, 'email':email,
            'password': password}

        if car and licensee:
            dct['car'] = car
            dct['license'] = licensee

        logic_sys.sign_up(dct)
        session['my_id'] = str(logic_sys.log_in({'email': email, 'password': password})['_id'])

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

        if len(request.form['waypoints']) != 1:
                waypoints = request.form['waypoints'].split(', ')
                waypoints.remove(end)
                waypoints.remove(startt)
        else:
            waypoints = []

        try:
            if not waypoints:
                    mapa = Map(startt, end, waypoints)
                    city_list = mapa.take_map_data()
            else:
                city_list = [startt, end]
        except:
            city_list = None
            flash('not enough data')
            return render_template('M_user.html', city_list = city_list)

        try:
            if action == 'button1':
                return render_template('M_user.html', city_list = city_list)

        except:
            city_list = None
            flash('not enough data')
            return render_template('M_user.html', city_list = city_list)

        dct_info = {
                    'user_id': ObjectId(session['my_id']),
                    'waypoints_list': city_list,
                    'status': 'created',
                    'driver': None
                    }

        if action == 'button2':
            logic_sys.trips_database.insert_one(dct_info)
            trip_id = logic_sys.trips_database.find_one(dct_info)
            while True:
                time.sleep(2)
                try:
                    logic_sys.trips_database.find_one(trip_id)['status']
                except TypeError:
                    return redirect(url_for('your_driver'))

    return render_template('M_user.html',city_list = [])

@app.route('/your_driver', methods = ['POST', 'GET'])
def your_driver():
    """
    renders your driver page
    """
    city_list = []
    if request.form == 'POST':
        city_list = logic_sys.trips_database.find_one(
            {'user_id': ObjectId(session['my_id'])}
            )['waypoints_list']

        return render_template('Y_your_driver.html', city_list = city_list)

    return render_template('Y_your_driver.html', city_list = city_list)

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    """
    profile for our user
    """
    if request.method == 'POST':
        action = request.form['action']

        if action == 'b1':
            info = logic_sys.get_database.find_one({'_id': ObjectId(session['my_id'])})
            if 'car' in info:
                return redirect(url_for('orders'))
            return redirect(url_for('choose_way'))

        if action == 'b2':
            session['my_id'] = None
            return render_template('O_start-page.html')

    return render_template('V_profile.html')

@app.route('/delete_acccount', methods = ['POST', 'GET'])
def delete():
    '''
    deletes an account
    '''
    if request.method == 'POST':
        password = request.form['password']
        real_password = \
            logic_sys.get_database.find_one({'_id': ObjectId(session['my_id'])})['password']

        if real_password == password:
            logic_sys.get_database.delete_one({'password': password})
            session['my_id'] = None
            return redirect(url_for('start'))

        flash('Wrong password')
        return render_template('V_delete_account.html')

    return render_template('V_delete_account.html')

@app.route('/main')
def main():
    '''
    main page
    '''
    return render_template('O_main.html')

@app.route('/get_help', methods = ['POST', 'GET'])
def get_help():
    '''
    gets help
    '''
    if request.method == 'POST':
        return redirect(url_for('profile'))
    return render_template('V_get_help.html')

@app.route('/change_info', methods = ['POST', 'GET'])
def change_info():
    """
    changes info about person
    """
    info = logic_sys.get_database.find_one({"_id": ObjectId(session['my_id'])})
    name_surname = info['name'] + " " + info['surname']

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']

        if val.validate_name(name) and val.validate_surname(surname):
            logic_sys.get_database.update_one(info, {"$set": {'name': name, 'surname': surname}})
            name_surname = info['name'] + " " + info['surname']
            return render_template('V_change_info.html', name_surname = name_surname)

        flash('invalid input name surname')
        return render_template('V_change_info.html', name_surname = name_surname)
    # person, change_data

    # logic_sys.get_database.update_one(person, {"$pull": change_data})
    return render_template('V_change_info.html', name_surname = name_surname)

def str_to_dict(string: str) -> dict:
    """
    str to dictionary
    """
    return eval(string)

@app.route('/driver_page', methods=['POST', 'GET'])
def orders():
    """
    shows all orders for drivers
    """
    order_list = []

    all_orders = list(logic_sys.trips_database.find({}))

    for i in all_orders:
        if len(order_list) != 3 and i['status'] == 'created':
            order_list.append(i)
        elif len(order_list) == 3:
            break

    if request.method == 'POST':
        action = request.form.get('action')
        order = request.form.get('orderId')
        order = str_to_dict(order)

        if action == 'button1':
            logic_sys.trips_database.update_one(
                order, {'$set': {'status': 'taken', 'driver': session['my_id']}})
            return render_template('V_driver_map.html')

        if action == 'button2':
            city_list = order['waypoints_list']
            return render_template('M_driver.html', order_list = order_list, city_list = city_list)

    return render_template('M_driver.html', order_list = order_list, city_list = [])

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
def page_not_found(error):
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

        dct_dist = self.make_dist(lst_places)
        way = self.greedy_shortest_path(self.startt, self.end, dct_dist, lst_places)

        return way

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
    def greedy_shortest_path(startt, end, graph, all_points):
        """
        makes a shortest path
        """
        unvisited = set(all_points)
        path = [startt]
        current = startt
        unvisited.remove(startt)

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
