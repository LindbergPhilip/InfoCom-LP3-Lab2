from os import fdopen
from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import redis
import pickle
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this so that you can connect to your redis server
# ===============================================
redis_server = redis.Redis(host = 'localhost', port = '6379', decode_responses=True, charset="unicode_escape")
# ===============================================

# Translate OSM coordinate (longitude, latitude) to SVG coordinates (x,y).
# Input coords_osm is a tuple (longitude, latitude).
def translate(coords_osm):
    x_osm_lim = (13.143390664, 13.257501336)
    y_osm_lim = (55.678138854000004, 55.734680845999996)

    x_svg_lim = (212.155699, 968.644301)
    y_svg_lim = (103.68, 768.96)

    x_osm = coords_osm[0]
    y_osm = coords_osm[1]

    x_ratio = (x_svg_lim[1] - x_svg_lim[0]) / (x_osm_lim[1] - x_osm_lim[0])
    y_ratio = (y_svg_lim[1] - y_svg_lim[0]) / (y_osm_lim[1] - y_osm_lim[0])
    x_svg = x_ratio * (x_osm - x_osm_lim[0]) + x_svg_lim[0]
    y_svg = y_ratio * (y_osm_lim[1] - y_osm) + y_svg_lim[0]

    return x_svg, y_svg

@app.route('/', methods=['GET'])
def map():
    return render_template('index.html')

@app.route('/get_drones', methods=['GET'])
def get_drones():
    drone_dict = {}
    
    #Hämta data för Drone1
    longitude1_key = "Drone1:longitude"
    latitude1_key = "Drone1:latitude"
    status1_key = "Drone1:status"
    longitude1 = redis_server.get(longitude1_key)
    latitude1 = redis_server.get(latitude1_key)
    status1 = redis_server.get(status1_key)
    
    
    if longitude1 is not None and latitude1 is not None:
        longitude1 = float(longitude1)
        latitude1 = float(latitude1)
        longitude1_svg,latitude1_svg = translate((longitude1,latitude1))
        drone_dict['DRONE_1'] = {'longitude': longitude1_svg,'latitude': latitude1_svg, 'status': status1}

    #Hämta data för Drone2
    longitude2_key = "Drone2:longitude"
    latitude2_key = "Drone2:latitude"
    status2_key = "Drone2:status"
    longitude2 = redis_server.get(longitude2_key)
    latitude2 = redis_server.get(latitude2_key)
    status2 = redis_server.get(status2_key)
    
    
    if longitude2 is not None and latitude2 is not None:
        longitude2 = float(longitude2)
        latitude2 = float(latitude2)
        longitude2_svg,latitude2_svg = translate((longitude2,latitude2))
        drone_dict['DRONE_2'] = {'longitude': longitude2_svg,'latitude': latitude2_svg, 'status': status2}
    
    
    #=============================================================================================================================================
    # Get the information of all the drones from redis server and update the dictionary `drone_dict' to create the response 
    # drone_dict should have the following format:
    # e.g if there are two drones in the system with IDs: DRONE1 and DRONE2
    # drone_dict = {'DRONE_1':{'longitude': drone1_logitude_svg, 'latitude': drone1_logitude_svg, 'status': drone1_status},
    #               'DRONE_2': {'longitude': drone2_logitude_svg, 'latitude': drone2_logitude_svg, 'status': drone2_status}
    #              }
    # use function translate() to covert the coodirnates to svg coordinates
    #=============================================================================================================================================
    return jsonify(drone_dict)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
