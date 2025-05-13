#GG  GUI SECTION
import tkinter as tk  # Import tkinter for GUI
from tkinter import ttk, messagebox  # Import widgets and dialogs
from classes import *  # Import all classes from classes.py
from backend import load_data, save_data, generate_booking_id, generate_ticket_id  # Import backend functions
from datetime import date

class TicketBookingGUI:
    def __init__(self, root):
        self.root = root  # Main window
        self.root.title("Grand Prix Ticket Booking")  # Set window title
        self.system = load_data()  # Load saved system data
        self.current_user = None  # Store current user (Admin or Customer)
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()  # Pack the frame into the root window
        self.login_screen()  # Show login screen initially

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()  # Remove all widgets from the frame

    def login_screen(self):
        self.clear_frame()  # Clear previous screen
        # Create login fields and labels
        tk.Label(self.frame, text="Welcome to Grand Prix Booking System", font=("Helvetica", 14, "bold")).pack(pady=10)
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
        tk.Label(self.frame, text=f"Welcome {self.current_user.get_name()}", font=("Helvetica", 14, "bold")).pack(pady=10)
        tk.Button(self.frame, text="Book Tickets", command=self.ticket_selection_screen).pack(pady=5)
        tk.Button(self.frame, text="View Purchase History", command=self.view_purchase_history).pack(pady=5)
        tk.Button(self.frame, text="Logout", command=self.login_screen).pack(pady=10)
        tk.Button(self.frame, text="Edit Account Info", command=self.edit_account_screen).pack(pady=5)
        tk.Button(self.frame, text="Delete Account", command=self.delete_account).pack(pady=5)

    def view_purchase_history(self):
        self.clear_frame()
        tk.Label(self.frame, text="Purchase History", font=("Helvetica", 14, "bold")).pack(pady=10)

        history = self.current_user.get_purchase_history()
        if not history:
            tk.Label(self.frame, text="No past purchases found.").pack()
        else:
            for index, booking in enumerate(history):
                try:
                    # Booking summary text
                    info = booking.display_booking()
                    for ticket in booking.get_tickets():
                        info += f"\n  - {ticket.__class__.__name__} on {ticket.get_event_date()} ({ticket.get_price()} AED)"

                    # Display booking
                    label = tk.Label(self.frame, text=info, justify="left", anchor="w")
                    label.pack(anchor="w", pady=2)

                    # Add a delete button next to each booking
                    btn = tk.Button(self.frame, text="Delete", command=lambda b=booking: self.delete_booking(b))
                    btn.pack(pady=1)
                except AttributeError as e:
                    tk.Label(self.frame, text="Error displaying booking: " + str(e)).pack()

        tk.Button(self.frame, text="Back", command=self.customer_dashboard).pack(pady=10)

    def ticket_selection_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Select Tickets", font=("Helvetica", 14, "bold")).pack(pady=10)
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
        tk.Label(self.frame, text="Payment Page", font=("Helvetica", 14, "bold")).pack(pady=10)
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
        tk.Label(self.frame, text="Invoice", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Create an Invoice object
        invoice_id = "INV" + booking.get_booking_id()[1:]  # Example: "B5" becomes "INV5"
        invoice = Invoice(invoice_id, booking.get_tickets(), booking.get_payment(), date.today().isoformat())

        # Display invoice summary
        invoice_text = invoice.display_invoice() + "\n"
        for ticket in invoice.get_tickets():
            invoice_text += f"{ticket.__class__.__name__} - {ticket.get_price()} AED on {ticket.get_event_date()}\n"

        # Show it in the GUI
        tk.Label(self.frame, text=invoice_text, justify="left").pack()

        # Back to login
        tk.Button(self.frame, text="Back to Login", command=self.login_screen).pack(pady=10)

    def admin_dashboard(self):
        self.clear_frame()
        tk.Label(self.frame, text="Admin Dashboard", font=("Helvetica", 14, "bold")).pack(pady=10)
        tk.Label(self.frame, text="Tickets Sold: " + str(len(self.system.get_bookings()))).pack()

        tk.Label(self.frame, text="\nCustomer Purchases:").pack()
        for booking in self.system.get_bookings():
            try:
                customer_name = booking.get_customer().get_name()
                ticket_list = ", ".join([ticket.__class__.__name__ + " (" + str(ticket.get_price()) + " AED) on " + ticket.get_event_date() for ticket in booking.get_tickets()])
                display_text = customer_name + " - " + ticket_list
                tk.Label(self.frame, text=display_text).pack(anchor="w")
            except AttributeError as e:
                tk.Label(self.frame, text="Error loading booking: " + str(e)).pack(anchor="w")

        tk.Label(self.frame, text="\nModify Discounts", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
        self.discount_type = ttk.Combobox(self.frame, values=["SingleRacePass", "WeekendPackage", "SeasonMembership", "GroupTicket"])
        self.discount_type.pack(pady=5)
        self.discount_value = tk.Entry(self.frame)
        self.discount_value.pack()
        tk.Button(self.frame, text="Apply Discount", command=self.apply_discount).pack(pady=10)
        tk.Button(self.frame, text="Logout", command=self.login_screen).pack()

    def edit_account_screen(self):
        self.clear_frame()
        tk.Label(self.frame, text="Edit Account Information", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Editable fields
        tk.Label(self.frame, text="New Name:").pack()
        name_entry = tk.Entry(self.frame)
        name_entry.insert(0, self.current_user.get_name())
        name_entry.pack()

        tk.Label(self.frame, text="New Email:").pack()
        email_entry = tk.Entry(self.frame)
        email_entry.insert(0, self.current_user.get_email())
        email_entry.pack()

        tk.Label(self.frame, text="New Password:").pack()
        password_entry = tk.Entry(self.frame, show="*")
        password_entry.insert(0, self.current_user.get_password())
        password_entry.pack()

        # Phone number only if user is a Customer
        if isinstance(self.current_user, Customer):
            tk.Label(self.frame, text="New Phone Number:").pack()
            phone_entry = tk.Entry(self.frame)
            phone_entry.insert(0, self.current_user.get_phone_number())
            phone_entry.pack()
        else:
            phone_entry = None

        def save_changes():
            self.current_user.set_name(name_entry.get())
            self.current_user.set_email(email_entry.get())
            self.current_user.set_password(password_entry.get())
            if isinstance(self.current_user, Customer):
                self.current_user.set_phone_number(phone_entry.get())

            save_data(self.system)
            messagebox.showinfo("Success", "Account info updated.")
            self.customer_dashboard()

        # Buttons
        tk.Button(self.frame, text="Save Changes", command=save_changes).pack(pady=10)
        tk.Button(self.frame, text="Back", command=self.customer_dashboard).pack(pady=5)

    def delete_account(self):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete your account? This cannot be undone.")
        if confirm:
            user_id = self.current_user.get_user_id()

            # Remove from user dictionary
            if user_id in self.system.get_users():
                del self.system.get_users()[user_id]

            # Remove from admin list if needed
            if isinstance(self.current_user, Admin):
                try:
                    self.system.get_admins().remove(self.current_user)
                except ValueError:
                    pass

            save_data(self.system)
            messagebox.showinfo("Deleted", "Your account has been deleted.")
            self.current_user = None
            self.login_screen()

    def delete_booking(self, booking):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?")
        if confirm:
            try:
                self.current_user.remove_booking(booking)  # Remove from customer history
                self.system.get_bookings().remove(booking)  # Remove from system records
                save_data(self.system)
                messagebox.showinfo("Deleted", "Booking deleted successfully.")
                self.view_purchase_history()  # Refresh the screen
            except ValueError:
                messagebox.showerror("Error", "Could not delete booking.")

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