# classes.py
from typing import List, Dict  # Import type hints for lists and dictionaries

# ------------------
# USER CLASSES
# ------------------
class User:
    def __init__(self, user_id: str, name: str, email: str, password: str):
        try:
            self._user_id = user_id  # Unique ID for the user
            self._name = name  # Name of the user
            self._email = email  # Email address
            self._password = password  # Password for login
        except Exception as e:
            print("Error creating User:", e)

    def get_user_id(self): return self._user_id  # Get user ID
    def set_user_id(self, user_id): self._user_id = user_id  # Set user ID

    def get_name(self): return self._name  # Get user's name
    def set_name(self, name): self._name = name  # Set user's name

    def get_email(self): return self._email  # Get email
    def set_email(self, email): self._email = email  # Set email

    def get_password(self): return self._password  # Get password
    def set_password(self, password): self._password = password  # Set password


class Customer(User):  # Inherits from User
    def __init__(self, user_id, name, email, password, phone_number):
        super().__init__(user_id, name, email, password)
        self.__purchase_history = []  # Stores all bookings made by the customer
        self.__phone_number = phone_number  # Customer's phone number

    def get_purchase_history(self): return self.__purchase_history  # Get all past bookings
    def set_purchase_history(self, history): self.__purchase_history = history  # Set purchase history
    def add_booking(self, booking): self.__purchase_history.append(booking)  # Add a new booking to history

    def get_phone_number(self): return self.__phone_number  # Get phone number
    def set_phone_number(self, phone_number): self.__phone_number = phone_number  # Set phone number


class Admin(User):  # Inherits from User
    def __init__(self, user_id, name, email, password, admin_code):
        super().__init__(user_id, name, email, password)
        self.__admin_code = admin_code  # Code to verify admin identity
        self.__managed_discounts = {}  # Dictionary of ticket discounts

    def get_admin_code(self): return self.__admin_code  # Get admin code
    def set_admin_code(self, code): self.__admin_code = code  # Set admin code

    def get_managed_discounts(self): return self.__managed_discounts  # Get discount list
    def set_managed_discounts(self, discounts): self.__managed_discounts = discounts  # Set new discounts


# ------------------
# TICKET CLASSES
# ------------------
class Ticket:
    def __init__(self, ticket_id: str, price: float, validity: str, description: str):
        self._ticket_id = ticket_id  # Unique ticket ID
        self._price = price  # Ticket price
        self._validity = validity  # How long the ticket is valid
        self._description = description  # Description of ticket

    def get_ticket_id(self): return self._ticket_id  # Get ticket ID
    def set_ticket_id(self, ticket_id): self._ticket_id = ticket_id  # Set ticket ID

    def get_price(self): return self._price  # Get price
    def set_price(self, price): self._price = price  # Set price

    def get_validity(self): return self._validity  # Get validity
    def set_validity(self, validity): self._validity = validity  # Set validity

    def get_description(self): return self._description  # Get description
    def set_description(self, description): self._description = description  # Set description


