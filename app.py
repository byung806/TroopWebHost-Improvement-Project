from tkinter import Label, Tk, Frame, Entry, Button


# The main window of the application
class App(Tk):
    LOGIN_SCREEN = 0
    DATA_VISUALIZATION_SCREEN = 1

    # THe constructor to initialize the window
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        self.title('TroopWebHost Improvement Project')

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # A dict of all the screen objects
        self.screens = {}
        self.screens[App.LOGIN_SCREEN] = LoginScreen(container, controller=self)
        self.screens[App.DATA_VISUALIZATION_SCREEN] = DataVisualizationScreen(container, controller=self)

        for screen_name in self.screens:
            self.screens[screen_name].grid(row=0, column=0, sticky='nsew')

        # Open login screen first
        self.switch_screen_to(App.LOGIN_SCREEN)

    # Switch screens
    def switch_screen_to(self, name):
        screen = self.screens[name]
        screen.tkraise()


# The Frame for the login screen
class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Function to verify login credentials are correct
        def authenticate():
            #TODO: add actual verification
            username = username_entry.get()
            password = password_entry.get()
            controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)

        # Text and entry boxes for login
        login_label = Label(self, text='Sign In')
        username_label = Label(self, text='Username')
        username_entry = Entry(self)
        password_label = Label(self, text='Password')
        password_entry = Entry(self, show='*')
        login_button = Button(self, text='Login', command=authenticate)

        # Positioning each element on the screen
        login_label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=40)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1, pady=20)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1, pady=20)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)
        

# The data visualization screen, shown after login
class DataVisualizationScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        screen_label = Label(self, text='Data Visualization Screen')
        screen_label.pack()
    

# Start app and start main loop
app = App()
app.mainloop()
