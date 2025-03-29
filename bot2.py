import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InputMediaPhoto, InputFile, InputMediaDocument

# Ваш токен
API_TOKEN = '7526778294:AAHgvNGYezNe5uwriUhCof4_T6gP3-kAp0Q'

bot = telebot.TeleBot(API_TOKEN)

DELIVERY_CHANNEL_ID = '@GrowFoodBotOleg'
OFFICE_CHANNEL_ID = '@officechatgrowfood'


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Заявка на пропуск')
    item2 = telebot.types.KeyboardButton("Заявка на офисного курьера")
    markup.row(item1, item2)
    item3 = telebot.types.KeyboardButton("Заявка на курьерскую службу (KSE)")
    item4 = telebot.types.KeyboardButton("Встретить гостя, курьера и тд")
    markup.row(item3, item4)
    item5 = telebot.types.KeyboardButton("Заказ канцелярии")
    item6 = telebot.types.KeyboardButton("Сообщить о проблеме")
    markup.row(item5, item6)


    bot.send_message(
        message.chat.id,
        'Добро пожаловать! Вы можете выбрать нужный вам пункт меню.',
        reply_markup=markup
    )

#-----------------------------Заявка на пропуск---------------------------------------------

class RequestPassState:
    """Состояние для отслеживания процесса заполнения формы"""
    def __init__(self):
        self.organization = None
        self.full_name = None
        self.phone_number = None
        self.department = None
        self.position = None


state_dict = {}  # Словарь для хранения состояний пользователей

@bot.message_handler(func=lambda m: m.text == 'Заявка на пропуск')
def request_pass_start(message):
    """Начало процесса заполнения формы заявки на пропуск"""
    user_state = state_dict.get(message.from_user.id)
    if not user_state:
        user_state = RequestPassState()
        state_dict[message.from_user.id] = user_state

    bot.send_message(
        message.chat.id,
        'Пожалуйста, укажите название вашей организации.'
    )
    bot.register_next_step_handler(message, handle_organization_input)



def handle_organization_input(message):
    """Функция для обработки названия организации"""
    user_state = state_dict[message.from_user.id]
    user_state.organization = message.text.strip()

    if user_state.organization.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректное название организации. Название не должно состоять только из цифр.'
        )
        bot.register_next_step_handler(message, handle_organization_input)
        return

    bot.send_message(
        message.chat.id,
        'Теперь укажите ваше полное имя.'
        )
    bot.register_next_step_handler(message, handle_full_name_input)


def handle_full_name_input(message):
    """Функция для обработки полного имени"""
    user_state = state_dict[message.from_user.id]
    user_state.full_name = message.text.strip().capitalize()

    if user_state.full_name.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректное имя. Имя не должно содержать цифр.'
        )
        bot.register_next_step_handler(message, handle_full_name_input)
        return

    bot.send_message(
        message.chat.id,
        'Укажите ваш номер телефона после +7. Пример: +79998887766'
    )
    bot.register_next_step_handler(message, handle_phone_number_input)



def handle_phone_number_input(message):
    """Функция для обработки номера телефона"""
    user_state = state_dict[message.from_user.id]
    user_state.phone_number = message.text.strip().capitalize()

    if not user_state.phone_number.isdigit():
        bot.send_message(
            message.chat.id,
            'Номер телефона должен состоять только из цифр и соответствовать формату +7XXXXXXXXXX'
        )
        bot.register_next_step_handler(message, handle_phone_number_input)
        return

    bot.send_message(
        message.chat.id,
        'Укажите ваш отдел.'
    )
    bot.register_next_step_handler(message, handle_department_input)



def handle_department_input(message):
    """Функция для обработки отдела"""
    user_state = state_dict[message.from_user.id]
    user_state.department = message.text.strip().capitalize()

    if user_state.department.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректное название отдела. Название отдела не должно состоять только из цифр.'
        )
        bot.register_next_step_handler(message, handle_department_input)
        return

    bot.send_message(
        message.chat.id,
        'И последнее, укажите вашу должность.'
    )
    bot.register_next_step_handler(message, handle_position_input)



