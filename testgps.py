import serial
import pynmea2
import webbrowser

# Configure the serial port
port = "/dev/ttyS0"  # Replace with the actual serial port
baudrate = 9600  # Replace with the baudrate of your GPS module
ser = serial.Serial(port, baudrate, timeout=1)

# Flag to track if the browser window is already opened
browser_opened = False

try:
    while True:
        # Read a line of GPS data
        data = ser.readline().decode("utf-8")

        # Parse the NMEA sentence
        if data.startswith("$GNGGA"):
            try:
                msg = pynmea2.parse(data)
                latitude = msg.latitude
                longitude = msg.longitude
                altitude = msg.altitude
                print("Latitude: {}".format(latitude))
                print("Longitude: {}".format(longitude))
                print("Altitude: {}".format(altitude))

                # Open the map in a web browser if not already opened
                if not browser_opened:
                    map_link = 'http://maps.google.com/?q={},{}'.format(latitude, longitude)
                    webbrowser.open(map_link)
                    browser_opened = True

            except pynmea2.ParseError:
                continue

except KeyboardInterrupt:
    print("Exiting GPS data collection")
