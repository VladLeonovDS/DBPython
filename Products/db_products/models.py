from db_connection.connection import BaseDBView, fdb


class Category(BaseDBView):
    def get_all_categories(self):
        self.connector.cursor.execute('''
            SELECT *
            FROM product_category
            ''')
        result = self.connector.cursor.fetchall()
        self.connector.cursor.close()
        return result

class Product(BaseDBView):
    def get_all_products(self):
        self.connector.cursor.execute('''
            SELECT
        P.ID,
        P.NAME_PRODUCT,
        P.DATE_SELL,
        P.PRICE,
        P.AMOUNT,
        PC.CATEGORY_NAME
        FROM
        PRODUCTS
        P
        LEFT
        JOIN
        PRODUCT_CATEGORY
        PC
        ON
        PC.ID = P.ID_CATEGORY ORDER BY NAME_PRODUCT
        ''')
        result = self.connector.cursor.fetchall()
        self.connector.cursor.close()
        return result
    def get_product_by_id(self, product_id):
        self.connector.cursor.execute('''
            SELECT
        P.ID,
        P.NAME_PRODUCT,
        P.PRICE,
        P.AMOUNT,
        P.ID_CATEGORY,
        PC.CATEGORY_NAME,
        P.DATE_SELL
        FROM
        PRODUCTS
        P
        LEFT
        JOIN
        PRODUCT_CATEGORY
        PC
        ON
        PC.ID = P.ID_CATEGORY
        WHERE
        P.ID = ?''',
        (product_id,))
        result = self.connector.cursor.fetchone()
        self.connector.cursor.close()
        return result
    def create_product(self, product_name, category_id, price, date, amount):
        try:
            self.connector.cursor.execute('''
            INSERT INTO PRODUCTS (NAME_PRODUCT, AMOUNT, PRICE, ID_CATEGORY, DATE_SELL) VALUES (?,?,?,?,?)
        ''', (product_name, amount, price, category_id, date))
            self.connector.dataset.commit()
            return True
        except fdb.Error as e:
            print(f"Ошибка: ", e)
    def update_product(self, id, product_name, category_id, price, date, amount):
        try:
            self.connector.cursor.execute('''
            UPDATE PRODUCTS SET NAME_PRODUCT = ?, ID_CATEGORY = ?, PRICE = ?, AMOUNT = ?, DATE_SELL = ? WHERE ID = ?
        ''', (product_name, category_id, price, amount, date, id))
            self.connector.dataset.commit()
            return True
        except fdb.Error as e:
            print(f"Ошибка: ", e)
    def delete_product(self, id):
        try:
            self.connector.cursor.execute('''
            DELETE FROM PRODUCTS WHERE ID = ?
        ''', (id, ))
            self.connector.dataset.commit()
            return True
        except fdb.Error as e:
            print(f"Ошибка: ", e)