def handle_position_input(message):
    """Функция для обработки должности"""
    user_state = state_dict[message.from_user.id]
    user_state.position = message.text.strip().capitalize()

    if user_state.position.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректное название должности. Название должности не должно состоять из цифр.'
        )
        bot.register_next_step_handler(message, handle_position_input)
        return

    application_text = (
        f"Новая заявка на пропуск.\n"
        f"Организация: {user_state.organization}\n"
        f"ФИО: {user_state.full_name}\n"
        f"Телефон: +7{user_state.phone_number}\n"
        f"Отдел: {user_state.department}\n"
        f"Должность: {user_state.position}"
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text)

    # Все данные введены, отправляем подтверждение
    bot.send_message(
        message.chat.id,
        f'Готово! Ваша заявка на пропуск отправлена.\nСрок готовности: 1-2 дня.\nЗабрать пропуск можно в офисе по адресу: ул. Миллионная, д.6\nДля этого обратитесь, пожалуйста, к офис-менеджеру.'
    )

    #Очистим состояние пользователя
    del state_dict[message.from_user.id]


#------------------------------------Заявка на офисного курьера-------------------------------------------------
class RequestOfficeCuriers:
    """Состояние для отслеживания процесса заполнения формы заявки на офисного курьера"""
    def __init__(self):
        self.from_address = None # Адрес отправителя 1
        self.from_name_and_phone = None # Имя отправителя и номер телефона 2
        self.to_address = None # Адрес получателя 3
        self.to_name_and_phone = None # Имя получателя и номер телефона 4
        self.name_docs = None # Наименование (документы или груз) 5
        self.delivery_deadline = None # Крайний срок доставки 6
        self.comment = None # Комментарий 7
        self.photo = None # Вложены ли изображения или документы 8

RequestOfficeCuriers_dict = {} # Словарь для хранения состояний заявок на офисного курьера

@bot.message_handler(func=lambda m: m.text == 'Заявка на офисного курьера')
def request_office_curiers(message):
    """Функция для начала процесса заполнения формы заявки на офисного курьера"""
    user_state = RequestOfficeCuriers_dict.get(message.from_user.id)
    if not user_state:
        user_state = RequestOfficeCuriers()
        RequestOfficeCuriers_dict[message.from_user.id] = user_state

    bot.send_message(
        message.chat.id, 'Заявки оформляются за 1 день и более, доставка по СПБ и ближайшей области. Для того, чтобы создать заявку на офисного курьера ответьте на следующие вопросы: Укажите адрес отправителя в формате: ул. Миллионная, д.6')
    bot.register_next_step_handler(message, handle_from_address_input)


def handle_from_address_input(message):
    """Функция для обработки адреса отправителя"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.from_address = message.text.strip().capitalize()
    if user_state.from_address.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректный адрес отправителя. Адрес должен быть в формате: ул. Миллионная, д.6.'
        )
        bot.register_next_step_handler(message, handle_from_address_input)
        return

    bot.send_message(message.chat.id, 'Укажите имя и номер телефона отправителя')
    bot.register_next_step_handler(message, handle_from_name_and_phone_input)


def handle_from_name_and_phone_input(message):
    """Функция для обработки имени и номера телефона отправителя"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.from_name_and_phone = message.text.strip().capitalize()

    bot.send_message(message.chat.id, 'Укажите адрес отправки заказа (куда)')
    bot.register_next_step_handler(message, handle_to_address_input)


def handle_to_address_input(message):
    """Функция для обработки адреса доставки заказа"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.to_address = message.text.strip().capitalize()
    if user_state.to_address.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректный адрес доставки. Адрес должен быть в формате: ул. Миллионная, д.6. Адрес не должен состоять только из цифр.'
        )
        bot.register_next_step_handler(message, handle_to_address_input)
        return


    bot.send_message(message.chat.id, 'Укажите имя и номер телефона получателя')
    bot.register_next_step_handler(message, handle_to_name_and_phone_input)


def handle_to_name_and_phone_input(message):
    """Функция для обработки имени и номера телефона получателя"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.to_name_and_phone = message.text.strip().capitalize()
    bot.send_message(message.chat.id, 'Укажите наименование (документы или груз)')
    bot.register_next_step_handler(message, handle_name_docs_input)


