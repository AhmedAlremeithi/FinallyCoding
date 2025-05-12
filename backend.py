# backend.py
import pickle  # For saving and loading objects in binary format
import os  # For checking file existence
from classes import TicketBookingSystem  # Importing main system class

DATA_FILE = "data.pkl"  # Filename to store serialized data

# ------------------------------
# SAVE SYSTEM DATA
# ------------------------------
def save_data(system: TicketBookingSystem):
    try:
        with open(DATA_FILE, "wb") as file:  # Open file in write-binary mode
            data = {
                "users": system.get_users(),  # Save user dictionary
                "admins": system.get_admins(),  # Save admin list
                "bookings": system.get_bookings(),  # Save booking list
                "tickets": system.get_tickets()  # Save ticket list
            }
            pickle.dump(data, file)  # Serialize and write to file
    except Exception as e:
        print("Error saving data:", e)  # Print error if something goes wrong


# ------------------------------
# LOAD SYSTEM DATA
# ------------------------------
def load_data() -> TicketBookingSystem:
    system = TicketBookingSystem()  # Initialize empty system
    if os.path.exists(DATA_FILE):  # Check if data file exists
        try:
            with open(DATA_FILE, "rb") as file:  # Open file in read-binary mode
                data = pickle.load(file)  # Deserialize the file contents
                system.set_users(data.get("users", {}))  # Load users
                system.set_admins(data.get("admins", []))  # Load admins
                system.set_bookings(data.get("bookings", []))  # Load bookings
                system.set_tickets(data.get("tickets", []))  # Load tickets
        except Exception as e:
            print("Error loading data:", e)  # Print error if loading fails
    return system  # Return the populated system object


# ------------------------------
# GENERATE UNIQUE BOOKING ID
# ------------------------------
def generate_booking_id(system: TicketBookingSystem) -> str:
    try:
        return "B" + str(len(system.get_bookings()) + 1)  # Booking ID based on count
    except Exception as e:
        print("Error generating booking ID:", e)  # Print error if fails
        return "B0"  # Fallback ID


# ------------------------------
# GENERATE UNIQUE TICKET ID
# ------------------------------
def generate_ticket_id(system: TicketBookingSystem) -> str:
    try:
        return "T" + str(len(system.get_tickets()) + 1)  # Ticket ID based on count
    except Exception as e:
        print("Error generating ticket ID:", e)  # Print error if fails
        return "T0"  # Fallback ID