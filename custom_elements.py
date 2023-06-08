from tkinter import END
from tkinter.ttk import Entry, Treeview
from datetime import datetime


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
    def __init__(self, master=None, columns={}, show='headings', *args, **kwargs):
        super().__init__(master, columns=columns.keys(), *args, **kwargs)
        self.col_names = columns
        self['show'] = show
        # Sort by increasing order on first click
        for col in columns:
            self.heading(col, text=self.col_names[col], command=lambda col_copy=col: self.sort_by(
                col_copy, reverse=False), anchor='center')

    # Sort chart by a specific column
    def sort_by(self, col, reverse=False):
        # Get and sort specific column, keeping track of which row each item was originally in
        column = [(iid, self.set(iid, col)) for iid in self.get_children()]
        def normal_key(x): return x[1].lower()
        if reverse:
            # Sort by date (latest to earliest), setting people without a date to a date far in the past so they show up at the bottom
            def dates_key(d): return datetime.strptime(
                '12/22/1900' if not d[1] else d[1], r'%m/%d/%Y')
        else:
            # Sort by date (earliest to latest), setting people without a date to a date far in the future
            def dates_key(d): return datetime.strptime(
                '12/22/2050' if not d[1] else d[1], r'%m/%d/%Y')
        column_is_date = self.col_names[col] == 'Expiry Date'
        # Sort by normal key if column is not a date, else sort by the date key
        column.sort(reverse=reverse,
                    key=dates_key if column_is_date else normal_key)

        # Rearrange original rows in the chart based on sort
        for i, (iid, value) in enumerate(column):
            self.move(iid, parent='', index=i)

        # Set sort command to sort other way on next click
        self.heading(col, text=self.col_names[col], command=lambda col_copy=col: self.sort_by(
            col_copy, not reverse), anchor='center')


# Custom class to create checkable rows in a Treeview
class CheckableSortableTreeview(SortableTreeview):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.selected = set()

        self.tag_configure('checked', background='#a0f79c')
        self.tag_configure('unchecked', background='#eeeeee')

    # Uncheck row with item
    def check_row(self, item):
        self.item(item, tags=("checked",))

    # Check row with item
    def uncheck_row(self, item):
        self.item(item, tags=("unchecked",))

    # Get currently selected items in the chart (as item objects)
    def get_selected_items(self):
        self.update()
        return self.selection()

    # Get currently selected items in the chart (as email strings)
    def get_selected_items_email(self):
        selected_items = self.selected
        emails = []
        for item in selected_items:
            # Get email
            email = self.item(item)['values'][3]
            emails.append(email)
        return list(set(emails))

    # Add selected items in the chart
    def add_selected(self):
        selected_items = self.selection()
        for item in selected_items:
            self.selected.add(item)

    # Remove selected items from the chart
    def remove_selected(self, all=False):
        selected_items = self.get_children() if all else self.selection()
        for item in selected_items:
            if item in self.selected:
                self.selected.remove(item)

    # Highlight selected items in chart
    def color_selected(self):
        selected_items = self.selected
        for item in self.get_children():
            if item in selected_items:
                self.check_row(item)
            else:
                self.uncheck_row(item)