def handle_name_docs_input(message):
    """Функция для обработки наименования документа или груза"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.name_docs = message.text.strip().capitalize()
    if user_state.name_docs.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректное наименование (документы или груз). Наименование не должно состоять только из цифр.'
        )
        bot.register_next_step_handler(message, handle_name_docs_input)
        return
    bot.send_message(message.chat.id, 'Укажите крайний срок доставки.')
    bot.register_next_step_handler(message, handle_delivery_deadline_input)


def handle_delivery_deadline_input(message):
    """Функция для обработки крайнего срока доставки"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.delivery_deadline = message.text.strip().capitalize()
    bot.send_message(message.chat.id, 'Добавьте комментарий.')
    bot.register_next_step_handler(message, handle_comment_input)


def handle_comment_input(message):
    """Функция для обработки комментария"""
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.comment = message.text.strip().capitalize()
    if user_state.comment.isdigit():
        bot.send_message(
            message.chat.id,
            'Некорректный комментарий. Комментарий не должен состоять только из цифр.'
        )
        bot.register_next_step_handler(message, handle_comment_input)
        return


    bot.send_message(message.chat.id, 'Добавьте фото, изображение или документ.')
    bot.register_next_step_handler(message, handle_photo_input)


def handle_photo_input(message):
    """Функция для обработки вложения фото или документов"""
    # Получаем текущее состояние пользователя
    user_state = RequestOfficeCuriers_dict[message.from_user.id]

    if message.content_type == 'photo':
        # Сохраняем информацию об изображении
        file_id = message.photo[-1].file_id  # берем самое высокое разрешение
        user_state.photo_file_id = file_id

        # Отправляем подтверждение пользователю
        bot.reply_to(message, "Готово! Ваша заявка принята.")

        application_text = (
        f'Заявка на курьерскую службу.\n'
        f'Адрес отправителя: {user_state.from_address}\n'
        f'Имя и номер отправителя: {user_state.from_name_and_phone}\n'                
        f'Адрес получателя: {user_state.to_address}\n'
        f'Имя и номер получателя: {user_state.to_name_and_phone}\n'
        f'Наименование посылки: {user_state.name_docs}\n'
        f'Крайний срок доставки: {user_state.delivery_deadline}\n'
        f'Комментарий: {user_state.comment}\n'
        )


        bot.send_message(OFFICE_CHANNEL_ID, application_text, parse_mode='html')

        # Отправляем изображение в канал доставки
        bot.send_media_group(OFFICE_CHANNEL_ID, [InputMediaPhoto(file_id)])

        del RequestOfficeCuriers_dict[message.from_user.id]



    elif message.content_type == 'image':
        # Сохраняем информацию об изображении
        file_id = message.photo[-1].file_id  # берем самое высокое разрешение
        user_state.photo_file_id = file_id

        # Отправляем подтверждение пользователю
        bot.reply_to(message, "Готово! Ваша заявка принята.")

        application_text = (
            f'Заявка на курьерскую службу.\n'
            f'Адрес отправителя: {user_state.from_address}\n'
            f'Имя и номер отправителя: {user_state.from_name_and_phone}\n'
            f'Адрес получателя: {user_state.to_address}\n'
            f'Имя и номер получателя: {user_state.to_name_and_phone}\n'
            f'Наименование посылки: {user_state.name_docs}\n'
            f'Крайний срок доставки: {user_state.delivery_deadline}\n'
            f'Комментарий: {user_state.comment}\n'
        )

        bot.send_message(OFFICE_CHANNEL_ID, application_text, parse_mode='html')

        bot.send_media_group(OFFICE_CHANNEL_ID, [InputMediaPhoto(file_id)])

        del RequestOfficeCuriers_dict[message.from_user.id]


    elif message.content_type == 'document':
        # Сохраняем информацию о документе
        file_id = message.document.file_id
        user_state.document_file_id = file_id

        # Отправляем подтверждение пользователю
        bot.reply_to(message, "Готово! Ваша заявка принята.")

        application_text = (
            f'Заявка на курьерскую службу.\n'
            f'Адрес отправителя: {user_state.from_address}\n'
            f'Имя и номер отправителя: {user_state.from_name_and_phone}\n'
            f'Адрес получателя: {user_state.to_address}\n'
            f'Имя и номер получателя: {user_state.to_name_and_phone}\n'
            f'Наименование посылки: {user_state.name_docs}\n'
            f'Крайний срок доставки: {user_state.delivery_deadline}\n'
            f'Комментарий: {user_state.comment}\n'
        )

        bot.send_message(OFFICE_CHANNEL_ID, application_text, parse_mode='html')

        bot.send_media_group(OFFICE_CHANNEL_ID, [InputMediaDocument(file_id)])

        del RequestOfficeCuriers_dict[message.from_user.id]

    else:
        # Если не изображение, фото или документ, возвращаем ошибку
        bot.reply_to(message, "Пожалуйста, пришлите изображение или документ.")


