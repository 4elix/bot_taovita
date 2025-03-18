import datetime

try:
    from .database_config import SQLBaseConnect
except ImportError as error:
    from database_config import SQLBaseConnect


class SQLCartsPart(SQLBaseConnect):
    def get_cart_info(self, user_id: int) -> tuple:
        sql = '''
               SELECT total_price, total_quantity FROM cart
               WHERE user_id = %s
           '''
        return self.manager(sql, user_id, fetchone=True)

    def add_cart_user_id(self, user_id: int) -> None:
        sql = '''
            INSERT INTO cart (user_id) 
            VALUES (%s) 
            ON CONFLICT (user_id) DO NOTHING;
        '''
        self.manager(sql, user_id, commit=True)

    def get_cart_id(self, user_id: int) -> int:
        sql = 'SELECT cart_id FROM cart WHERE user_id = %s;'
        return self.manager(sql, user_id, fetchone=True)[0]

    def clear_cart(self, cart_id: int) -> None:
        sql = '''
            UPDATE products p
            SET quantity = quantity + (
                SELECT cp.quantity FROM cart_products cp
                WHERE cp.product_id = p.product_id AND cp.cart_id = %s
            )
            WHERE EXISTS (
                SELECT 1 FROM cart_products cp WHERE cp.product_id = p.product_id AND cp.cart_id = %s
            );
            
            DELETE FROM cart_products WHERE cart_id = %s;
            
            UPDATE cart 
            SET total_price = 0, total_quantity = 0
            WHERE cart_id = %s;
        '''
        self.manager(sql, cart_id, cart_id, cart_id, cart_id, commit=True)

    def show_cart_items(self, cart_id: int) -> tuple:
        sql = '''
            SELECT title, cart_products.quantity, cart_products.price FROM cart_products
            JOIN products USING(product_id) WHERE cart_id = %s;
        '''
        return self.manager(sql, cart_id, fetchall=True)

    def add_or_update_to_cart(self, cart_id: int, product_id: int, price: int, quantity: int) -> None:
        cursor = self.database.cursor()
        cursor.execute('''
            INSERT INTO cart_products(cart_id, product_id, price, quantity)
            VALUES( %(cart_id)s, %(product_id)s, %(price)s, %(quantity)s )
            ON CONFLICT (cart_id, product_id) DO UPDATE
            SET price = cart_products.price + %(price)s,
            quantity = %(quantity)s
            WHERE cart_products.cart_id = %(cart_id)s
            AND cart_products.product_id = %(product_id)s;

            UPDATE cart SET
                total_price = info.total_price,
                total_quantity = info.total_quantity
                FROM (
                    SELECT 
                        SUM(quantity) AS total_quantity,
                        SUM(price * quantity) AS total_price
                    FROM cart_products WHERE cart_id = %(cart_id)s
                ) AS info
                WHERE cart.cart_id = %(cart_id)s;
                
            UPDATE products SET
                quantity = quantity - %(quantity)s
            WHERE product_id = %(product_id)s;
        ''', {
            'cart_id': cart_id,
            'product_id': product_id,
            'price': price,
            'quantity': quantity
        })
        self.database.commit()

    def add_shipping_address(self, user_id: int, cart_id: int, shipping_address: str, sub_phone_number: str) -> None:
        sql = '''
            INSERT INTO shipping(user_id, cart_id, shipping_address, sub_phone_number)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, cart_id)
            DO UPDATE SET
                shipping_address = EXCLUDED.shipping_address, 
                sub_phone_number = EXCLUDED.sub_phone_number;
        '''
        self.manager(sql, user_id, cart_id, shipping_address, sub_phone_number, commit=True)

    def get_info_user_cart_shipping(self, cart_id: int) -> tuple:
        sql = '''
        SELECT 
            total_quantity, total_price, fio, email, phone_number, 
            shipping_address, sub_phone_number, tg_id, shipping_id 
        FROM cart
            LEFT JOIN shipping USING (user_id) 
            LEFT JOIN users USING (user_id) 
        WHERE cart.cart_id = %s
        '''
        info = self.manager(sql, cart_id, fetchone=True)
        return info

    def add_history_buy(self, total_quantity: int, total_price: int, fio: str, email: str, phone_number: str,
                        shipping_address: str, sub_phone_number: str, tg_id: int, shipping_id: int,
                        datetime_buy: datetime.datetime) -> None:
        sql = '''
            INSERT INTO history_buy(total_quantity, total_price, fio, email, phone_number, 
                                    shipping_address, sub_phone_number, tg_id, shipping_id, datetime_buy)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.manager(sql, total_quantity, total_price, fio, email,
                     phone_number, shipping_address, sub_phone_number, tg_id, shipping_id, datetime_buy, commit=True)

    def get_list_buyers(self) -> list:
        sql = '''
            SELECT cart_id, fio FROM shipping
            LEFT JOIN users USING(user_id)
        '''
        list_buyers = self.manager(sql, fetchall=True)
        return [buyers for buyers in list_buyers]

    def get_sales(self, year: str) -> list:
        sql = '''
            SELECT fio, phone_number, total_quantity, total_price FROM history_buy 
            WHERE EXTRACT(YEAR FROM datetime_buy) = %s
        '''
        sales_info = self.manager(sql, year, fetchall=True)
        return sales_info
