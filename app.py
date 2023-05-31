from tkinter import Label, Tk, Frame, Button, CENTER
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

        # Open login screen first
        self.current_screen = App.LOGIN_SCREEN
        self.switch_screen_to(App.LOGIN_SCREEN)

    # Switch screens
    def switch_screen_to(self, name):
        old_screen = self.screens[self.current_screen]
        old_screen.grid_forget()

        screen = self.screens[name]
        screen.grid(row=0, column=0, sticky='nsew')
        screen.tkraise()
        screen.focus()

        self.current_screen = name


# The Frame for the login screen
class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(background='#333333')

        # Function to verify login credentials are correct
        def authenticate(*_):
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

        # Position each element on the screen
        login_label.grid(row=0, column=0, sticky='nsew', pady=25)
        username_entry.grid(row=1, column=0, padx=10, pady=15)
        password_entry.grid(row=2, column=0, padx=10, pady=15)
        login_button.grid(row=3, column=0, pady=25)

        # Make enter key work to press login button
        password_entry.bind('<Return>', authenticate)

        # Place holding frame in the center of the screen
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        

# The data visualization screen, shown after login
class DataVisualizationScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Configure how much each column will expand with new space
        self.grid_columnconfigure(0, weight = 4)
        self.grid_columnconfigure(1, weight = 3)
        self.grid_columnconfigure(2, weight = 3)

        # 3 main frames for the three sections of the application
        data_visualizer_frame = Frame(self, bg='red')
        selected_people_frame = Frame(self, bg='green')
        email_template_frame = Frame(self, bg='blue')
      
        # Inside data visualizer frame
        sorting_frame = Frame(data_visualizer_frame, bg='purple')
        chart_frame = Frame(data_visualizer_frame, bg='pink')

        # Inside selected people frame
        to_email_frame = Frame(selected_people_frame, bg='yellow')
        email_list_frame = Frame(selected_people_frame, bg='orange')

        # Inside email template frame
        select_template_frame = Frame(email_template_frame, bg='purple')
        template_list_frame = Frame(email_template_frame, bg='pink')
        
        # Place frames on screen (They initially have 0 width but expand if there are components inside)
        sorting_frame.grid(row=0, column=0, sticky = 'nsew')
        chart_frame.grid(row=1, column=0, sticky = 'nsew')
        to_email_frame.grid(row=0, column=0, sticky='nsew')
        email_list_frame.grid(row=1, column=0, sticky='nsew')
        select_template_frame.grid(row=0, column=0, sticky='nsew')
        template_list_frame.grid(row=1, column=0, sticky='nsew')
        data_visualizer_frame.grid(row=0, column=0, sticky='nsew')
        selected_people_frame.grid(row=0, column=1, sticky='nsew')
        email_template_frame.grid(row=0, column=2, sticky='nsew')

      # Titles for data table
        name_label = Label(chart_frame, text='Name', font=('Verdana', 18))
        training_label = Label(chart_frame, text='Training Name', font=('Verdana', 18))
        expiry_date_label = Label(chart_frame, text='Expiry Date', font=('Expiry Date', 18))

      # Sorting buttons
        sort_by_name_button = Button(sorting_frame, text='Sort by Name', font=('Verdana', 13))
        sort_by_training_name_button = Button(sorting_frame, text='Sort by Training Name', font=('Verdana', 13))
        sort_by_expiry_date_button = Button(sorting_frame, text='Sort by Expiry Date', font=('Verdana', 13))

      # Position each title on the screen
        name_label.grid(row=1, column=0, sticky='w', padx=40, pady=15)
        training_label.grid(row=1, column=1, sticky='w', padx=40, pady=15)
        expiry_date_label.grid(row=1, column=2, sticky='w', padx=40, pady=15)

      # Position each button on the screen
        sort_by_name_button.grid(row=0, column=0, sticky='w', padx=8, pady=15)
        sort_by_training_name_button.grid(row=0, column=1, sticky='w', padx=8, pady=15)
        sort_by_expiry_date_button.grid(row=0, column=2, sticky='w', padx=8, pady=15)

      # Title for selected people frame
        to_email_label = Label(to_email_frame, text='To Email', font=('Verdana', 18))

      # Email send button
        email_send_button = Button(to_email_frame, text='Send', font=('Verdana', 13))

      # Position each title on the screen
        to_email_label.grid(row=0, column=0, sticky='w', padx=40, pady=15)

      # Position each button on the screen
        email_send_button.grid(row=1, column=0, sticky='w', padx=60, pady=15)

      # Title for email template frame
        select_template_label = Label(select_template_frame, text='Select Template', font=('Verdana', 18))

      # Position each title on the screen
        select_template_label.grid(row=0, column=0, sticky='w', padx=40, pady=15)

  
# Start app and start main loop
app = App()
app.mainloop()
