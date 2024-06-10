import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
GPIO.setwarnings(False)
# Set up the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Create an instance of the RFID reader
reader = SimpleMFRC522()

try:
    while True:
        # Wait for a card to be detected
        text = input('place your card name:')
        reader.write(text)
        print("valid!")
        print("Hold your card near the reader")
        id, text = reader.read()

        # Prompt the user to enter the amount to be paid
        amount = float(input("Enter the amount to be paid: $"))
        print("Please TAP your card to complete payment")
        id, text = reader.read()
        print("payment successful!!")

        # Process the payment
        #process_payment(id, amount)

finally:
    # Clean up the GPIO pins
    GPIO.cleanup()
