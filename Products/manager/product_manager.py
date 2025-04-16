import datetime
from dotenv import load_dotenv
load_dotenv()
from db_products.models import Product, Category
from factory.widget_factory import DBWindow
from tkinter import *
from tkinter import messagebox
from datetime import *
from decimal import Decimal
from tkcalendar import DateEntry


def create_dialog_window(action):
    dialog = Toplevel()
    dialog.title('Добавление записи' if action == 'add' else "Изменить запись")
    dialog.grab_set()

    return dialog

class ProductDatabaseManager():
    Window = None
    ProductInterface = Product()
    def __init__(self):
        self.selected_id = None
        self.startLoop()
    def startLoop(self):
        self.Window = (DBWindow()
         .getWindow("Учёт товаров в магазине")
         .insertButtonFrame(self)
         .insertProductsFrame(self))
         # .insertBasicFrames())

    def delete_product(self):
        if not self.selected_id:
            messagebox.showwarning("Ошибка, продукт не выбран")
            return
        if messagebox.askyesno("Удалить?"):
            self.ProductInterface.delete_product(self.selected_id)
            self.refreshcb(self.Window)
            return

    def registerEvents(self):
        self.Window.treeview.bind("<<TreeviewSelect>>", self.on_select)


    def on_select(self, event):
        selected = self.Window.treeview.selection()
        if selected:
            self.set_selected(self.Window.treeview.item(selected[0])['values'][0])

    def initRefresh(self):
        self.refreshcallback = self.refreshcb(self.Window)

    def set_selected(self, product_id):
        self.selected_id = product_id
        print(product_id)

    def get_products(self):
        return self.ProductInterface.get_all_products()

    def show_dialog(self, action):
        if action == 'edit' and not self.selected_id:
            messagebox.showwarning("Ошибка", "Выберите запись для редактирования")
            return

        dialog = create_dialog_window(action)

        FIELDS =  [
            ("Наименование", "entry"),
            ("Цена", "entry"),
            ("Количество", "entry"),
            ("Категория", "combobox", Category().get_all_categories()),
            ("Дата продажи", "date")
        ]

        initial_data = None

        if action == 'edit' and self.selected_id:
            initial_data = Product().get_product_by_id(self.selected_id)

        entries = self.create_form_fields(dialog, FIELDS, initial_data)

        ttk.Button(dialog, text="Сохранить", command=lambda: self.save_action(dialog, entries, action)).grid(row=6,
                                                                                                             columnspan=2,
                                                                                                             sticky="ew",
                                                                                                             padx=5,
                                                                                                             pady=5)
    def get_form_date(self, entries):
        return {
            "product_name": entries["Наименование"].get(),
            "price": entries["Цена"].get(),
            "amount": entries["Количество"].get(),
            "category_id": entries["Категория"].get().split()[0],
            "date": entries["Дата продажи"].get_date().strftime("%d.%m.%Y")
        }

    def save_action(self, dialog, entries, action):
        data = self.get_form_date(entries)

        try:
            if action == 'add':
                Product().create_product(**data)
                messagebox.showinfo("Успех", "Товар успешно добавлен")
            else:
                Product().update_product(self.selected_id, **data)
                messagebox.showinfo("Успех", "Изменения сохранены")

            dialog.destroy()
            self.refreshcb(self.Window)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")


    def search(self):
        dialog = Toplevel()
        dialog.title("Поиск товара")
        dialog.grab_set()

        entry = ttk.Entry(dialog)
        entry.insert(0, "Наименование")
        entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(dialog, text="Сохранить", command=self.printsearch(entry, self.Window)).grid(row=6,
                                                                                                             columnspan=2,
                                                                                                             sticky="ew",
                                                                                                             padx=5,
                                                                                                             pady=5)



    def printsearch(self, str, window):

        for product in self.get_products():
            try:
                formatted_values = []
                for value in product:
                    if not str in value:
                        continue
                    if isinstance(value, date):
                        formatted_values.append(value.strftime("%d.%m.%Y"))
                    elif isinstance(value, Decimal):
                        formatted_values.append(str(value) + 'руб.')
                    else:
                        formatted_values.append(value)
                window.treeview.insert("", 0, values=formatted_values)
            except Exception as e:
                print("Ошибка: ", e)


    def create_form_fields(self, dialog, fields_config, initial_data=None):
        entries = {}

        for i, (field_name, field_type, *extra) in enumerate(fields_config):
            ttk.Label(dialog, text=field_name).grid(row=i, column=0, padx=5, pady=5, sticky=W)
            if field_type == "entry":
                entry = ttk.Entry(dialog)
                if initial_data:
                    entry.insert(0, initial_data[i + 1])

            elif field_type == "combobox":
                entry = ttk.Combobox(dialog, values=extra[0], state="readonly", width=17)
                if initial_data:
                    entry.set(f"{initial_data[4]} {initial_data[5]}")

            elif field_type == "date":
                entry = DateEntry(dialog, date_pattern="dd.mm.yyyy", width=17)
                if initial_data:
                    entry.set_date(initial_data[6])
                else:
                    entry.set_date(date.today())

            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field_name] = entry

        return entries

    def refreshcb(self, window):
        for product in self.get_products():
            try:
                formatted_values = []
                for value in product:
                    if isinstance(value, date):
                        formatted_values.append(value.strftime("%d.%m.%Y"))
                    elif isinstance(value, Decimal):
                        formatted_values.append(str(value) + 'руб.')
                    else:
                        formatted_values.append(value)
                window.treeview.insert("", 0, values=formatted_values)
            except Exception as e:
                print("Ошибка: ", e)
