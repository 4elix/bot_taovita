try:
    from .database_config import SQLBaseConnect
except ImportError as error:
    from database_config import SQLBaseConnect


class CreationPart(SQLBaseConnect):
    def db_create_users(self) -> None:
        try:
            sql = '''
                DROP TABLE IF EXISTS users CASCADE;
                CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    fio TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    lang TEXT NOT NULL,
                    is_admin BOOLEAN NOT NULL DEFAULT False, 
                    is_ceo BOOLEAN NOT NULL DEFAULT False, 
                    is_client BOOLEAN NOT NULL DEFAULT True, 
                    tg_id BIGINT NOT NULL UNIQUE
                );
            '''
            self.manager(sql, commit=True)
        except Exception as error:
            print(f'Ошибка {error.__class__} в db_create_users')

    def db_create_categories(self):
        try:
            sql = '''
                DROP TABLE IF EXISTS categories CASCADE;
                CREATE TABLE IF NOT EXISTS categories(
                    category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    lang TEXT,
                    category_name TEXT NOT NULL
                );
            '''
            self.manager(sql, commit=True)
        except Exception as error:
            print(f'Ошибка {error.__class__} в db_create_categories')

    def db_create_products(self) -> None:
        try:
            sql = '''
                DROP TABLE IF EXISTS products CASCADE;
                CREATE TABLE IF NOT EXISTS products(
                    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    image_path TEXT,
                    title TEXT,
                    price INTEGER,
                    description TEXT,
                    lang TEXT,
                    category_id INTEGER REFERENCES categories(category_id)
                );
            '''
            self.manager(sql, commit=True)
        except Exception as error:
            print(f'Ошибка {error.__class__} в db_create_products')

    def db_create_feedback(self) -> None:
        try:
            sql = '''
                DROP TABLE IF EXISTS feedback CASCADE;
                CREATE TABLE IF NOT EXISTS feedback(
                    product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    text TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    datetime_creation TIMESTAMP NOT NULL,
                    user_id INTEGER REFERENCES users(user_id)
                );
            '''
            self.manager(sql, commit=True)
        except Exception as error:
            print(f'Ошибка {error.__class__} в db_create_feedback')

    def db_create_cart(self):
        sql = '''
               DROP TABLE IF EXISTS cart CASCADE;
               CREATE TABLE IF NOT EXISTS cart(
                   cart_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                   user_id INTEGER NOT NULL UNIQUE,
                   total_quantity INTEGER DEFAULT 0,
                   total_price INTEGER DEFAULT 0,

                   FOREIGN KEY (user_id) REFERENCES users(user_id)
               );
           '''
        self.manager(sql, commit=True)

    def db_create_cart_for_products(self):
        sql = '''
               DROP TABLE IF EXISTS cart_products;
               CREATE TABLE IF NOT EXISTS cart_products(
                   cart_product_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                   cart_id INTEGER NOT NULL,
                   product_id INTEGER NOT NULL,

                   quantity INTEGER DEFAULT 0,
                   price INTEGER,

                   FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
                   FOREIGN KEY (product_id) REFERENCES products(product_id),

                   UNIQUE(cart_id, product_id)
               );
           '''
        self.manager(sql, commit=True)

    def db_create_shipping(self):
        sql = '''
            DROP TABLE IF EXISTS shipping;
            CREATE TABLE IF NOT EXISTS shipping(
                shipping_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                user_id INTEGER NOT NULL,
                cart_id INTEGER NOT NULL,
                shipping_address TEXT,
                sub_phone_number TEXT,
                
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (cart_id) REFERENCES cart(cart_id),

                UNIQUE(user_id, cart_id)
            );
        '''
        self.manager(sql, commit=True)

    def db_create_history_buy(self):
        sql = '''
            DROP TABLE IF EXISTS history_buy;
            CREATE TABLE IF NOT EXISTS history_buy(
                history_buy_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                total_quantity INTEGER, 
                total_price INTEGER, 
                fio TEXT, 
                email TEXT, 
                phone_number TEXT,
                shipping_address TEXT, 
                sub_phone_number TEXT, 
                tg_id INTEGER, 
                shipping_id INTEGER,
                datetime_buy TIMESTAMP
            );
        '''
        self.manager(sql, commit=True)


creation = CreationPart()
# creation.db_create_users()
# creation.db_create_categories()
# creation.db_create_products()
# creation.db_create_feedback()
# creation.db_create_cart()
# creation.db_create_cart_for_products()
# creation.db_create_shipping()
# creation.db_create_history_buy()
