import serial
import time

ser = serial.Serial('COM3',9600)
ser.write("500,200,60,1,65,10".encode())
ser.close()