class SingleRacePass(Ticket):  # Inherits from Ticket
    def __init__(self, ticket_id, price=200.0, validity="1 Day", description="Single race access", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date  # Date of the race
        self.__seat_type = seat_type  # Type of seat

    def get_event_date(self): return self.__event_date  # Get event date
    def set_event_date(self, date): self.__event_date = date  # Set event date

    def get_seat_type(self): return self.__seat_type  # Get seat type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type  # Set seat type


class WeekendPackage(Ticket):  # Inherits from Ticket
    def __init__(self, ticket_id, price=350.0, validity="2 Days", description="Weekend package", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date
        self.__seat_type = seat_type

    def get_event_date(self): return self.__event_date
    def set_event_date(self, date): self.__event_date = date

    def get_seat_type(self): return self.__seat_type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type


class SeasonMembership(Ticket):  # Inherits from Ticket
    def __init__(self, ticket_id, price=800.0, validity="Full Season", description="Season membership", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date
        self.__seat_type = seat_type

    def get_event_date(self): return self.__event_date
    def set_event_date(self, date): self.__event_date = date

    def get_seat_type(self): return self.__seat_type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type


class GroupTicket(Ticket):  # Inherits from Ticket
    def __init__(self, ticket_id, price=150.0, validity="1 Day", description="Group access ticket", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date
        self.__seat_type = seat_type

    def get_event_date(self): return self.__event_date
    def set_event_date(self, date): self.__event_date = date

    def get_seat_type(self): return self.__seat_type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type


# ------------------
# PAYMENT CLASS
# ------------------
class Payment:
    def __init__(self, payment_method, name_on_card, card_number, cvc):
        self.__payment_method = payment_method  # Payment method used
        self.__name_on_card = name_on_card  # Cardholder name
        self.__card_number = card_number  # Card number
        self.__cvc = cvc  # Security code

    def get_payment_method(self): return self.__payment_method
    def set_payment_method(self, method): self.__payment_method = method

    def get_name_on_card(self): return self.__name_on_card
    def set_name_on_card(self, name): self.__name_on_card = name

    def get_card_number(self): return self.__card_number
    def set_card_number(self, number): self.__card_number = number

    def get_cvc(self): return self.__cvc
    def set_cvc(self, cvc): self.__cvc = cvc

    def display_payment_info(self):  # Only show last 4 digits of card
        try:
            return self.__payment_method + " ****" + self.__card_number[-4:]
        except Exception as e:
            return "Error displaying payment info: " + str(e)


# ------------------
# BOOKING CLASS
# ------------------
class Booking:
    def __init__(self, booking_id, customer, tickets, payment):
        self.__booking_id = booking_id  # Unique booking ID
        self.__customer = customer  # The customer who made the booking
        self.__tickets = tickets  # List of tickets in this booking
        self.__payment = payment  # Payment details

    def get_booking_id(self): return self.__booking_id
    def set_booking_id(self, booking_id): self.__booking_id = booking_id

    def get_customer(self): return self.__customer
    def set_customer(self, customer): self.__customer = customer

    def get_tickets(self): return self.__tickets
    def set_tickets(self, tickets): self.__tickets = tickets

    def get_payment(self): return self.__payment
    def set_payment(self, payment): self.__payment = payment

    def display_booking(self):
        try:
            return "Booking #" + self.__booking_id + " for " + self.__customer.get_name()
        except Exception as e:
            return "Error displaying booking: " + str(e)


# ------------------
# INVOICE CLASS
# ------------------
class Invoice:
    def __init__(self, invoice_id, tickets, payment, date_issued):
        self.__invoice_id = invoice_id  # Invoice ID
        self.__tickets = tickets  # Tickets on this invoice
        self.__payment = payment  # Payment info
        self.__date_issued = date_issued  # Invoice issue date

    def get_invoice_id(self): return self.__invoice_id
    def set_invoice_id(self, invoice_id): self.__invoice_id = invoice_id

    def get_tickets(self): return self.__tickets
    def set_tickets(self, tickets): self.__tickets = tickets

    def get_payment(self): return self.__payment
    def set_payment(self, payment): self.__payment = payment

    def get_date_issued(self): return self.__date_issued
    def set_date_issued(self, date): self.__date_issued = date

    def display_invoice(self):
        try:
            return "Invoice #" + self.__invoice_id + " issued on " + self.__date_issued
        except Exception as e:
            return "Error displaying invoice: " + str(e)


# ------------------
# TICKET BOOKING SYSTEM
# ------------------
class TicketBookingSystem:
    def __init__(self):
        self.__users = {}  # All users mapped by user_id
        self.__admins = []  # List of admin users
        self.__bookings = []  # List of all bookings
        self.__tickets = []  # List of all tickets

    def get_users(self): return self.__users
    def set_users(self, users): self.__users = users

    def get_admins(self): return self.__admins
    def set_admins(self, admins): self.__admins = admins

    def get_bookings(self): return self.__bookings
    def set_bookings(self, bookings): self.__bookings = bookings

    def get_tickets(self): return self.__tickets
    def set_tickets(self, tickets): self.__tickets = tickets

    def register_user(self, user): self.__users[user.get_user_id()] = user  # Add user
    def add_booking(self, booking): self.__bookings.append(booking)  # Add booking
    def add_admin(self, admin): self.__admins.append(admin)  # Add admin
    def add_ticket(self, ticket): self.__tickets.append(ticket)  # Add ticket
    def get_user(self, user_id): return self.__users.get(user_id)  # Get user by ID

    def save_data(self): pass  # Saving handled externally
    def load_data(self): pass  # Loading handled externally