from tkinter import Tk, CENTER
from tkinter.ttk import Label, Frame, Button, Style, LabelFrame
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

        # Function to verify login credentials are correct
        def authenticate(*_):
            #TODO: add actual verification
            username = username_entry.get()
            password = password_entry.get()
            if True:  # if login failed
                password_entry.reset()
                password_entry.focus_set()
                error_label.grid(row=3, column=0)
            else:
                controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)

        # Frame to keep login centered in the screen
        center_frame = LabelFrame(self, text='Sign In', labelanchor='n')

        # Text and entry boxes for login
        #login_label = Label(center_frame, text='Sign In')
        username_entry = PlaceholderEntry(center_frame, placeholder='Username')
        password_entry = PlaceholderEntry(center_frame, show='*', placeholder='Password')
        error_label = Label(center_frame, text='Incorrect username or password.', style='TLabel')
        login_button = Button(center_frame, text='Login', command=authenticate)

        # Position each element on the screen
        #login_label.grid(row=0, column=0, sticky='nsew', pady=25)
        username_entry.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=2, column=0, padx=10, pady=10)
        login_button.grid(row=4, column=0, pady=10)

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
        
        # COLUMN 1
        # ------ LEFTMOST DATA VISUALIZATION FRAME ------
        data_visualizer_frame = LabelFrame(self, text='data_visualizer_frame')

        # Top sorting frame
        sorting_frame = LabelFrame(data_visualizer_frame, text='sorting_frame')
        sort_by_name_button = Button(sorting_frame, text='Sort by Name')
        sort_by_training_name_button = Button(sorting_frame, text='Sort by Training Name')
        sort_by_expiry_date_button = Button(sorting_frame, text='Sort by Expiry Date')

        sort_by_name_button.grid(row=0, column=0, sticky='w', padx=8, pady=15)
        sort_by_training_name_button.grid(row=0, column=1, sticky='w', padx=8, pady=15)
        sort_by_expiry_date_button.grid(row=0, column=2, sticky='w', padx=8, pady=15)

        # Bottom chart frame
        chart_frame = LabelFrame(data_visualizer_frame, text='chart_frame')
        name_label = Label(chart_frame, text='Name')
        training_label = Label(chart_frame, text='Training Name')
        expiry_date_label = Label(chart_frame, text='Expiry Date')

        name_label.grid(row=1, column=0, sticky='w', padx=40, pady=15)
        training_label.grid(row=1, column=1, sticky='w', padx=40, pady=15)
        expiry_date_label.grid(row=1, column=2, sticky='w', padx=40, pady=15)

        # Place frames on screen (They initially have 0 width but expand if there are components inside)
        sorting_frame.grid(row=0, column=0, sticky = 'nsew')
        chart_frame.grid(row=1, column=0, sticky = 'nsew')
        data_visualizer_frame.grid(row=0, column=0, sticky='nsew')





        # COLUMN 2
        # ------ MIDDLE SELECTED PEOPLE FRAME ------
        selected_people_frame = LabelFrame(self, text='selected_people_frame')

        # Top to email frame
        to_email_frame = LabelFrame(selected_people_frame, text='to_email_frame')
        to_email_label = Label(to_email_frame, text='To Email')
        email_send_button = Button(to_email_frame, text='Send')

        to_email_label.grid(row=0, column=0, sticky='w', padx=40, pady=15)
        email_send_button.grid(row=1, column=0, sticky='w', padx=60, pady=15)


        # Bottom selected frame
        email_list_frame = LabelFrame(selected_people_frame, text='email_list_frame')
        
        to_email_frame.grid(row=0, column=0, sticky='nsew')
        email_list_frame.grid(row=1, column=0, sticky='nsew')
        selected_people_frame.grid(row=0, column=1, sticky='nsew')





        # COLUMN 3
        # ------ RIGHTMOST EMAIL TEMPLATE FRAME ------
        email_template_frame = LabelFrame(self, text='email_template_frame')

        # Top selected template frame
        select_template_frame = LabelFrame(email_template_frame, text='select_template_frame')
        select_template_label = Label(select_template_frame, text='Select Template')
        select_template_label.grid(row=0, column=0, sticky='w', padx=40, pady=15)

        
        # Bottom template textbox frame
        template_list_frame = LabelFrame(email_template_frame, text='template_list_frame')

        select_template_frame.grid(row=0, column=0, sticky = 'nsew')
        template_list_frame.grid(row=1, column=0, sticky='nsew')
        email_template_frame.grid(row=0, column=2, sticky='nsew')


if __name__ == '__main__':
    # Start app and start main loop
    app = App()
    app.tk.call('source', 'forest-light.tcl')
    
    s = Style()
    s.theme_use('forest-light')

    app.mainloop()
