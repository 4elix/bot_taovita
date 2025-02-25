text_register = {
    'RU': 'Чтобы заказать товар, вам нужно зарегистрироваться',
    'UZ': "Ishni boshlash uchun siz ro'yxatdan o'tishingiz kerak"
}


def text_start(lang, role):
    if role == 'CLIENT':
        text = {
            'RU': 'Здравствуй, что бы заказать нажмите на Посмотреть категории 📚',
            'UZ': "Salom, buyurtma berish uchun bosing kategoriyalarni ko'rish 📚",
        }
        return text[lang]
    else:
        text = {
            'RU': 'Здравствуйте, выберете действие',
            'UZ': "Salom, harakatni tanlang"
        }
        return text[lang]


text_get_fio = {
    'RU': 'Для начала введите свое ФИО, через пробел. Пример: Иванов Иванович Иванов',
    'UZ': "Boshlash uchun bo'sh joy bilan to'liq ismingizni kiriting. Misol: Ivanov Ivanovich Ivanov",
}

error_text_get_fio = {
    'RU': 'Вы ввели некорректные данные, убедитесь что вы ввели данные через пробел. Пример: Иванов Иванович Иванов',
    'UZ': "Siz noto'g'ri ma'lumotlarni kiritdingiz, bo'sh joy orqali ma'lumotlarni kiritganingizga ishonch hosil qiling. Misol: Ivanov Ivanovich Ivanov",
}

text_get_email = {
    'RU': 'Теперь я знаю как к вам обращаться, введите электронную почту. Пример: test@gmail.com',
    'UZ': 'Endi men sizga qanday murojaat qilishni bilaman, elektron pochtangizni kiriting. Misol: test@gmail.com',
}

error_text_get_email = {
    'RU': 'Вы ввели некорректные данные, убедитесь что вы ввели как указано в примере. Пример: test@gmail.com',
    'UZ': "Siz noto'g'ri ma'lumotlarni kiritdingiz, misolda ko'rsatilgandek kiritganingizga ishonch hosil qiling. Misol: test@gmail.com",
}

text_get_phone_number = {
    'RU': 'Нажмите на кнопку для окончания регистрации',
    'UZ': "Ro'yxatdan o'tishni tugatish uchun tugmani bosing",
}

text_success_register = {
    'RU': 'Регистрация прошла успешно',
    'UZ': "Ro'yxatdan o'tish muvaffaqiyatli bo'ldi",
}

error_text_success_register = {
    'RU': 'Произошла ошибка, попробуйте зарегистрироваться ещё раз',
    'UZ': "An error has occurred, please try to register again.",
}

error_text_get_price = {
    'RU': 'Вы ввели неправильную стоимость, она должны состоять только из цифр. Символов не должно быть, введите заново',
    'UZ': "Siz noto'g'ri qiymatni kiritdingiz, u faqat raqamlardan iborat bo'lishi kerak. Belgilar bo'lmasligi kerak, qayta kiriting"
}

error_text_get_quantity = {
    'RU': 'Вы ввели неправильную количество, она должны состоять только из цифре. Символов не должно быть, введите заново',
    'UZ': "Siz noto'g'ri miqdorni kiritdingiz, u faqat raqamdan iborat bo'lishi kerak. Belgilar bo'lmasligi kerak, qayta kiriting"
}

text_list_categories = {
    'RU': 'Продукты данной категории',
    'UZ': 'Ushbu toifadagi mahsulotlar'
}

text_get_feedback = {
    'RU': 'Оставить свой отзыв.',
    'UZ': 'Fikringizni qoldiring'
}

text_get_rating = {
    'RU': 'Введите оценку, от 1-го до 5-ти',
    'UZ': "1 dan 5 gacha bo'lgan ballni kiriting",
}

error_text_get_rating = {
    'RU': 'Вы ввели неправильную оценку, оценка должна состоять из целых чисел или вы ввели большое значение',
    'UZ': "Siz noto'g'ri ball kiritdingiz, ball butun sonlardan iborat bo'lishi kerak yoki siz katta qiymat kiritdingiz"
}

success_send_feedback = {
    'RU': 'Отзыв успешно сохранен, мы учитываем ваше мнения',
    'UZ': "Ko'rib chiqish muvaffaqiyatli saqlanib qoldi, biz sizning fikringizni hisobga olamiz"
}

error_text_fio_and_phone = {
    'RU': 'Вы ввели неправильно ФИО или номер телефона, попробуйте ещё раз',
    'UZ': "Siz noto'g'ri ism yoki telefon raqamini kiritdingiz, qayta urinib ko'ring"
}


def text_info_product(lang: str, title: str, price: str, structure: str,
                      vitamins: str, description: str, quantity: str) -> str:
    if lang == 'RU':
        return f'''
Название продукта: {title}\n 
Стоимость: {price}\n 
Кол-во: {quantity}\n 
Состав: {structure}\n 
Витамины: {vitamins}\n 
Описание: {description}
'''
    elif lang == 'UZ':
        return f'''
Mahsulot nomi: {title}\n 
Narxi: {price}\n 
Soni: {quantity}\n 
Tarkibi: {structure}\n 
Vitaminlar: {vitamins}\n 
Tavsif: {description}
'''


def text_cart(lang: str, cart_products: tuple, total_quantity: str, total_price: str) -> str:
    text = ''
    if lang == 'RU':
        for title, quantity, price in cart_products:
            text += f'''
Название: {title}.
Стоимость за шт.: {price} сум.
Кол-во товара: {quantity} шт.
'''
        text += f'''
----------------------------------------
Общее кол-во товаров: {total_quantity} шт.
Общая стоимость товаров: {total_price} сум.
'''
        return text
    elif lang == 'UZ':
        for title, quantity, price in cart_products:
            text += f"""
Nomi: {title}.
Bir dona narxi: {price} so'm.
Tovarlar soni: {quantity} dona.
"""
        text += f"""
----------------------------------------
Tovarlarning umumiy soni: {total_quantity} dona.
Tovarlarning umumiy qiymati: {total_price} so'm.
"""
        return text


def text_cart_for_admin(fio: str, email: str, phone_number: str, sub_phone_number: str,
                        shipping_address: str, total_quantity: int, total_price: int, lang: str) -> str:
    if lang == 'RU':
        text = f'''
Пришла оплата от {fio}.
Электронная почта {email}.
Номер телефона {phone_number}.
Дополнительный номер телефона {sub_phone_number}.
Адрес доставки {shipping_address}.
------------------------------------------------------
Общая кол-во товаров {total_quantity} шт.
Общая стоимость товаров {total_price} сум.
        '''
        return text
    elif lang == 'UZ':
        text = f'''
{fio} to'lov keldi.
Elektron pochta {email}.
Telefon raqami {phone_number}.
Qo'shimcha telefon raqami {sub_phone_number}.
Yetkazib berish manzili {shipping_address}.
------------------------------------------------------
Tovarlarning umumiy soni {total_quantity} dona.
Tovarlarning umumiy qiymati {total_price} so'm.
        '''
        return text


def text_list_employee(lang: str, fio: str, phone_number: str) -> str:
    if lang == 'RU':
        text = f'''
Фио сотрудника: {fio}.
Номер телефона сотрудника: {phone_number}.
            '''
        return text
    elif lang == 'UZ':
        text = f'''
Xodimning ismi: {fio}.
Xodimning telefon raqami: {phone_number}.
            '''
        return text
