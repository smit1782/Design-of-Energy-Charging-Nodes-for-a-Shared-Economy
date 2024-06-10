import serial
import pynmea2
import webbrowser
import gmplot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure the serial port
port = "/dev/ttyS0"  # Replace with the actual serial port
baudrate = 9600  # Replace with the baudrate of your GPS module
ser = serial.Serial(port, baudrate, timeout=1)

# Pre-added marker coordinates and names
marker_latitude = [43.48131123391337, 43.48289937543217, 43.48329640428875]
marker_longitude = [-80.55117864595196, -80.54023484097098, -80.53690610028926]
marker_names = ["Marker 1", "Marker 2", "Marker 3"]

# Email configuration
sender_email = 'sd28pate@gmail.com'
sender_password = 'Smile_1782'
recipient_email = 'smitpatel1782000@gmail.com'
subject = 'GPS Coordinates'
message_template = 'Latitude: {}\nLongitude: {}\nAltitude: {}\n'

# SMTP server configuration (Gmail SMTP example)
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Initialize gmplot
map_gmplot = None

# Function to send email
def send_email(latitude, longitude, altitude):
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = recipient_email
    email_message['Subject'] = subject

    # Format the message body with GPS coordinates
    message_body = message_template.format(latitude, longitude, altitude)
    email_message.attach(MIMEText(message_body, 'plain'))

    # Create a secure connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(email_message)

    # Close the connection
    server.quit()

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

                # Send email with GPS coordinates
                send_email(latitude, longitude, altitude)

            except pynmea2.ParseError:
                continue

except KeyboardInterrupt:
    print("Exiting GPS data collection")
