# Stefon Miller
# INFOSCI 0010 Group Project
# This program uses Speedtest-cli and mysql connector to run a speedtest and output the results to an MySQL Server

import speedtest
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# Building and floor ID will be set for each individual Raspberry pi and will thus be global variables
# If this were production code, I would check the SSID of the connected network and determine the
# network_id variable from there. However, because I am currently off-campus I wouldn't be able to connect and test
# this feature anyway so it's better left out for now
building_id = 4
floor = 3
network_id = 1

# Connect to the MySQL server containing the tests
#Names of actual server/connection info are ommitted(for obvious reasons)
try:
    c = mysql.connector.connect(host='servername', database='dbname',
                                user='username', password='pw')
    cursor = c.cursor()
    print('Connected to server')
except mysql.connector.Error as e:
    print('Failed to connect to server'.format(e))

# Get time when speedtest was taken
currTime = datetime.now()

# Select the nearest server and begin the test
stest = speedtest.Speedtest()
stest.get_best_server()

# Run a speedtest and store the results in a dictonary
stest.download()
stest.upload()
stest.results.share()
results_dict = stest.results.dict()

#Insert data from our speedtest into the tests table contained in the database
add_test = """INSERT INTO tests(date_taken, time_taken, server_location, download_in_Mbps, upload_in_Mbps,
ping_in_ms, fk_building_id, fk_network_id, floor_number) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """
testDate = currTime.date()
testTime = currTime.time()
servName = results_dict['server']['name']
download = results_dict['download'] / 1000000
upload = results_dict['upload'] / 1000000
ping = results_dict['ping']
try:
    test_data = (testDate, testTime, servName, download, upload, ping, building_id, network_id, floor)
    cursor.execute(add_test, test_data)
except Error as e:
    print("Failed to add data to database")

#Commit changes and close connection
c.commit()
cursor.close()
c.close()
