# classes.py
from typing import List, Dict

# ------------------
# USER CLASSES
# ------------------
class User:
    def __init__(self, user_id: str, name: str, email: str, password: str):
        try:
            self._user_id = user_id
            self._name = name
            self._email = email
            self._password = password
        except Exception as e:
            print("Error creating User:", e)

    def get_user_id(self): return self._user_id
    def set_user_id(self, user_id): self._user_id = user_id

    def get_name(self): return self._name
    def set_name(self, name): self._name = name

    def get_email(self): return self._email
    def set_email(self, email): self._email = email

    def get_password(self): return self._password
    def set_password(self, password): self._password = password


class Customer(User):
    def __init__(self, user_id, name, email, password, phone_number):
        super().__init__(user_id, name, email, password)
        self.__purchase_history = []
        self.__phone_number = phone_number

    def get_purchase_history(self): return self.__purchase_history
    def set_purchase_history(self, history): self.__purchase_history = history
    def add_booking(self, booking): self.__purchase_history.append(booking)

    def get_phone_number(self): return self.__phone_number
    def set_phone_number(self, phone_number): self.__phone_number = phone_number


class Admin(User):
    def __init__(self, user_id, name, email, password, admin_code):
        super().__init__(user_id, name, email, password)
        self.__admin_code = admin_code
        self.__managed_discounts = {}

    def get_admin_code(self): return self.__admin_code
    def set_admin_code(self, code): self.__admin_code = code

    def get_managed_discounts(self): return self.__managed_discounts
    def set_managed_discounts(self, discounts): self.__managed_discounts = discounts


# ------------------
# TICKET CLASSES
# ------------------
class Ticket:
    def __init__(self, ticket_id: str, price: float, validity: str, description: str):
        self._ticket_id = ticket_id
        self._price = price
        self._validity = validity
        self._description = description

    def get_ticket_id(self): return self._ticket_id
    def set_ticket_id(self, ticket_id): self._ticket_id = ticket_id

    def get_price(self): return self._price
    def set_price(self, price): self._price = price

    def get_validity(self): return self._validity
    def set_validity(self, validity): self._validity = validity

    def get_description(self): return self._description
    def set_description(self, description): self._description = description


class SingleRacePass(Ticket):
    def __init__(self, ticket_id, price=200.0, validity="1 Day", description="Single race access", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date
        self.__seat_type = seat_type

    def get_event_date(self): return self.__event_date
    def set_event_date(self, date): self.__event_date = date

    def get_seat_type(self): return self.__seat_type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type


class WeekendPackage(Ticket):
    def __init__(self, ticket_id, price=350.0, validity="2 Days", description="Weekend package", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date
        self.__seat_type = seat_type

    def get_event_date(self): return self.__event_date
    def set_event_date(self, date): self.__event_date = date

    def get_seat_type(self): return self.__seat_type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type


class SeasonMembership(Ticket):
    def __init__(self, ticket_id, price=800.0, validity="Full Season", description="Season membership", event_date="", seat_type=""):
        super().__init__(ticket_id, price, validity, description)
        self.__event_date = event_date
        self.__seat_type = seat_type

    def get_event_date(self): return self.__event_date
    def set_event_date(self, date): self.__event_date = date

    def get_seat_type(self): return self.__seat_type
    def set_seat_type(self, seat_type): self.__seat_type = seat_type


class GroupTicket(Ticket):
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
        self.__payment_method = payment_method
        self.__name_on_card = name_on_card
        self.__card_number = card_number
        self.__cvc = cvc

    def get_payment_method(self): return self.__payment_method
    def set_payment_method(self, method): self.__payment_method = method

    def get_name_on_card(self): return self.__name_on_card
    def set_name_on_card(self, name): self.__name_on_card = name

    def get_card_number(self): return self.__card_number
    def set_card_number(self, number): self.__card_number = number

    def get_cvc(self): return self.__cvc
    def set_cvc(self, cvc): self.__cvc = cvc

    def display_payment_info(self):
        try:
            return self.__payment_method + " ****" + self.__card_number[-4:]
        except Exception as e:
            return "Error displaying payment info: " + str(e)


# ------------------
# BOOKING CLASS
# ------------------
class Booking:
    def __init__(self, booking_id, customer, tickets, payment):
        self.__booking_id = booking_id
        self.__customer = customer
        self.__tickets = tickets
        self.__payment = payment

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
        self.__invoice_id = invoice_id
        self.__tickets = tickets
        self.__payment = payment
        self.__date_issued = date_issued

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
        self.__users = {}
        self.__admins = []
        self.__bookings = []
        self.__tickets = []

    def get_users(self): return self.__users
    def set_users(self, users): self.__users = users

    def get_admins(self): return self.__admins
    def set_admins(self, admins): self.__admins = admins

    def get_bookings(self): return self.__bookings
    def set_bookings(self, bookings): self.__bookings = bookings

    def get_tickets(self): return self.__tickets
    def set_tickets(self, tickets): self.__tickets = tickets

    def register_user(self, user): self.__users[user.get_user_id()] = user
    def add_booking(self, booking): self.__bookings.append(booking)
    def add_admin(self, admin): self.__admins.append(admin)
    def add_ticket(self, ticket): self.__tickets.append(ticket)
    def get_user(self, user_id): return self.__users.get(user_id)

    def save_data(self): pass  # Implemented in backend.py
    def load_data(self): pass