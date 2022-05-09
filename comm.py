from serial import Serial

try:# ser = s.Serial('/dev/ttyUSB0', 9600)
    ser = Serial('/dev/ttyUSB0', 115200)
    ser.write(b'hello!')

    while True:
        rt = ser.read(size=2)
        rt_decoded = rt.decode("utf-8")
        # print(rt_decoded)

    ser.close()

except:
    print("Connection Failed")