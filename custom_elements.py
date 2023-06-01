import tkinter as tk
from tkinter import END
from tkinter.ttk import Entry


# Custom class to create entry boxes with a placeholder
class PlaceholderEntry(Entry):
    def __init__(self, master=None, show='', placeholder='', fg='black', placeholder_color='grey50', style='', *args, **kwargs):
        super().__init__(master, show=show, style=style, *args, **kwargs)
        self.placeholder = placeholder
        self.fg = fg
        self.placeholder_color = placeholder_color
        self.has_content = False
        self.show_original = show
        self.bind('<FocusIn>', self.clear_placeholder)
        self.bind('<FocusOut>', self.fill_placeholder)
        self.fill_placeholder()


    # Clears placeholder text in entry, called when user clicks into entry box
    def clear_placeholder(self, *_):
        if not self.has_content:
            self.has_content = True
            self.config(foreground=self.fg)
            self.config(show=self.show_original)
            self.delete(0, END)


    # Fills placeholder text in entry, called when user clicks out of entry & box is empty
    def fill_placeholder(self, *_):
        if super().get() == '':
            self.insert(0, self.placeholder)
            self.config(foreground=self.placeholder_color)
            self.config(show='')
            self.has_content = False


    # Override original get function to return '' when there's a placeholder
    def get(self):
        content = super().get()
        if self.has_content:
            return content
        return ''
