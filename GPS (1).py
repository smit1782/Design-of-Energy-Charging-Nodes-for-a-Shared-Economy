import serial
import pynmea2
import webbrowser
import gmplot
import blynklib

# Configure the serial port
port = "/dev/ttyS0"  # Replace with the actual serial port
baudrate = 9600  # Replace with the baudrate of your GPS module
ser = serial.Serial(port, baudrate, timeout=1)

# Pre-added marker coordinates and names
marker_latitude = [43.48131123391337, 43.48289937543217, 43.48329640428875]
marker_longitude = [-80.55117864595196, -80.54023484097098, -80.53690610028926]
marker_names = ["Location A", "Location B", "Location C"]

# Blynk configuration
BLYNK_AUTH = 'DEfLntieXc8xB9pAJPhQJ0Hklel5h5Ay'  # Replace with your Blynk auth token
blynk = blynklib.Blynk(BLYNK_AUTH)
vpin_latitude = 0  # Virtual pin for latitude
vpin_longitude = 1  # Virtual pin for longitude
print("blynk connected")
# Initialize gmplot
map_gmplot = None

try:
    while True:
        # Read a line of GPS data
        data = ser.readline().decode("utf-8")

        # Parse the NMEA sentence
        if data.startswith("$GNGGA"):
            try:
                print("trying to fetch data")
                msg = pynmea2.parse(data)
                latitude = msg.latitude
                longitude = msg.longitude
                altitude = msg.altitude
                print("Latitude: {}".format(latitude))
                print("Longitude: {}".format(longitude))
                print("Altitude: {}".format(altitude))

                # Create the map and open the web browser only once
                if map_gmplot is None:
                    # Initialize gmplot
                    map_gmplot = gmplot.GoogleMapPlotter(latitude, longitude, 100)

                    # Add pre-added markers with names
                    for lat, lng, name in zip(marker_latitude, marker_longitude, marker_names):
                        map_gmplot.marker(lat, lng, title=name)

                # Add current GPS marker with custom name
                map_gmplot.marker(latitude, longitude, title="Current Location")

                # Generate the map
                map_gmplot.draw("map.html")

                # Open the map in a web browser
                webbrowser.open("map.html")

                # Update Blynk virtual pins with latitude and longitude values
                blynk.virtual_write(vpin_latitude, latitude)
                blynk.virtual_write(vpin_longitude, longitude)

            except pynmea2.ParseError:
                continue



except KeyboardInterrupt:
    print("Exiting GPS data collection")
while True:
# Run Blynk event loop
        blynk.run()