#------------------------------------Заявка на курьерскую службу--------------------------------------


class RequestCourierService:
    def __init__(self):
        self.name_receive = None # Имя получателя
        self.to_address = None # Адрес доставки
        self.phone_to = None # Номер телефона получателя
        self.name_docs = None # Наименование груза или документов
        self.deadline = None # Крайний срок доставки
        self.comment = None # Комментарий

        self.name_send = None # Имя отправителя
        self.from_address = None # Адрес от куда забираем
        self.phone_from = None # Номер телефона отправителя
        self.to_name_spb = None # Имя получателя в СПБ

request_courier_service_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Заявка на курьерскую службу (KSE)')
def request_courier_service(message):
    """Функция для обработки запроса на курьерскую службу"""
    bot.send_message(message.chat.id, """Тип курьерской службы:
Внимание! Одна из точек (забор/отправка) – по-умолчанию офис в СПб (ул. Миллионная, д.6).
Если вам нужно отправить документы в офис СПб – выберите «Мы получаем» и укажите адрес, откуда нужно забрать документы.
Если вам нужно получить документы из петербургского офиса – выберите «Мы отправляем».""")
    keyboard = [
        [types.InlineKeyboardButton('Мы отправляем', callback_data='we_send')],
        [types.InlineKeyboardButton('Мы получаем', callback_data='we_take')]
    ]

    markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, 'Выберите тип курьерской службы:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'we_send')
def we_send_callback(call):
    """Функция для обработки выбранного типа курьерской службы (Мы отправляем)"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Мы отправляем.")
    user_state = RequestCourierService()
    request_courier_service_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Укажите имя получателя')
    bot.register_next_step_handler(call.message, handle_to_name1_input)


def handle_to_name1_input(message):
    """Функция для обработки имени получателя"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_receive = message.text.strip().capitalize()
    if user_state.name_receive.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректное имя получателя. Имя не должно содержать цифр.')
        bot.register_next_step_handler(message, handle_to_name1_input)
        return
    bot.send_message(message.chat.id, 'Укажите адрес доставки')
    bot.register_next_step_handler(message, handle_to_address1_input)


def handle_to_address1_input(message):
    """Функция для обработки адреса доставки"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.to_address = message.text.strip().capitalize()
    if user_state.to_address.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректный адрес доставки. Адрес не должен содержать только цифр.')
        bot.register_next_step_handler(message, handle_to_address1_input)
        return
    bot.send_message(message.chat.id, 'Укажите номер телефона получателя после + 7')
    bot.register_next_step_handler(message, handle_phone_to1_input)


def handle_phone_to1_input(message):
    """Функция для обработки номера телефона получателя"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.phone_to = message.text.strip()
    if not user_state.phone_to.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректный номер телефона получателя +7 и остальное 10 цифр.')
        bot.register_next_step_handler(message, handle_phone_to1_input)
        return

    bot.send_message(message.chat.id, 'Укажите наименование груза или документов')
    bot.register_next_step_handler(message, handle_name_docs1_input)


