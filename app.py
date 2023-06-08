from tkinter import Tk, Text, CENTER, LEFT, RIGHT, TOP, END, WORD, YES, HORIZONTAL, VERTICAL, BOTH, StringVar, PanedWindow
from tkinter.ttk import Label, Frame, Button, Style, LabelFrame, Scrollbar, OptionMenu, Separator
from custom_elements import PlaceholderEntry, SortableTreeview, CheckableSortableTreeview, PlaceholderTextbox
from get_data import get_logged_in_session, get_data
from send_email import send_email
import json

# The main window of the application


class App(Tk):
    LOGIN_SCREEN = 0
    DATA_VISUALIZATION_SCREEN = 1

    # THe constructor to initialize the window
    def __init__(self, default_width, default_height, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        self.title('TroopWebHost Improvement Project')

        # Center app when opened
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (default_width/2)
        y = (screen_height/2) - (default_height/2)

        self.geometry('1280x720+%d+%d' % (x, y))
        self.minsize(1050, 600)

        # Focus on every object with mouse click (so entry boxes/textboxes can be deselected)
        self.bind_all("<1>", lambda event: event.widget.focus_set())

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # A dict of all the screen objects
        self.screens = {}
        self.screens[App.LOGIN_SCREEN] = LoginScreen(
            container, controller=self)
        self.screens[App.DATA_VISUALIZATION_SCREEN] = DataVisualizationScreen(
            container, controller=self, orient='horizontal')

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

    # Request and parse data from TroopWebHost
    def get_data(self, session):
        self.screens[App.DATA_VISUALIZATION_SCREEN].get_data(session)


# The Frame for the login screen
class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Function to verify login credentials are correct
        def authenticate(*_):
            username = username_entry.get()
            password = password_entry.get()
            session = get_logged_in_session(username, password)
            if session is None:  # incorrect username/password
                password_entry.reset_with_focus()
                error_label.grid(row=3, column=0)
                error_label.after(3000, lambda *_: error_label.grid_forget())
            else:
                controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)
                controller.get_data(session)

        # Frame to keep login centered in the screen
        center_frame = LabelFrame(
            self, text='Sign in to TroopWebHost', labelanchor='n')

        # Text and entry boxes for login
        # login_label = Label(center_frame, text='Sign In')
        username_entry = PlaceholderEntry(center_frame, placeholder='Username')
        password_entry = PlaceholderEntry(
            center_frame, show='*', placeholder='Password')
        error_label = Label(
            center_frame, text='Incorrect username or password.', style='TLabel')
        login_button = Button(center_frame, text='Login', command=authenticate)

        # Position each element on the screen
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
        self.controller = controller
        # Set data to empty until it can be filled with updated data
        self.data = []
        # List of all emails currently in the selected emails list
        self.selected = []

        min_sizes = [500, 130, 400]

        self.data_visualizer_column = DataVisualizerColumn(self)
        self.add(self.data_visualizer_column, minsize=min_sizes[0])
        self.selected_emails_column = SelectedEmailsColumn(self)
        self.add(self.selected_emails_column, minsize=min_sizes[1])
        self.email_template_column = EmailTemplateColumn(self)
        self.add(self.email_template_column, minsize=min_sizes[2])

    # Request and parse data from TroopWebHost
    def get_data(self, session):
        self.data = get_data(session)
        self.data_visualizer_column.update_chart(self.data)

    def add_selected(self):
        self.data_visualizer_column.chart_treeview.add_selected()
        self.selected = self.data_visualizer_column.chart_treeview.get_selected_items_email()
        self.selected_emails_column.update_selected(self.selected)
        self.data_visualizer_column.chart_treeview.color_selected()

    def remove_selected(self):
        self.data_visualizer_column.chart_treeview.remove_selected()
        self.selected = self.data_visualizer_column.chart_treeview.get_selected_items_email()
        self.selected_emails_column.update_selected(self.selected)
        self.data_visualizer_column.chart_treeview.color_selected()

    def remove_all_selected(self):
        self.data_visualizer_column.chart_treeview.remove_selected(all=True)
        self.selected.clear()
        self.selected_emails_column.update_selected(self.selected)
        self.data_visualizer_column.chart_treeview.color_selected()


