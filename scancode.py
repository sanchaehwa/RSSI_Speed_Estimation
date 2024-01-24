21
#!/usr/bin/env python
# test BLE Scanning software
# jcs 6/8/2014
import blescan
import sys
#import bluetooth._bluetooth as bluez
import pymysql
from time import sleep
import threading
import os
import openpyxl
import time
import argparse 



##########################################
#               Database                 #
##########################################

class DB_sending:
    def __init__(self):
        self.url = "210.115.227.109"
        self.id = 'cic'
        self.password = '20180903in'
        self.dbName = 'beacon_dataset'
        #self.id = 'root'
        #self.password = 'cic108$$'

    def creat_connet(self):
        self.db = pymysql.connect(host=self.url, port=3306, user=self.id, passwd=self.password, db=self.dbName, charset='utf8')
        self.cursor = self.db.cursor()

  #  def insert_unique_data(self, mac, uuid, major, minor):
       # sql = "insert into test (mac, UUID, major, minor) " \
             #   "select '"+ mac+"' ,'"+uuid+"' ,'"+major+"' ,'"+minor+"' from dual where not exists" \
              #  "( select * from beacon_unique_info_tb where mac = '"+mac+"' and UUID = '"+uuid+"')"
      #  self.cursor.execute(sql)
      #  self.db.commit()
        #print(self.cursor.lastrowid)

    # def insert_valiable_data(self, table ,minor, rssi):
    #     sql = "INSERT INTO "+str(table)+" (minor, rssi, time) VALUES ('"+ minor +"', '"+ rssi +"', CURRENT_TIMESTAMP);"
    #     #print(sql)
    #     self.cursor.execute(sql) 
    #     self.db.commit()
    #     #print(self.cursor.lastrowid)    
        
        
   # def insert_valiable_data(self, minor, rssi):
     #   sql = "test (`minor`, `rssi`, `time`) VALUES ('"+ minor +"', '"+ rssi +"', CURRENT_TIMESTAMP);"
        #print(sql)
       # self.cursor.execute(sql)
       # self.db.commit()

    # def insert_valiable_data(self, mac, rssi, txpower, accuracy):
    #     sql = "INSERT INTO `device_variable_info_tb` (`mac`, `rssi`, `txpower`, `accuracy`, `time`) VALUES ('"+ mac +"', '"+ rssi +"', '"+ txpower +"', '"+ accuracy +"', CURRENT_TIMESTAMP);"
    #     print(sql)
    #     self.cursor.execute(sql)
    #     self.db.commit()
    #     print(self.cursor.lastrowid)

     def insert_beacon_rssi2(self, mac, txpower, rssi, distance, time):
         sql = "INSERT INTO test (mac, txpower, rssi, distance, time) VALUES ('"+ mac +"', '"+ txpower +"', '"+ rssi +"', '"+ distance +"', CURRENT_TIMESTAMP);"
         self.cursor.execute(sql)
         self.db.commit()

    # def insert_beacon_rssi3(self, mac, major, minor, rssi, txpower, est_dist, time):
    #     sql = "INSERT INTO q_learning_tb (mac, major, minor, rssi, txpower, est_dist, time) VALUES ('"+ mac +"','"+ major +"','"+ minor +"','"+ rssi +"','"+ txpower +"','"+ est_dist +"', CURRENT_TIMESTAMP);"
    #     self.cursor.execute(sql)
    #     self.db.commit()

    # def run_sensor_thread(self):
    #     os.system("sudo python3 /home/pi/sensorDataToDB.py")



dev_id = 0
conn = DB_sending()


##########################################
#           Bluetooth scan               #
##########################################
try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")

except:
    print("error accessing bluetooth device...")
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)


conn.creat_connet()
##########################################
#       Beacon info check & EXCEL add    #
##########################################
while True:
        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:
            beacon_split = beacon.split(',')
            if beacon_split[2] in ["1111"]:
                # [0] MAC, [1] UUID, [2] Major, [3] Minor, [4] Tx Power, [5] RSSI
                
                conn.insert_unique_data(beacon_split[0], beacon_split[4], beacon_split[5], beacon_split[3])
                #conn.insert_valiable_data(beacon_split[3] , beacon_split[5] )
                
conn.db.close()

