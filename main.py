import tkinter as tk
import shelve
from tkinter.messagebox import showinfo
from tkinter import Frame


class User:
    def __init__(self, name=None, age=None, skills=None):
        self.name = name
        self.age = age
        self.skills = skills

    def __str__(self):
        return self.name

class WindowDB(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        self.columns = ['name', 'age', 'skills']
        self.entries = {}

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT)

        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT)

        value_frame = tk.Frame(right_frame)
        value_frame.pack(side=tk.LEFT)

        for row, column in enumerate(['id'] + self.columns):
            label = tk.Label(value_frame, text=column)
            entry = tk.Entry(value_frame)

            label.grid(row=row, column=0)
            entry.grid(row=row, column=1)

            self.entries[column] = entry

        button_frame = tk.Frame(right_frame)
        button_frame.pack(side=tk.RIGHT)

        tk.Button(right_frame, text='Save', command=self.save).pack(side=tk.TOP)
        tk.Button(right_frame, text='Fetch', command=self.fetch).pack(side=tk.TOP)
        tk.Button(right_frame, text='Quit', command=self.quit).pack(side=tk.TOP)

        list_frame = tk.Frame(left_frame)
        list_frame.pack()
        list_box = tk.Listbox(list_frame, width=40, height=10)

        for key in db:
            list_box.insert(0, key)

        list_box.pack()
        self.list_box = list_box

    def save(self):
        key = self.entries['id'].get()

        if key in db:
            record = db[key]
        else:
            record = User()

        for column in self.columns:
            setattr(record, column, str(self.entries[column].get()))

        db[key] = record
        showinfo(title='save result', message='success')

    def fetch(self):
        key = None

        elements = self.list_box.curselection()
        if len(elements):
            key = self.list_box.get(elements[0])

        if not key:
            showinfo(title='key errror', message='key not found')
            return

        record = None
        try:
            record = db[key]
        except KeyError:
            showinfo(title='fetch result', message=f'key {key} not found')

        for column in self.columns:
            if isinstance(record, User):
                value = str(getattr(record, column))
            else:
                value = ''

            self.entries[column].delete(0, tk.END)
            self.entries[column].insert(0, value)

        self.entries['id'].delete(0, tk.END)
        self.entries['id'].insert(0, key)


def show_window():
    app = tk.Tk()
    window = WindowDB(app)
    window.pack()
    app.mainloop()


if __name__ == '__main__':
    db = shelve.open('db')
    show_window()
    db.close()




