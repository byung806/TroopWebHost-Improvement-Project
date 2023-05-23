from tkinter import Label, Tk, Frame, Entry, Button

class App(Tk):
    LOGIN_SCREEN = 0
    DATA_VISUALIZATION_SCREEN = 1


    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        self.title('TroopWebHost Improvement Project')

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.screens = {}
        self.screens[App.LOGIN_SCREEN] = LoginScreen(container, controller=self)
        self.screens[App.DATA_VISUALIZATION_SCREEN] = DataVisualizationScreen(container, controller=self)

        for screen_name in self.screens:
            self.screens[screen_name].grid(row=0, column=0, sticky='nsew')

        self.switch_screen_to(App.LOGIN_SCREEN)

    
    def switch_screen_to(self, name):
        screen = self.screens[name]
        screen.tkraise()


class LoginScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def authenticate():
            username = username_entry.get()
            password = password_entry.get()
            controller.switch_screen_to(App.DATA_VISUALIZATION_SCREEN)

        login_label = Label(self, text='Sign In')
        username_label = Label(self, text='Username')
        username_entry = Entry(self)
        password_label = Label(self, text='Password')
        password_entry = Entry(self, show='*')
        login_button = Button(self, text='Login', command=authenticate)

        login_label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=40)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=1, column=1, pady=20)
        password_label.grid(row=2, column=0)
        password_entry.grid(row=2, column=1, pady=20)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)
        

class DataVisualizationScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        screen_label = Label(self, text='Data Visualization Screen')
        screen_label.pack()
    

app = App()
app.mainloop()
