import asyncio, tracemalloc

from tkinter import Tk, Text, CENTER, NSEW, LEFT, RIGHT, END, WORD, YES, StringVar
from tkinter.ttk import Label, Frame, Button, Style, LabelFrame, Scrollbar, OptionMenu, PanedWindow
from custom_elements import PlaceholderEntry, SortableTreeview
from get_data import get_logged_in_session, get_data

# The main window of the application
class App(Tk):
    LOGIN_SCREEN = 0
    DATA_VISUALIZATION_SCREEN = 1

    # THe constructor to initialize the window
    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        self.title('TroopWebHost Improvement Project')
        self.geometry('1280x720')
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        # Focus on every object with mouse click (so entry boxes/textboxes can be deselected)
        self.bind_all("<1>", lambda event: event.widget.focus_set())

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # A dict of all the screen objects
        self.screens = {}
        self.screens[App.LOGIN_SCREEN] = LoginScreen(container, controller=self)
        self.screens[App.DATA_VISUALIZATION_SCREEN] = DataVisualizationScreen(container, controller=self, orient='horizontal')

        # Open login screen first
        self.current_screen = App.LOGIN_SCREEN
        self.switch_screen_to(App.LOGIN_SCREEN)

        self.running_tasks = []
        self.loop = loop
        self.updater(0.01)
        # self.running_tasks.append(self.loop.create_task(self.updater(interval=1/120)))

    def updater(self, interval):
        self.update()
        self.loop.call_later(interval, self.updater, interval)

    def create_task(self, task):
        self.running_tasks.append(self.loop.create_task(task))

    # Switch screens
    def switch_screen_to(self, name):
        old_screen = self.screens[self.current_screen]
        old_screen.grid_forget()

        screen = self.screens[name]
        screen.grid(row=0, column=0, sticky='nsew')
        screen.tkraise()
        screen.focus()

        self.current_screen = name


    async def get_data(self, session):
        self.data = await get_data(session)
        print(self.data)


    def close(self):
        for task in self.running_tasks:
            task.cancel()
        self.loop.stop()


# The Frame for the login screen
class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Function to verify login credentials are correct
        async def authenticate(*_):
            username = username_entry.get()
            password = password_entry.get()
            session = await get_logged_in_session(username, password)

            if session is None:  # incorrect username/password
                password_entry.reset()
                error_label.grid(row=3, column=0)
            else:
                controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)
                controller.loop.create_task(controller.get_data(session))


        # Frame to keep login centered in the screen
        center_frame = LabelFrame(self, text='Sign in to TroopWebHost', labelanchor='n')

        # Text and entry boxes for login
        #login_label = Label(center_frame, text='Sign In')
        username_entry = PlaceholderEntry(center_frame, placeholder='Username')
        password_entry = PlaceholderEntry(center_frame, show='*', placeholder='Password')
        error_label = Label(center_frame, text='Incorrect username or password.', style='TLabel')
        login_button = Button(center_frame, text='Login', command=lambda: controller.loop.create_task(authenticate()))

        # Position each element on the screen
        #login_label.grid(row=0, column=0, sticky='nsew', pady=25)
        username_entry.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=2, column=0, padx=10, pady=10)
        login_button.grid(row=4, column=0, pady=10)

        # Make enter key work to press login button
        password_entry.bind('<Return>', authenticate)

        # Place holding frame in the center of the screen
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        

# The data visualization screen, shown after login, holds the three main columns of the application
class DataVisualizationScreen(PanedWindow):
    def __init__(self, parent, controller, *args, **kwargs):
        PanedWindow.__init__(self, parent, *args, **kwargs)
        
        data_visualizer_column = DataVisualizerColumn(self)
        self.add(data_visualizer_column, weight=4)
        selected_emails_column = SelectedEmailsColumn(self)
        self.add(selected_emails_column, weight=1)
        email_template_column = EmailTemplateColumn(self)
        email_login_column = EmailLoginColumn(self, replacement=email_template_column)
        self.add(email_login_column, weight=1)


