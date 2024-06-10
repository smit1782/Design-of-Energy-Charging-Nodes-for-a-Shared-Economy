import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Set up GPIO
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

# Create an instance of the RFID reader
reader = SimpleMFRC522()

# Product database
products = {
    "001": {"name": "Product 1", "price": 10.0},
    "002": {"name": "Product 2", "price": 15.0},
    "003": {"name": "Product 3", "price": 20.0},
}

# Initialize variables
selected_uid = None
selected_product = None
total_amount = 0.0

def process_payment(uid, amount):
    if uid == selected_uid:
        # Placeholder function for payment processing
        print("Payment processed successfully.")
        print("Amount paid: ", amount)
    else:
        print("Error: Invalid card for payment.")

try:
    while True:
        # Scan for RFID tags
        print("Hold an RFID tag near the reader...")
        uid = reader.read_id()
        
        if uid is not None:
            print("UID: ", uid)
            
            # Convert the UID to string
            uid_str = str(uid)
            
            if selected_uid is None:
                selected_uid = uid
                print("Card with UID", uid, "selected.")
            elif selected_uid == uid:
                print("Card with UID", uid, "already selected.")
            else:
                print("Error: Card with UID", uid, "is different from the selected card.")
                continue

            # Prompt for product selection
            product_id = input("Enter product ID: ")
            
            if product_id in products:
                selected_product = products[product_id]
                total_amount += selected_product["price"]
                print("Product", selected_product["name"], "added.")
                print("Current Total Amount:", total_amount)
            else:
                print("Error: Invalid product ID.")

        # Process payment if 'P' key is pressed
        if input("Press 'P' to make payment: ").upper() == "P":
            process_payment(selected_uid, total_amount)
            print("place the card used priviously to complete the payment...")
            reader.read()
            if selected_uid != reader.read_id():
                print("ERROR :( Valid vard not used ")
            else:
                print("Payment completed.")
            break

except KeyboardInterrupt:
    # Calculate the final bill
    print("Selected Card UID:", selected_uid)
    if selected_product:
        print("Selected Product:", selected_product["name"])
    print("Total Amount: ", total_amount)

    # Clean up GPIO
    GPIO.cleanup()
