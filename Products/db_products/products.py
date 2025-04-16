from manager.product_manager import ProductDatabaseManager

if __name__=='__main__':
    Manager = ProductDatabaseManager()
    Manager.initRefresh()
    Manager.registerEvents()
    Manager.Window.runWindow()


# def Product_print(row):
#         product_name = row['name_product']
#         print('Идентификатор: ', row['id'], '\n'
#                                             'Наименование: ', product_name, '\n'
#                                                                             'Дата: ',
#               row['date_sell'].strftime('%d.%m.%Y'), '\n'
#                                                      'Выручка: ', float(row['amount']) * float(row['price']),
#               '\n',
#               '-' * 12)
# prods = Product().get_all_products;
# for row in prods:
#     Product_print(row)
#
# product_name = input('Введите наименование товара: ')
# category_id = input("Введите идентификатор категории товара: ")
# price = input("Введите цену за одну единицу товара: ")
# amount = input("Введите проданное количество товара: ")
#
# Product().create_product(product_name, category_id, price, amount)
#
# id = input("Введите ID: \n")
#
# print(Product().get_product_by_id(id))
#
# product_name = input('Введите наименование товара: \n')
# category_id = input("Введите идентификатор категории товара: \n")
# price = input("Введите цену за одну единицу товара: \n")
# amount = input("Введите проданное количество товара: \n")
#
# Product().update_product(id, product_name, category_id, price, amount)
#
# print(Product().get_product_by_id(id))
#
# Product().delete_product(id)
#
# print(Product().get_product_by_id(id))