# Leftmost data visualization column
class DataVisualizerColumn(PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        PanedWindow.__init__(self, parent, *args, **kwargs)
        
        # Top sorting frame
        sorting_frame = Frame(self)
        sort_by_name_button = Button(sorting_frame, text='Sort by Name', command=lambda: chart_treeview.sort_by(0))
        sort_by_name_button.grid(row=0, column=0, sticky=NSEW, padx=8, pady=15)
        sort_by_training_name_button = Button(sorting_frame, text='Sort by Training Name', command=lambda: chart_treeview.sort_by(1))
        sort_by_training_name_button.grid(row=0, column=1, sticky=NSEW, padx=8, pady=15)
        sort_by_expiry_date_button = Button(sorting_frame, text='Sort by Expiry Date', command=lambda: chart_treeview.sort_by(3))
        sort_by_expiry_date_button.grid(row=0, column=2, sticky=NSEW, padx=8, pady=15)
        self.add(sorting_frame, weight=0)

        # Bottom chart frame
        chart_frame = Frame(self)
        # Scroll bar for all the data
        chart_tree_scroll = Scrollbar(chart_frame)
        chart_tree_scroll.pack(side=RIGHT, fill='y')
        columns = {0:'Name', 1:'Email', 2:'Training Name', 3:'Expiry Date'}
        # Chart for all the data
        chart_treeview = SortableTreeview(chart_frame, selectmode='extended', columns=columns,
                                          yscrollcommand=chart_tree_scroll.set)
        # chart_treeview.tag_configure('checked', background='#a0f79c')
        chart_tree_scroll.config(command=chart_treeview.yview)
        contacts = []
        # Fake test data (lorem ipsum to fill the chart)
        for n in range(1, 100):
            contacts.append((f'first {n} last {n}', f'email{n}@a.com', 'YPT', '6/1/23'))
        # Adding each row in the test data to the chart ('' and END just refer to the whole chart)
        for contact in contacts:
            chart_treeview.insert('', END, values=contact, tags=('checked',))
        chart_treeview.column('0', anchor='w', minwidth=120, width=130, stretch=YES)
        chart_treeview.column('1', anchor="w", minwidth=120, width=130, stretch=YES)
        chart_treeview.column('2', anchor="w", minwidth=120, width=130, stretch=YES)
        chart_treeview.column('3', anchor="w", minwidth=120, width=130, stretch=YES)
        chart_treeview.pack(expand=True, fill='both')
        self.add(chart_frame, weight=1)


# Middle selected emails column
class SelectedEmailsColumn(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Scroll bar for the selected list
        selected_tree_scroll = Scrollbar(self)
        selected_tree_scroll.pack(side=RIGHT, fill='y')
        # Chart for the selected people
        selected_treeview = SortableTreeview(self, selectmode='none', columns={0: 'Selected'},
                                             yscrollcommand=selected_tree_scroll.set)
        # selected_treeview.tag_configure('checked', background='#a0f79c')
        selected_tree_scroll.config(command=selected_treeview.yview)
        # Fake test data (lorem ipsum to fill the chart)
        contacts = []
        for n in range(1, 100):
            contacts.append((f'email{n}@a.com',))
        for contact in contacts:
            selected_treeview.insert('', END, values=contact)
        selected_treeview.column('0', anchor='center', minwidth=100, width=120, stretch=YES)
        selected_treeview.pack(expand=True, fill='both')


# Rightmost email template frame
class EmailTemplateColumn(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        # Top selected template frame
        select_template_frame = Frame(self)
        options = ['', 'Default', 'Custom']
        # Dropdown to choose email templates
        select_template_dropdown = OptionMenu(select_template_frame, StringVar(value=options[1]), *options)
        select_template_dropdown.pack(side=LEFT)
        # Button to send the email
        email_send_button = Button(select_template_frame, text='Send Email', style='Accent.TButton')
        email_send_button.pack(side=RIGHT)
        select_template_frame.pack(side='top')

        # Bottom template textbox frame
        template_text_frame = Frame(self)
        # Textbox to hold the email template
        template_text_box = Text(template_text_frame, wrap=WORD, width=50)  # width in characters not pixels
        template_text_box.pack(expand=True, fill='both')
        template_text_frame.pack(side='top', expand=True, fill='both')


# The Frame for the email login screen
class EmailLoginColumn(Frame):
    def __init__(self, parent, replacement, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Function to verify email login credentials are correct
        async def authenticate(*_):
            username = username_entry.get()
            password = password_entry.get()
            if False: #login_failed:
                error_label.grid(row=3, column=0)
            else:
                parent.forget(self)
                parent.add(replacement, weight=1)
            

        # Frame to keep login centered in the screen
        center_frame = LabelFrame(self, text='Sign in to your email', labelanchor='n')

        # Text and entry boxes for login
        #login_label = Label(center_frame, text='Sign In')
        username_entry = PlaceholderEntry(center_frame, placeholder='Username')
        password_entry = PlaceholderEntry(center_frame, show='*', placeholder='Password')
        error_label = Label(center_frame, text='Incorrect username or password.', style='TLabel')
        login_button = Button(center_frame, text='Login', command=lambda: asyncio.run(authenticate()))

        # Position each element on the screen
        #login_label.grid(row=0, column=0, sticky='nsew', pady=25)
        username_entry.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=2, column=0, padx=10, pady=10)
        login_button.grid(row=4, column=0, pady=10)

        # Make enter key work to press login button
        password_entry.bind('<Return>', authenticate)

        # Place holding frame in the center of the screen
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


if __name__ == '__main__':
    # Enable tracemalloc to get object allocation traceback
    tracemalloc.start()

    # Start app and start main loop
    loop = asyncio.get_event_loop()

    app = App(loop)
    app.tk.call('source', 'forest-light.tcl')

    s = Style()
    s.theme_use('forest-light')

    loop.run_forever()
    app.close()
    loop.close()


    # app.mainloop()

