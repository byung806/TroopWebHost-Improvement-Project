import tkinter as tk
from tkinter import END
from tkinter.ttk import Entry, Treeview


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


    # Resets entry box after a bad password (clears text and sets focus)
    def reset(self, *_):
        self.delete(0, END)
        self.has_content = True
        self.focus_set()


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


# Custom class to create a sortable chart
class SortableTreeview(Treeview):
    def __init__(self, master=None, columns={}, *args, **kwargs):
        super().__init__(master, columns=columns.keys(), *args, **kwargs)
        self.col_names = columns
        # Sort by increasing order on first click
        for col in columns:
            self.heading(col, text=self.col_names[col], command=lambda col_copy=col: self.sort_by(col_copy, reverse=False), anchor='center')


    # Sort chart by a specific column
    def sort_by(self, col, reverse=False):
        # Get and sort specific column, keeping track of which row each item was originally in
        column = [(iid, self.set(iid, col)) for iid in self.get_children()]
        column.sort(reverse=reverse, key=lambda x: x[1])
    
        # Rearrange original rows in the chart based on sort
        for i, (iid, value) in enumerate(column):
            self.move(iid, parent='', index=i)

        # Set sort command to sort other way on next click
        self.heading(col, text=self.col_names[col], command=lambda col_copy=col: self.sort_by(col_copy, not reverse), anchor='center')
        