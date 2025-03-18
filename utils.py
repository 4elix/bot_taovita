from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    lang = State()
    fio = State()
    email = State()
    phone_number = State()


class ShowListProductForCategory(StatesGroup):
    category_name = State()


class ShowProductState(StatesGroup):
    product_name = State()


class GetProductForDelete(StatesGroup):
    product_name = State()


class CreateProductState(StatesGroup):
    lang = State()
    image_path = State()
    title = State()
    price = State()
    structure = State()
    vitamins = State()
    description = State()
    quantity = State()
    category_name = State()


class EditProductState(StatesGroup):
    title = State()
    price = State()
    quantity = State()


class CreateCategoryState(StatesGroup):
    lang = State()
    cat_name = State()


class GetFeedbackState(StatesGroup):
    text = State()
    rating = State()


class GetDateState(StatesGroup):
    custom_date = State()


class DeleteEmployee(StatesGroup):
    name_employee = State()
    phone_number = State()


class EditEmployee(StatesGroup):
    name_employee = State()
    phone_number = State()


class ShippingAddress(StatesGroup):
    cart_id = State()
    sub_phone_number = State()
    address = State()


class YearSelas(StatesGroup):
    year = State()
