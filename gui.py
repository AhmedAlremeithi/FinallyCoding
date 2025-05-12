# gui.py
import tkinter as tk  # Import tkinter for GUI
from tkinter import ttk, messagebox  # Import widgets and dialogs
from classes import *  # Import all classes from classes.py
from backend import load_data, save_data, generate_booking_id, generate_ticket_id  # Import backend functions

class TicketBookingGUI:
    def __init__(self, root):
        self.root = root  # Main window
        self.root.title("Grand Prix Ticket Booking")  # Set window title
        self.system = load_data()  # Load saved system data
        self.current_user = None  # Store current user (Admin or Customer)
        self.frame = tk.Frame(self.root)  # Create frame to hold widgets
        self.frame.pack()  # Pack the frame into the root window
        self.login_screen()  # Show login screen initially

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()  # Remove all widgets from the frame

    def login_screen(self):
        self.clear_frame()  # Clear previous screen
        # Create login fields and labels
        tk.Label(self.frame, text="Welcome to Grand Prix Booking System").pack(pady=10)
        tk.Label(self.frame, text="Name:").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()
        tk.Label(self.frame, text="Email:").pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()
        tk.Label(self.frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()
        tk.Label(self.frame, text="Phone Number (Customer only):").pack()
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.pack()
        tk.Label(self.frame, text="Admin Code (optional):").pack()
        self.admin_code_entry = tk.Entry(self.frame)
        self.admin_code_entry.pack()
        # Login/Register button
        tk.Button(self.frame, text="Login/Register", command=self.handle_login).pack(pady=10)

    def handle_login(self):
        # Get input values
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()
        admin_code = self.admin_code_entry.get()

        if not name or not email or not password:
            messagebox.showerror("Error", "Name, Email and Password are required")
            return

        # Create user ID from name and email
        user_id = name.lower().replace(" ", "") + "_" + email.split("@")[0]
        user = self.system.get_user(user_id)  # Check if user already exists

        if user:
            # Existing user
            if admin_code.strip() == "ADMINS12" and isinstance(user, Admin):
                self.current_user = user
                self.admin_dashboard()
            elif admin_code.strip() == "ADMINS12" and not isinstance(user, Admin):
                # Upgrade to admin
                upgraded_admin = Admin(user.get_user_id(), user.get_name(), user.get_email(), user.get_password(), admin_code)
                self.system.add_admin(upgraded_admin)
                self.system.register_user(upgraded_admin)
                self.current_user = upgraded_admin
                self.admin_dashboard()
            elif isinstance(user, Admin):
                self.current_user = user
                self.admin_dashboard()
            else:
                self.current_user = user
                self.customer_dashboard()
        else:
            # New user registration
            if admin_code == "ADMINS12":
                user = Admin(user_id, name, email, password, admin_code)
                self.system.add_admin(user)
                self.system.register_user(user)
                self.current_user = user
                self.admin_dashboard()
            else:
                if not phone:
                    messagebox.showerror("Error", "Phone number required for customer registration")
                    return
                user = Customer(user_id, name, email, password, phone)
                self.system.register_user(user)
                self.current_user = user
                self.customer_dashboard()

        save_data(self.system)  # Save user after login

    def customer_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text=f"Welcome {self.current_user.get_name()}").pack(pady=10)
        tk.Button(self.frame, text="Book Tickets", command=self.ticket_selection_screen).pack(pady=5)
        tk.Button(self.frame, text="View Purchase History", command=self.view_purchase_history).pack(pady=5)
        tk.Button(self.frame, text="Logout", command=self.login_screen).pack(pady=10)

    def view_purchase_history(self):
        self.clear_frame()
        tk.Label(self.frame, text="Purchase History").pack(pady=10)
        history = self.current_user.get_purchase_history()
        if not history:
            tk.Label(self.frame, text="No past purchases found.").pack()
        else:
            for booking in history:
                try:
                    info = booking.display_booking()
                    for ticket in booking.get_tickets():
                        info += f"\n  - {ticket.__class__.__name__} on {ticket.get_event_date()} ({ticket.get_price()} AED)"
                    tk.Label(self.frame, text=info, justify="left").pack(anchor="w")
                except Exception as e:
                    tk.Label(self.frame, text="Error displaying booking: " + str(e)).pack()
        tk.Button(self.frame, text="Back", command=self.customer_dashboard).pack(pady=10)

    def ticket_selection_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Select Tickets").pack(pady=10)
        tk.Label(self.frame, text="Enter Race Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.frame)
        self.date_entry.pack()

        self.ticket_options = [SingleRacePass, WeekendPackage, SeasonMembership, GroupTicket]  # Ticket types
        self.ticket_vars = {}  # Store selected ticket types

        for ticket_class in self.ticket_options:
            ticket_id = generate_ticket_id(self.system)  # Generate temporary ID
            temp_ticket = ticket_class(ticket_id)  # Create temp ticket
            var = tk.IntVar()
            label = f"{ticket_class.__name__} - {temp_ticket.get_price()} AED"
            self.ticket_vars[ticket_class] = var
            tk.Checkbutton(self.frame, text=label, variable=var).pack(anchor="w")

        tk.Button(self.frame, text="Proceed to Payment", command=self.payment_screen).pack(pady=10)

    def payment_screen(self):
        self.selected_tickets = []
        date = self.date_entry.get()
        if not date:
            messagebox.showerror("Error", "Please enter a race date.")
            return

        for ticket_class, var in self.ticket_vars.items():
            if var.get() == 1:
                ticket_id = generate_ticket_id(self.system)
                ticket = ticket_class(ticket_id)
                ticket.set_event_date(date)
                if isinstance(self.current_user, Customer):
                    for admin in self.system.get_admins():
                        discounts = admin.get_managed_discounts()
                        if ticket.__class__.__name__ in discounts:
                            discounted_price = discounts[ticket.__class__.__name__]
                            ticket.set_price(discounted_price)
                self.selected_tickets.append(ticket)

        if not self.selected_tickets:
            messagebox.showerror("Error", "No ticket selected")
            return

        self.clear_frame()
        tk.Label(self.frame, text="Payment Page").pack(pady=10)
        tk.Label(self.frame, text="Payment Method:").pack()
        self.method_entry = ttk.Combobox(self.frame, values=["Credit Card", "Debit Card", "PayPal"])
        self.method_entry.pack()
        tk.Label(self.frame, text="Name on Card:").pack()
        self.name_card_entry = tk.Entry(self.frame)
        self.name_card_entry.pack()
        tk.Label(self.frame, text="Card Number:").pack()
        self.card_entry = tk.Entry(self.frame)
        self.card_entry.pack()
        tk.Label(self.frame, text="CVC:").pack()
        self.cvc_entry = tk.Entry(self.frame)
        self.cvc_entry.pack()
        tk.Button(self.frame, text="Pay Now", command=self.process_payment).pack(pady=10)

    def process_payment(self):
        method = self.method_entry.get()
        name = self.name_card_entry.get()
        card = self.card_entry.get()
        cvc = self.cvc_entry.get()

        if not method or not name or not card or not cvc:
            messagebox.showerror("Error", "All fields required")
            return

        payment = Payment(method, name, card, cvc)
        booking_id = generate_booking_id(self.system)
        booking = Booking(booking_id, self.current_user, self.selected_tickets, payment)
        self.system.add_booking(booking)
        if isinstance(self.current_user, Customer):
            self.current_user.add_booking(booking)
        save_data(self.system)
        self.invoice_screen(booking)

    def invoice_screen(self, booking):
        self.clear_frame()
        tk.Label(self.frame, text="Invoice").pack(pady=10)
        summary = booking.display_booking() + "\n"
        for ticket in booking.get_tickets():
            summary += ticket.__class__.__name__ + " - " + str(ticket.get_price()) + " AED on " + ticket.get_event_date() + "\n"
        tk.Label(self.frame, text=summary).pack()
        tk.Button(self.frame, text="Back to Login", command=self.login_screen).pack(pady=10)

    def admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Dashboard").pack(pady=10)
        tk.Label(self.frame, text="Tickets Sold: " + str(len(self.system.get_bookings()))).pack()

        tk.Label(self.frame, text="\nCustomer Purchases:").pack()
        for booking in self.system.get_bookings():
            try:
                customer_name = booking.get_customer().get_name()
                ticket_list = ", ".join([ticket.__class__.__name__ + " (" + str(ticket.get_price()) + " AED) on " + ticket.get_event_date() for ticket in booking.get_tickets()])
                display_text = customer_name + " - " + ticket_list
                tk.Label(self.frame, text=display_text).pack(anchor="w")
            except Exception as e:
                tk.Label(self.frame, text="Error loading booking: " + str(e)).pack(anchor="w")

        tk.Label(self.frame, text="\nModify Discounts").pack()
        self.discount_type = ttk.Combobox(self.frame, values=["GroupTicket", "SeasonMembership"])
        self.discount_type.pack()
        self.discount_value = tk.Entry(self.frame)
        self.discount_value.pack()
        tk.Button(self.frame, text="Apply Discount", command=self.apply_discount).pack(pady=10)
        tk.Button(self.frame, text="Logout", command=self.login_screen).pack()

    def apply_discount(self):
        ticket_type = self.discount_type.get()
        value = self.discount_value.get()
        try:
            value = float(value)
            if isinstance(self.current_user, Admin):
                discounts = self.current_user.get_managed_discounts()
                discounts[ticket_type] = value
                self.current_user.set_managed_discounts(discounts)
                messagebox.showinfo("Success", "Discount updated")
                save_data(self.system)
        except ValueError:
            messagebox.showerror("Error", "Invalid discount value")

if __name__ == "__main__":
    root = tk.Tk()  # Create root window
    app = TicketBookingGUI(root)  # Start the GUI
    root.mainloop()  # Keep GUI running