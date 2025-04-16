from db_products import *
from tkinter import *
from tkinter import ttk

class DBWindow():
    window = None
    treeview = None
    def getWindow(self, title):
        if self.window != None:
            return self
        self.window = Tk()
        self.window.title(title)
        # window.geometry("400x300")
        # window.resizeble(False, False)


        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        return self

    def insertBasicFrames(self, controller):
        self.insertProductsFrame()
        self.insertButtonFrame(controller)
        return self

    def insertProductsFrame(self, controller):
        self.treeview = WindowConstructor().add_productsframe(self.window)
        return self

    def insertButtonFrame(self, controller):
        WindowConstructor().add_buttonframe(self.window, controller)
        return self

    def runWindow(self):
        self.window.mainloop()
        return self

class WindowConstructor():
    def create_button(self, text, column, frame, command):
        button = ttk.Button(frame, text=text, command=command)
        button.grid(row=0,
                           column=column,
                           ipady=2, pady=10, padx=20, sticky=EW)
        return button


    def add_buttonframe(self, window, controller):
        buttons_frame = Frame(window)
        buttons_frame.grid(row=1, column=0, pady=10, sticky=EW)


        create_button = self.create_button("Добавить запись", 0, buttons_frame, command= lambda: controller.show_dialog("add"))
        update_button = self.create_button("Изменить запись", 1, buttons_frame, command=lambda: controller.show_dialog("edit"))
        delete_button = self.create_button("Удалить запись", 2, buttons_frame, command=controller.delete_product)
        sort_button = self.create_button("Найти товар", 3, buttons_frame, command=controller.search)

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame.grid_columnconfigure(3, weight=1)

    def add_frame(self, window, headings):
        table_frame = Frame(window)

        columns = list(headings.keys())
        table_frame.grid(row=0, column=0, sticky=NSEW)

        vertical_scrollbar = Scrollbar(table_frame, orient="vertical")
        vertical_scrollbar.grid(row=0, column=1, sticky=NS)

        treeview = ttk.Treeview(table_frame, columns=columns, show='headings',
                                         yscrollcommand=vertical_scrollbar.set)
        vertical_scrollbar.config(command=treeview.yview)

        for key, value in headings.items():
            treeview.heading(key, text=value)
        treeview.column('ID', width=0, stretch=NO)
        treeview.grid(row=0, column=0, sticky=NSEW)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        return treeview

    def add_productsframe(self, window):
        products_headings = {
            'ID': 'Идентификатор',
            'NAME_PRODUCT': 'Наименование',
            'DATE_SELL': 'Дата продажи',
            'PRICE': 'Цена',
            'AMOUNT': 'Кол-во',
            'ID_CATEGORY': 'Категория'
        }

        return self.add_frame(window, products_headings)