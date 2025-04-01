from ViewDA import *
from ModelDA import *
from ControllerDA import *

from ModelUser import *
from ControllerUser import *
server = 'LAPTOPSN\SQLEXPRESST'
database = 'qlnv'


class Controller:
    def __init__(self, model, login_view):
        self.model = model
        self.login_view = login_view

    def login(self, username, password):
        # Check if the provided credentials match any user
        if self.model.verify_user(username, password):
            x=self.model.find_LoaiNV(username);
            if x=="Admin":
                # If login is successful, show the dashboard view and create its widgets
                self.login_view.withdraw()
                self.login_view.destroy()
                # Call create_widgets to initialize the widgets, including buttons
                dashboard_view = ViewDA(server, database)  # Pass the root to the View
                model = ModelDA(server, database)
                controller = ControllerDA(dashboard_view, model, server, database)
                # Start the Tkinter event loop for the login view only
                dashboard_view.mainloop()
            else:
                self.login_view.withdraw()
                self.login_view.destroy()
                user_view = ViewUser(server, database)
                model = ModelUser(server, database)
                controller = ControllerUser(user_view, model, server, database)
                controller.LoadNV(username)
                user_view.mainloop()


        else:
            self.login_view.show_message("Invalid username or password")

    def show_dashboard(self):
        # Hide the login view and show the dashboard view
        self.login_view.withdraw()

