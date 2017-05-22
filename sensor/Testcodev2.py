from socket import *
import time
import struct
import time
import struct
import csv

f = open('test.csv','wb') 
csv_out = csv.writer(f)
# csv_out.writerow('timestamp,Qx_sensor1,Qy_sensor1,Qz_sensor1,Qw_sensor1,Heading_sensor1,Pitch_sensor1,Roll_sensor1,Qx_sensor2,Qy_sensor2,Qz_sensor2,Qw_sensor2','Heading_sensor2','Pitch_sensor2','Roll_sensor2','diff_Heading','diff_Pitch','diff_Roll','vel_Heading','vel_Pitch','vel_Roll','acc_Heading','acc_Pitch','acc_Roll','Vbat')

csv_out.writerow(['timestamp','Qx_sensor1','Qy_sensor1','Qz_sensor1','Qw_sensor1','Heading_sensor1','Pitch_sensor1','Roll_sensor1','accx','accy','accz','gx','gy','gz','Vbat'])

HOST = '192.168.4.10' # local machine's IP address
PORT = 9048

address = (HOST, PORT) 
client_socket = socket(AF_INET, SOCK_DGRAM) #Set Up the Socket
client_socket.bind((HOST, PORT)) 
client_socket.settimeout(5) #only wait 5 second for a response, otherwise timeout

start = start = time.time()

while(1): #Main Loop
    single_var = client_socket.recvfrom(200)
    test = single_var[0]
    #print(test)
    data = struct.unpack('fffffffffffffff',test) #15 floats for sit-stand device and 25 floats for Harness device
    csv_out.writerow(data)

    #print struct.unpack('fffffffffffffffffffffffff',test)
    time.sleep(10/1000000) # sleep 10 microseconds
    print (".")