def handle_name_docs1_input(message):
    """Функция для обработки наименования груза или документов"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_docs = message.text.strip().capitalize()
    if user_state.name_docs.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректное наименование груза или документов. Наименование не должно содержать только цифр.')
        bot.register_next_step_handler(message, handle_name_docs1_input)
        return
    bot.send_message(message.chat.id, 'Укажите крайний срок доставки.')
    bot.register_next_step_handler(message, handle_delivery_deadline1_input)


def handle_delivery_deadline1_input(message):
    """Функция для обработки крайнего срока доставки"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.deadline = message.text.strip().capitalize()
    bot.send_message(message.chat.id, 'Добавьте комментарий.')
    bot.register_next_step_handler(message, handle_comment1_input)


def handle_comment1_input(message):
    """Функция для обработки комментария"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.comment = message.text.strip().capitalize()

    application_text = (
        f'Заявка на курьерскую службу.\n'
        f'Тип доставки: Мы отправляем\n'
        f'Имя получателя: {user_state.name_receive}\n'
        f'Телефон получателя: +7{user_state.phone_to}\n'
        f'Адрес (куда доставить): {user_state.to_address}\n'
        f'Наименование документов: {user_state.name_docs}\n'
        f'Крайний срок доставки: {user_state.deadline}\n'
        f'Комментарий: {user_state.comment}\n'
        f'<a href="tg://user?id={message.from_user.id}">Сообщение от: {message.from_user.first_name}</a>\n'
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text, parse_mode='html')

    bot.send_message(message.chat.id, 'Готово! Ваша заявка принята.', parse_mode='html')

    del request_courier_service_dict[message.from_user.id]


@bot.callback_query_handler(func=lambda call: call.data == 'we_take')
def we_take_callback(call):
    """Функция для обработки выбранного типа курьерской службы (Мы получаем)"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Мы получаем.")
    user_state = RequestCourierService()
    request_courier_service_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Укажите имя отправителя')
    bot.register_next_step_handler(call.message, handle_from_name2_input)


def handle_from_name2_input(message):
    """Функция для обработки имени отправителя"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_send = message.text.strip().capitalize()
    if user_state.name_send.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректное имя отправителя. Имя не должно содержать цифр.')
        bot.register_next_step_handler(message, handle_from_name2_input)
        return
    bot.send_message(message.chat.id, 'Укажите адрес откуда забираем')
    bot.register_next_step_handler(message, handle_from_address2_input)


def handle_from_address2_input(message):
    """Функция для обработки адреса откуда забираем"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.from_address = message.text.strip().capitalize()
    if user_state.from_address.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректный адрес откуда забираем. Адрес не должен содержать только цифры.')
        bot.register_next_step_handler(message, handle_from_address2_input)
        return
    bot.send_message(message.chat.id, 'Укажите номер телефона отправителя после +7')
    bot.register_next_step_handler(message, handle_phone_from2_input)


def handle_phone_from2_input(message):
    """Функция для обработки номера телефона отправителя"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.phone_from = message.text.strip()

    if not user_state.phone_from.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректный номер телефона +7 и 10 остальных цифр.')
        bot.register_next_step_handler(message, handle_phone_from2_input)
        return

    bot.send_message(message.chat.id, 'Укажите наименование документов')
    bot.register_next_step_handler(message, handle_name_docs2_input)


def handle_name_docs2_input(message):
    """Функция для обработки наименования документов"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_docs = message.text.strip().capitalize()
    if user_state.name_docs.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректное наименование документов. Наименование не должно содержать только цифр.')
        bot.register_next_step_handler(message, handle_name_docs2_input)
        return
    bot.send_message(message.chat.id, 'Укажите крайний срок забора')
    bot.register_next_step_handler(message, handle_delivery_deadline2_input)


