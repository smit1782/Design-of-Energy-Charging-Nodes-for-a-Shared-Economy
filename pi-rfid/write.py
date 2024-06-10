import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
	text = input('New USer:')
	print("NOW PLACE your USER ID card to register...")
	reader.write(text)
	print("Registered")
finally:
	GPIO.cleanup()