# Leftmost data visualization column
class DataVisualizerColumn(PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        PanedWindow.__init__(self, parent, orient=VERTICAL, *args, **kwargs)

        # Top sorting frame
        sorting_frame = Frame(self)
        add_selected_button = Button(sorting_frame, text='Add Selected to Recipients',
                                     command=lambda: parent.add_selected(), style='Accent.TButton')
        add_selected_button.pack(padx=8, pady=8, side='left')
        remove_selected_button = Button(sorting_frame, text='Remove Selected from Recipients',
                                        command=lambda: parent.remove_selected(), style='Accent.TButton')
        remove_selected_button.pack(padx=8, pady=8, side='left')
        deselect_all_button = Button(sorting_frame, text='Remove All Recipients',
                                     command=lambda: parent.remove_all_selected(), style='TButton')
        deselect_all_button.pack(padx=8, pady=8, side='right')
        self.add(sorting_frame)

        # Bottom chart frame
        chart_frame = Frame(self)
        # Scroll bar for all the data
        chart_tree_scroll = Scrollbar(chart_frame)
        chart_tree_scroll.pack(side=RIGHT, fill='y')
        columns = {0: 'Name', 1: 'Training Name', 2: 'Expiry Date', 3: 'Email'}
        # Chart for all the data
        self.chart_treeview = CheckableSortableTreeview(chart_frame, selectmode='extended', columns=columns,
                                                        yscrollcommand=chart_tree_scroll.set)
        chart_tree_scroll.config(command=self.chart_treeview.yview)
        self.update_chart(parent.data)
        self.chart_treeview.column(
            '0', anchor='w', minwidth=120, width=160, stretch=YES)
        self.chart_treeview.column(
            '1', anchor="w", minwidth=120, width=160, stretch=YES)
        self.chart_treeview.column(
            '2', anchor="w", minwidth=120, width=160, stretch=YES)
        self.chart_treeview.column(
            '3', anchor="w", minwidth=120, width=160, stretch=YES)
        self.chart_treeview.pack(expand=True, fill='both')
        self.add(chart_frame)

    # Update chart once self.data is updated
    def update_chart(self, data):
        # Adding each row in the test data to the chart ('' and END just refer to the whole chart)
        for row in data:
            self.chart_treeview.insert(
                '', END, values=row, tags=('unchecked',))


# Middle selected emails column
class SelectedEmailsColumn(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Scroll bar for the selected list
        selected_tree_scroll = Scrollbar(self)
        selected_tree_scroll.pack(side=RIGHT, fill='y')
        # Chart for the selected people
        self.selected_treeview = SortableTreeview(self, selectmode='none', columns={0: 'Email Recipients'},
                                                  yscrollcommand=selected_tree_scroll.set)
        # selected_treeview.tag_configure('checked', background='#a0f79c')
        selected_tree_scroll.config(command=self.selected_treeview.yview)
        self.selected_treeview.column(
            '0', anchor='center', minwidth=100, width=120)
        self.selected_treeview.pack(expand=True, fill='both')

    # Update selected chart after select or deselect
    def update_selected(self, data):
        for item in self.selected_treeview.get_children():
            self.selected_treeview.delete(item)
        # Adding each row in the test data to the chart ('' and END just refer to the whole chart)
        for row in data:
            self.selected_treeview.insert(
                '', END, values=row, tags=('unchecked',))


# Rightmost email template frame
class EmailTemplateColumn(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent_widget = parent

        self.templates = dict()

        # Top error message / success message
        self.top_label = Label(self)
        self.top_label.bind('<Configure>', lambda _: self.top_label.config(wraplength=self.top_label.winfo_width()))

        # Login frame
        self.login_to_email_frame = Frame(self)
        self.email_to_use = PlaceholderEntry(self.login_to_email_frame, placeholder='Sender Email')
        self.email_to_use.pack(padx=8, pady=8, side=LEFT, expand=True)
        self.passw_to_use = PlaceholderEntry(self.login_to_email_frame, placeholder='Email Password', show='*')
        self.passw_to_use.pack(padx=8, pady=8, side=RIGHT, expand=True)
        self.login_to_email_frame.pack(side=TOP, fill='x')

        # Separator
        self.separator = Separator(self, orient=HORIZONTAL)
        self.separator.pack(fill='x', pady=8)

        # Template dropdown
        self.select_template_dropdown = OptionMenu(self, '')
        self.select_template_dropdown.pack(padx=8, pady=8, side=TOP, fill='x')

        # Label about editing loaded template
        self.disclaimer_label = Label(self, text='Editing the subject or message loaded from a template will not change the template.')
        self.disclaimer_label.bind('<Configure>', lambda _: self.disclaimer_label.config(wraplength=self.disclaimer_label.winfo_width()))
        self.disclaimer_label.pack(padx=8, pady=8, side=TOP, fill='x')

        # Subject & send email frame
        self.subject_send_email_frame = Frame(self)
        self.email_send_button = Button(self.subject_send_email_frame, text='Send Email', style='Accent.TButton', command=self.send_email)
        self.email_send_button.pack(padx=8, pady=8, side=RIGHT)
        self.subject_entry = PlaceholderEntry(self.subject_send_email_frame, placeholder='Subject')
        self.subject_entry.pack(padx=8, pady=8, side=LEFT, expand=True, fill='x', before=self.email_send_button)
        self.subject_send_email_frame.pack(side=TOP, fill='x')

        # Email body
        self.template_text_box = PlaceholderTextbox(self, placeholder='Type your message here...', wrap=WORD, width=50, borderwidth=5)
        self.template_text_box.pack(padx=8, pady=8, side=TOP, expand=True, fill=BOTH)

        # Fill in template dropdown & text box from json
        self.update_templates_from_json()

    # Attempt to send email (returns True if success and False otherwise)
    def send_email(self, *_):
        email, password = self.email_to_use.get(), self.passw_to_use.get()
        recipients = self.parent_widget.selected
        subject = self.subject_entry.get()
        body = self.template_text_box.get()
        
        # Try to send email
        success = send_email(email, password, recipients, subject, body)
        if success:
            self.top_label.config(text=f'Success! Email sent to {len(recipients)} recipients.')
        else:
            self.top_label.config(text='Email failed to send. Make sure you\'re connected to the internet, have at least 1 recipient selected, and your password is your app password, not your normal password.')
            self.passw_to_use.reset_with_focus()

        # Make label appear
        self.top_label.pack(padx=8, pady=8, side=TOP, before=self.login_to_email_frame, fill='x')
        # Make label disappear after 5 seconds
        self.top_label.after(20000, lambda *_: self.top_label.pack_forget())

    # Called when user changes to a different template (new_template is name of template)
    def on_template_change(self, new_template):
        template_dict = self.templates[new_template]

        subject = template_dict['subject']
        self.subject_entry.clear_placeholder()
        self.subject_entry.insert(0, subject)
        if subject == '':
            self.subject_entry.reset_without_focus()

        body = template_dict['body']
        self.template_text_box.clear_placeholder()
        self.template_text_box.insert('1.0', body)
        if body == '':
            self.template_text_box.reset_without_focus()

    # Read from json, then update templates dropdown and textbox
    def update_templates_from_json(self):
        self.templates = self.read_templates_from_json()


        options = list(self.templates.keys())
        # Required empty first option for an OptionMenu
        options.insert(0, '')

        self.select_template_dropdown.pack_forget()
        self.select_template_dropdown = OptionMenu(self, StringVar(value=options[1]), *options, command=self.on_template_change)
        self.select_template_dropdown.pack(padx=8, pady=8, side=TOP, fill='x', after=self.disclaimer_label)

        self.subject_entry.pack_forget()
        self.subject_entry = PlaceholderEntry(self.subject_send_email_frame, placeholder='Subject')
        self.subject_entry.pack(padx=8, pady=8, side=LEFT, expand=True, fill='x', before=self.email_send_button)

        self.on_template_change(options[1])

    # Read templates from json file
    def read_templates_from_json(self):
        return json.load(open('templates.json', 'r'))

    # Save templates to json file
    def save_templates_to_json(self):
        pass


# The Frame for the email login screen
class EmailLoginColumn(Frame):
    def __init__(self, parent, replacement, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Function to verify email login credentials are correct
        def authenticate(*_):
            username = username_entry.get()
            password = password_entry.get()
            if False:  # login_failed:
                error_label.grid(row=3, column=0)
            else:
                parent.forget(self)
                parent.add(replacement, minsize=400)

        # Frame to keep login centered in the screen
        center_frame = LabelFrame(
            self, text='Sign in to your email', labelanchor='n')

        # Text and entry boxes for login
        # login_label = Label(center_frame, text='Sign In')
        username_entry = PlaceholderEntry(center_frame, placeholder='Username')
        password_entry = PlaceholderEntry(
            center_frame, show='*', placeholder='Password')
        error_label = Label(
            center_frame, text='Incorrect username or password.', style='TLabel')
        login_button = Button(center_frame, text='Login', command=authenticate)

        # Position each element on the screen
        # login_label.grid(row=0, column=0, sticky='nsew', pady=25)
        username_entry.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=2, column=0, padx=10, pady=10)
        login_button.grid(row=4, column=0, pady=10)

        # Make enter key work to press login button
        password_entry.bind('<Return>', authenticate)

        # Place holding frame in the center of the screen
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


if __name__ == '__main__':
    # Start app and start main loop
    app = App(1280, 720)
    app.tk.call('source', 'forest-light.tcl')

    s = Style()
    s.theme_use('forest-light')

    app.mainloop()