def handle_delivery_deadline2_input(message):
    """Функция для обработки крайнего срока забора"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.deadline = message.text.strip().capitalize()
    if user_state.deadline.isdigit():
        bot.send_message(message.chat.id, 'Укажите корректный крайний срок забора. Крайний срок не должен содержать только цифр.')
        bot.register_next_step_handler(message, handle_delivery_deadline2_input)
        return
    bot.send_message(message.chat.id, 'Добавьте комментарий.')
    bot.register_next_step_handler(message, handle_comment2_input)


def handle_comment2_input(message):
    """Функция для обработки комментария"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.comment = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите имя получателя в Санкт-Петербурге (кому передать)')
    bot.register_next_step_handler(message, handle_to_name_spb2_input)


def handle_to_name_spb2_input(message):
    """Функция для обработки имени получателя в Санкт-Петербурге"""
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.to_name_spb = message.text.strip()
    bot.send_message(message.chat.id, 'Готово! Ваша заявка принята.')

    application_text = (
        f'Заявка на курьерскую службу.\n'
        f'Тип доставки: Мы получаем\n'
        f'Имя отправителя: {user_state.name_send}\n'
        f'Адрес (откуда забираем): {user_state.from_address}\n'
        f'Телефон отправителя: +7{user_state.phone_from}\n'
        f'Наименование документов: {user_state.name_docs}\n'
        f'Крайний срок забора: {user_state.deadline}\n'
        f'Комментарий: {user_state.comment}\n'
        f'<a href="tg://user?id={message.from_user.id}">Сообщение от: {message.from_user.first_name}</a>\n'
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text, parse_mode='html')

    del request_courier_service_dict[message.from_user.id]


#-------------------------------встретить гостя----------------------------------------------
class RequestGuest():
    def __init__(self):
        self.date = None
        self.time = None
        self.information = None

guest_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Встретить гостя, курьера и тд')
def guest(message):
    """Функция для обработки запроса на встречу"""
    user_state = guest_dict.get(message.from_user.id)
    if not user_state:
        user_state = RequestGuest()
        guest_dict[message.from_user.id] = user_state
    bot.send_message(message.chat.id, 'Укажите дату встречи.')
    bot.register_next_step_handler(message, handle_date_input)


def handle_date_input(message):
    """Получаем ответ на вопрос 'Дата встречи?'"""
    guest_state = guest_dict[message.from_user.id]
    guest_state.date = message.text.strip()

    bot.send_message(message.chat.id,'Укажите время встречи.')
    bot.register_next_step_handler(message, handle_time_input)


def handle_time_input(message):
    """Получаем ответ на вопрос 'Время встречи?'"""
    guest_state = guest_dict[message.from_user.id]
    guest_state.time = message.text.strip()

    bot.send_message(message.chat.id,'Укажите что именно требуется.')
    bot.register_next_step_handler(message, handle_information_input)


def handle_information_input(message):
    """Получаем ответ на вопрос 'Что именно требуется?'"""
    guest_state = guest_dict[message.from_user.id]
    guest_state.information = message.text.strip()

    # Все данные введены, отправляем подтверждение
    bot.send_message(
        message.chat.id, 'Готово!')

    application_text = (
        f'Встретить гостя, курьера и тд.\n'
        f'Дата встречи: {guest_state.date}\n'
        f'Время встречи: {guest_state.time}\n'
        f'Что именно требуется: {guest_state.information}\n'
        f'<a href="tg://user?id={message.from_user.id}">Сообщение от: {message.from_user.first_name}</a>\n'
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text, parse_mode='html')



    del guest_dict[message.from_user.id]

#-------------------------Заказ канцелярии-----------------------------------------------------------


class RequestOffice():
    def __init__(self):
        self.article = None

office_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Заказ канцелярии')
def office(message):
    """Функция для обработки запроса на канцелярию"""
    keyboard = [
        [InlineKeyboardButton(text='Срочно', callback_data='fast_order')],
        [InlineKeyboardButton(text='Ближайшая доставка', callback_data='near_delivery')],
    ]

    markup = types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, 'Выберите тип заказа:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'fast_order')
