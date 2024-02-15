from flask import Flask, request
from flask_cors import CORS
import redis
import json


app = Flask(__name__)
CORS(app)

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis(host = 'localhost', port = '6379', decode_responses=True, charset="unicode_escape")
# ===============================================

@app.route('/drone', methods=['POST'])
def drone():
    drone = request.get_json()
    drone_ip = request.remote_addr
    drone_id = drone['id']
    drone_longitude = drone['longitude']
    drone_latitude = drone['latitude']
    drone_status = drone['status']
    
    print(drone_ip)
    print(drone_id)
    print(drone_longitude)
    print(drone_latitude)
    print(drone_status)
    
    if (drone_id == "Drone1"):
        redis_server.set('id1', drone_id)
        redis_server.set('ip1', drone_ip)
        redis_server.set('longitude1', drone_longitude)
        redis_server.set('latitude1', drone_latitude)
        redis_server.set('status1', drone_status)
    if (drone_id == "Drone2"):
        redis_server.set('id2', drone_id)
        redis_server.set('ip2', drone_ip)
        redis_server.set('longitude2', drone_longitude)
        redis_server.set('latitude2', drone_latitude)
        redis_server.set('status2', drone_status)
   
    # Get the infomation of the drone in the request, and update the information in Redis database
    # Data that need to be stored in the database: 
    # Drone ID, logitude of the drone, latitude of the drone, drone's IP address, the status of the drone
    # Note that you need to store the metioned infomation for all drones in Redis, think carefully how to store them
    # =========================================================================================




     # =======================================================================================
    return 'Get data'

if __name__ == "__main__":


    app.run(debug=True, host='0.0.0.0', port='5001')
