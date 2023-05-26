from tkinter import Label, Tk, Frame, Canvas, Button, CENTER, font
from custom_elements import PlaceholderEntry


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
        self.geometry('340x440')
        
        # Focus on every object with mouse click (so entry boxes/textboxes can be deselected)
        self.bind_all("<1>", lambda event: event.widget.focus_set())

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
        self.configure(background='#333333')

        # Function to verify login credentials are correct
        def authenticate():
            #TODO: add actual verification
            username = username_entry.get()
            password = password_entry.get()
            controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)

        # Frame to keep login centered in the screen
        center_frame = Frame(self)

        # Text and entry boxes for login
        login_label = Label(center_frame, text='Sign In', font=('Verdana', 40))
        username_entry = PlaceholderEntry(center_frame, font=('Verdana', 20), placeholder='Username')
        password_entry = PlaceholderEntry(center_frame, show='*', font=('Verdana', 20), placeholder='Password')
        login_button = Button(center_frame, text='Login', command=authenticate, font=('Verdana', 30))

        # Positioning each element on the screen
        login_label.grid(row=0, column=0, sticky='nsew', pady=25)
        username_entry.grid(row=1, column=0, padx=10, pady=15)
        password_entry.grid(row=2, column=0, padx=10, pady=15)
        login_button.grid(row=3, column=0, pady=25)

        # Place holding frame in the center of the screen
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        

# The data visualization screen, shown after login
class DataVisualizationScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        screen_label = Label(self, text='Data Visualization Screen')
        screen_label.pack()
    

# Start app and start main loop
app = App()
app.mainloop()
