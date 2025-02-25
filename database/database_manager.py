try:
    from .users_part import SQLUsersPart
    from .products_part import SQLProductsPart
    from .carts_part import SQLCartsPart
except ImportError as error:
    from users_part import SQLUsersPart
    from products_part import SQLProductsPart
    from carts_part import SQLCartsPart

#


class SQLActionManager:
    def __init__(self):
        self.users: SQLUsersPart = SQLUsersPart()
        self.products: SQLProductsPart = SQLProductsPart()
        self.carts: SQLCartsPart = SQLCartsPart()
