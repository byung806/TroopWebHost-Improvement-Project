from tkinter import Tk, Text, CENTER, NSEW, RIGHT, END, WORD, StringVar
from tkinter.ttk import Label, Frame, Button, Style, LabelFrame, Treeview, Scrollbar, Separator, OptionMenu
from custom_elements import PlaceholderEntry
from get_data import get_logged_in_session, get_data


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
        self.geometry('1280x720')
        
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


    def get_data(self, session):
        self.data = get_data(session)


# The Frame for the login screen
class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Function to verify login credentials are correct
        def authenticate(*_):
            #TODO: add actual verification
            username = username_entry.get()
            password = password_entry.get()
            session = get_logged_in_session(username, password)
            if session is None:  # incorrect username/password
                password_entry.reset()
                error_label.grid(row=3, column=0)
            else:
                controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)
                controller.get_data(session)


        # Frame to keep login centered in the screen
        center_frame = LabelFrame(self, text='Sign In', labelanchor='n', style='A.TLabelframe')

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
        data_visualizer_frame = Frame(self, padding=10)

        # Top sorting frame
        sorting_frame = Frame(data_visualizer_frame)
        sort_by_name_button = Button(sorting_frame, text='Sort by Name')
        sort_by_name_button.grid(row=0, column=0, sticky=NSEW, padx=8, pady=15)
        sort_by_training_name_button = Button(sorting_frame, text='Sort by Training Name')
        sort_by_training_name_button.grid(row=0, column=1, sticky=NSEW, padx=8, pady=15)
        sort_by_expiry_date_button = Button(sorting_frame, text='Sort by Expiry Date')
        sort_by_expiry_date_button.grid(row=0, column=2, sticky=NSEW, padx=8, pady=15)

        # Bottom chart frame
        chart_frame = Frame(data_visualizer_frame)

        chart_tree_scroll = Scrollbar(chart_frame)
        chart_tree_scroll.pack(side=RIGHT, fill='y')
        chart_treeview = Treeview(chart_frame, selectmode='extended', columns=(0,1,2,3), yscrollcommand=chart_tree_scroll.set)
        # chart_treeview.tag_configure('checked', background='#a0f79c')
        chart_treeview['show'] = 'headings'
        chart_treeview.heading('0', text='Name', anchor='center')
        chart_treeview.heading('1', text='Email', anchor='center')
        chart_treeview.heading('2', text='Training Name', anchor='center')
        chart_treeview.heading('3', text='Expiry Date', anchor='center')
        chart_tree_scroll.config(command=chart_treeview.yview)
        contacts = []
        # Making test data
        for n in range(1, 100):
            contacts.append((f'first {n} last {n}', f'email{n}@a.com', 'YPT', '6/1/23'))
        # Adding each row in the test data to the chart ('' and END just refer to the whole chart)
        for contact in contacts:
            chart_treeview.insert('', END, values=contact, tags=('checked',))
        chart_treeview.column('0', anchor='w', width=120)
        chart_treeview.column('1', anchor="w", width=120)
        chart_treeview.column('2', anchor="w", width=120)
        chart_treeview.column('3', anchor="w", width=120)
        chart_treeview.pack(expand=True, fill='both')

        # Place frames on screen (They initially have 0 width but expand if there are components inside)
        sorting_frame.grid(row=0, column=0, sticky = NSEW)
        chart_frame.grid(row=1, column=0, sticky = NSEW)
        data_visualizer_frame.grid(row=0, column=0, sticky=NSEW)



        separator1 = Separator(self)
        separator1.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="ns")



        # COLUMN 2
        # ------ MIDDLE SELECTED PEOPLE FRAME ------
        selected_people_frame = Frame(self, padding=10)

        # Top to email frame
        to_email_frame = Frame(selected_people_frame)
        email_send_button = Button(to_email_frame, text='Send Email')
        email_send_button.grid(row=1, column=0, sticky='w', pady=15)

        # Bottom selected frame
        email_list_frame = Frame(selected_people_frame)

        selected_tree_scroll = Scrollbar(email_list_frame)
        selected_tree_scroll.pack(side=RIGHT, fill='y')
        selected_treeview = Treeview(email_list_frame, selectmode='extended', columns=(0,), yscrollcommand=selected_tree_scroll.set)
        # selected_treeview.tag_configure('checked', background='#a0f79c')
        selected_treeview['show'] = 'headings'
        selected_treeview.heading('0', text='Selected', anchor='center')
        selected_tree_scroll.config(command=selected_treeview.yview)
        contacts = []
        for n in range(1, 100):
            contacts.append((f'email{n}@a.com',))
        for contact in contacts:
            selected_treeview.insert('', END, values=contact)
        selected_treeview.column('0', anchor='w', width=160)
        selected_treeview.pack(expand=True, fill='both')
        
        to_email_frame.grid(row=0, column=0, sticky='nsew')
        email_list_frame.grid(row=1, column=0, sticky='nsew')
        selected_people_frame.grid(row=0, column=2, sticky='nsew')



        separator2 = Separator(self)
        separator2.grid(row=0, column=3, padx=(10, 10), pady=10, sticky="ns")



        # COLUMN 3
        # ------ RIGHTMOST EMAIL TEMPLATE FRAME ------
        email_template_frame = Frame(self, padding=10)

        # Top selected template frame
        select_template_frame = Frame(email_template_frame)
        options = ['Default']
        select_template_dropdown = OptionMenu(select_template_frame, StringVar(value=options[0]), *options)
        select_template_dropdown.grid(row=0, column=0, sticky='w', pady=15)

        # Bottom template textbox frame
        template_text_frame = Frame(email_template_frame)
        selected_tree_scroll = Scrollbar(email_list_frame)
        selected_tree_scroll.pack(side=RIGHT, fill='y')
        template_text_box = Text(template_text_frame, wrap=WORD, width=50)  # width in characters not pixels
        template_text_box.pack(expand=True, fill='both')


        select_template_frame.grid(row=0, column=0, sticky = 'nsew')
        template_text_frame.grid(row=1, column=0, sticky='nsew')
        email_template_frame.grid(row=0, column=4, sticky='nsew')


if __name__ == '__main__':
    # Start app and start main loop
    app = App()
    app.tk.call('source', 'forest-light.tcl')
    
    s = Style()
    s.theme_use('forest-light')
    s.configure('A.TLabelframe', foreground='yellow')

    app.mainloop()
