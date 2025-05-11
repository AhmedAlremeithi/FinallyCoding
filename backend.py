# backend.py
import pickle
import os
from classes import TicketBookingSystem

DATA_FILE = "data.pkl"

# ------------------------------
# SAVE SYSTEM DATA
# ------------------------------
def save_data(system: TicketBookingSystem):
    try:
        with open(DATA_FILE, "wb") as file:
            data = {
                "users": system.get_users(),
                "admins": system.get_admins(),
                "bookings": system.get_bookings(),
                "tickets": system.get_tickets()
            }
            pickle.dump(data, file)
    except Exception as e:
        print("Error saving data:", e)


# ------------------------------
# LOAD SYSTEM DATA
# ------------------------------
def load_data() -> TicketBookingSystem:
    system = TicketBookingSystem()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "rb") as file:
                data = pickle.load(file)
                system.set_users(data.get("users", {}))
                system.set_admins(data.get("admins", []))
                system.set_bookings(data.get("bookings", []))
                system.set_tickets(data.get("tickets", []))
        except Exception as e:
            print("Error loading data:", e)
    return system


# ------------------------------
# GENERATE UNIQUE BOOKING ID
# ------------------------------
def generate_booking_id(system: TicketBookingSystem) -> str:
    try:
        return "B" + str(len(system.get_bookings()) + 1)
    except Exception as e:
        print("Error generating booking ID:", e)
        return "B0"


# ------------------------------
# GENERATE UNIQUE TICKET ID
# ------------------------------
def generate_ticket_id(system: TicketBookingSystem) -> str:
    try:
        return "T" + str(len(system.get_tickets()) + 1)
    except Exception as e:
        print("Error generating ticket ID:", e)
        return "T0"
