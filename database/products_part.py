try:
    from .database_config import SQLBaseConnect
except ImportError as error:
    from database_config import SQLBaseConnect


class SQLProductsPart(SQLBaseConnect):
    def save_product(self, data: tuple) -> None:
        sql = '''
            INSERT INTO products(image_path, title, price, description, lang, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        image_path, title, price, description, lang, category_id = data
        self.manager(sql, image_path, title, price, description, lang, category_id, commit=True)

    def update_product(self, data: tuple) -> None:
        sql = '''
            UPDATE products SET 
                price = %s
            WHERE title = %s
        '''
        price, title = data

        self.manager(sql, price, title, commit=True)

    def save_category(self, lang: str, category_name: str) -> None:
        sql = '''
            INSERT INTO categories(lang, category_name)
            VALUES (%s, %s)
        '''
        self.manager(sql, lang, category_name, commit=True)

    def show_list_categories(self, lang: str) -> tuple:
        sql = '''
            SELECT category_name FROM categories WHERE lang = %s
        '''
        list_categories = self.manager(sql, lang, fetchall=True)
        return tuple([category[0] for category in list_categories])

    def get_cat_id_for_name(self, cat_name: str) -> int:
        sql = '''
            SELECT category_id FROM categories WHERE category_name = %s
        '''
        cat_id = self.manager(sql, cat_name, fetchone=True)
        return cat_id

    def show_list_products(self, cat_id: int, lang: str) -> tuple:
        sql = '''
            SELECT title FROM products WHERE category_id = %s AND lang = %s
        '''
        list_products = self.manager(sql, cat_id, lang, fetchall=True)
        return tuple([product[0] for product in list_products])

    def get_product_info(self, product_name: str) -> tuple:
        sql = '''
            SELECT product_id, image_path, title, price, description, lang, category_id FROM products WHERE title = %s
        '''
        product_info = self.manager(sql, product_name, fetchone=True)
        if product_info is not None:
            return product_info

    def get_product_price(self, product_id: int) -> tuple:
        sql = "SELECT price FROM products WHERE product_id = %s;"
        return self.manager(sql, product_id, fetchone=True)[0]

    def delete_product(self, product_name: str) -> int:
        sql_check_product = 'SELECT * FROM products WHERE title = %s'
        get_product = self.manager(sql_check_product, product_name, fetchone=True)

        if get_product is None:
            return 404
        else:
            sql = 'DELETE FROM products WHERE title = %s'
            self.manager(sql, product_name, commit=True)
