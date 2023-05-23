from tkinter import Label, Tk, Frame, Entry, Button

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.title('TroopWebHost Improvement Project')

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.screens = {}
        login_frame = LoginScreen(container)
    
    def show_screen(self, name):
        screen = self.screens[name]
        screen.tkraise()


class LoginScreen(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        login_label = Label(self, text='Sign In', fg='#57a1f8', bg='white')
        username_label = Label(self, text='Username', fg='#57a1f8', bg='white')
        username_entry = Entry(self)
        password_label = Label(self, text='Password', fg='#57a1f8', bg='white')
        password_entry = Entry(self, show='*')
        login_button = Button(self, text='Login', fg='#57a1f8', bg='white', command=authenticate)
    
    def authenticate():
        pass

app = App()
app.mainloop()