def fast_order_callback(call):
    """Функция для обработки запроса на срочный заказ"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Срочный заказ.")
    user_state = RequestOffice()
    office_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, """Заказ осуществляется через компанию Комус. 
    Вставьте артикул или перечислите необходимые товары для заказа:""")
    bot.register_next_step_handler(call.message, handle_article_fast_input)


def handle_article_fast_input(message):
    """Функция для обработки артикула товара"""
    user_state = office_dict[message.from_user.id]
    user_state.article = message.text.strip().capitalize()

    bot.send_message(message.chat.id, 'Ваш заказ принят. Хорошего дня!')

    application_text = (
        f'Заявка на закупку:\n'
        f'Заказ: Срочно\n'
        f'Что нужно: {user_state.article}\n'
        f'<a href="tg://user?id={message.from_user.id}">Сообщение от: {message.from_user.first_name}</a>\n'
    )
    bot.send_message(DELIVERY_CHANNEL_ID, application_text, parse_mode='html')

    del office_dict[message.from_user.id]


@bot.callback_query_handler(func=lambda call: call.data == 'near_delivery')
def near_delivery_callback(call):
    """Функция для обработки запроса на ближайшую доставку"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Ближайшая доставка.")
    user_state = RequestOffice()
    office_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, """Заказ осуществляется через компанию Комус. 
    Вставьте артикул или перечислите необходимые товары для заказа:""")
    bot.register_next_step_handler(call.message, handle_article_near_input)


def handle_article_near_input(message):
    """Функция для обработки артикула товара"""
    user_state = office_dict[message.from_user.id]
    user_state.article = message.text.strip().capitalize()
    bot.send_message(message.chat.id, 'Ваш заказ принят. Хорошего дня!')

    application_text = (
        f'Заявка на закупку:\n'
        f'Заказ: Ближайшая доставка\n'
        f'Что нужно: {user_state.article}\n'
        f'<a href="tg://user?id={message.from_user.id}">Сообщение от: {message.from_user.first_name}</a>\n'
        )
    bot.send_message(DELIVERY_CHANNEL_ID, application_text, parse_mode='html')

    del office_dict[message.from_user.id]


#----------------------------------Сообщить о проблеме---------------
class ReportProblem():
    def __init__(self):
        self.description = None

report_problem_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Сообщить о проблеме')
def report_problem(message):
    """Функция для обработки запроса на сообщение о проблеме"""
    keyboard = [
        [InlineKeyboardButton(text='Поломка', callback_data='crash')],
        [InlineKeyboardButton(text='Проблема', callback_data='problem')],
    ]
    markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, 'Выберите тип заявки:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'crash')
def crash_callback(call):
    """Функция для обработки запроса на сообщение о поломке"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Поломка.")
    user_state = ReportProblem()
    report_problem_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Пожалуйста, опишите ситуацию:')
    bot.register_next_step_handler(call.message, handle_description_input)



def handle_description_input(message):
    """Функция для обработки описания проблемы"""
    user_state = report_problem_dict[message.from_user.id]
    user_state.description = message.text.strip()
    bot.send_message(message.chat.id, 'Спасибо, ваша заявка отправлена. Хорошего дня!')

    del report_problem_dict[message.from_user.id]


@bot.callback_query_handler(func=lambda call: call.data == 'problem')
def problem_callback(call):
    """Функция для обработки запроса на сообщение о проблеме"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Проблема.")
    user_state = ReportProblem()
    report_problem_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Пожалуйста, опишите ситуацию:')
    bot.register_next_step_handler(call.message, handle_description2_input)


def handle_description2_input(message):
    """Функция для обработки описания проблемы"""
    user_state = report_problem_dict[message.from_user.id]
    user_state.description = message.text.strip()
    bot.send_message(message.chat.id, 'Спасибо, ваша заявка отправлена. Хорошего дня!')

    del report_problem_dict[message.from_user.id]

#---------------------------------Запуск бота-----------------------------------------
bot.polling(none_stop=True)