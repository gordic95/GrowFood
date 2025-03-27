import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

# Ваш токен
API_TOKEN = '7526778294:AAHgvNGYezNe5uwriUhCof4_T6gP3-kAp0Q'

bot = telebot.TeleBot(API_TOKEN)

DELIVERY_CHANNEL_ID = '@GrowFoodBotOleg'


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
# Состояние для отслеживания процесса заполнения формы
class RequestPassState:
    def __init__(self):
        self.organization = None
        self.full_name = None
        self.phone_number = None
        self.department = None
        self.position = None


state_dict = {}  # Словарь для хранения состояний пользователей

@bot.message_handler(func=lambda m: m.text == 'Заявка на пропуск')
def request_pass_start(message):
    user_state = state_dict.get(message.from_user.id)
    if not user_state:
        user_state = RequestPassState()
        state_dict[message.from_user.id] = user_state

    bot.send_message(
        message.chat.id,
        'Пожалуйста, укажите название вашей организации.'
    )
    bot.register_next_step_handler(message, handle_organization_input)


# Функция для обработки названия организации
def handle_organization_input(message):
    user_state = state_dict[message.from_user.id]
    user_state.organization = message.text.strip()

    bot.send_message(
        message.chat.id,
        'Теперь укажите ваше полное имя.'
    )
    bot.register_next_step_handler(message, handle_full_name_input)


# Функция для обработки полного имени
def handle_full_name_input(message):
    user_state = state_dict[message.from_user.id]
    user_state.full_name = message.text.strip()

    bot.send_message(
        message.chat.id,
        'Укажите ваш номер телефона в формате +7...'
    )
    bot.register_next_step_handler(message, handle_phone_number_input)


# Функция для обработки номера телефона
def handle_phone_number_input(message):
    user_state = state_dict[message.from_user.id]
    user_state.phone_number = message.text.strip()

    bot.send_message(
        message.chat.id,
        'Укажите ваш отдел.'
    )
    bot.register_next_step_handler(message, handle_department_input)


# Функция для обработки отдела
def handle_department_input(message):
    user_state = state_dict[message.from_user.id]
    user_state.department = message.text.strip()

    bot.send_message(
        message.chat.id,
        'И последнее, укажите вашу должность.'
    )
    bot.register_next_step_handler(message, handle_position_input)


#Функция для обработки должности
def handle_position_input(message):
    user_state = state_dict[message.from_user.id]
    user_state.position = message.text.strip()

    application_text = (
        f"Новая заявка на пропуск:\n"
        f"Организация: {user_state.organization}\n"
        f"ФИО: {user_state.full_name}\n"
        f"Телефон: {user_state.phone_number}\n"
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
    user_state = RequestOfficeCuriers_dict.get(message.from_user.id)
    if not user_state:
        user_state = RequestOfficeCuriers()
        RequestOfficeCuriers_dict[message.from_user.id] = user_state

    bot.send_message(
        message.chat.id, 'Заявки оформляются за 1 день и более, доставка по СПБ и ближайшей области. Для того, чтобы создать заявку на офисного курьера ответьте на следующие вопросы: Укажите адрес отправителя в формате: ул. Миллионная, д.6')
    bot.register_next_step_handler(message, handle_from_address_input)


def handle_from_address_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.from_address = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите имя и номер телефона отправителя')
    bot.register_next_step_handler(message, handle_from_name_and_phone_input)


def handle_from_name_and_phone_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.from_name_and_phone = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите адрес отправки заказа (куда)')
    bot.register_next_step_handler(message, handle_to_address_input)


def handle_to_address_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.to_address = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите имя и номер телефона получателя')
    bot.register_next_step_handler(message, handle_to_name_and_phone_input)


def handle_to_name_and_phone_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.to_name_and_phone = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите наименование (документы или груз)')
    bot.register_next_step_handler(message, handle_name_docs_input)


def handle_name_docs_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.name_docs = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите крайний срок доставки.')
    bot.register_next_step_handler(message, handle_delivery_deadline_input)


def handle_delivery_deadline_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.delivery_deadline = message.text.strip()
    bot.send_message(message.chat.id, 'Добавьте комментарий.')
    bot.register_next_step_handler(message, handle_comment_input)


def handle_comment_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.comment = message.text.strip()
    bot.send_message(message.chat.id, 'Добавьте фото или документы.')
    bot.register_next_step_handler(message, handle_photo_input)


def handle_photo_input(message):
    user_state = RequestOfficeCuriers_dict[message.from_user.id]
    user_state.photo = message.text.strip()

    bot.send_message(message.chat.id, 'Готово! Ваша заявка принята.')

    del RequestOfficeCuriers_dict[message.from_user.id]

#------------------------------------Заявка на курьерскую службу--------------------------------------
class RequestCourierService:
    def __init__(self):
        self.name_receive = None # Имя получателя
        self.to_adress = None # Адрес доставки
        self.phone_to = None # Номер телефона получателя
        self.name_docs = None # Наименование груза или документов
        self.deadline = None # Крайний срок доставки
        self.comment = None # Комментарий

        self.name_send = None # Имя отправителя
        self.from_adress = None # Адрес от куда забираем
        self.phone_from = None # Номер телефона отправителя
        self.to_name_spb = None # Имя получателя в СПБ

request_courier_service_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Заявка на курьерскую службу (KSE)')
def request_courier_service(message):
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
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Мы отправляем.")
    user_state = RequestCourierService()
    request_courier_service_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Укажите имя получателя')
    bot.register_next_step_handler(call.message, handle_to_name_input)


def handle_to_name_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_receive = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите адрес доставки')
    bot.register_next_step_handler(message, handle_to_adress_input)


def handle_to_adress_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.to_adress = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите номер телефона получателя')
    bot.register_next_step_handler(message, handle_phone_to_input)


def handle_phone_to_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.phone_to = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите наименование груза или документов')
    bot.register_next_step_handler(message, handle_name_docs_input)


def handle_name_docs_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_docs = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите крайний срок доставки.')
    bot.register_next_step_handler(message, handle_delivery_deadline_input)


def handle_delivery_deadline_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.deadline = message.text.strip()
    bot.send_message(message.chat.id, 'Добавьте комментарий.')
    bot.register_next_step_handler(message, handle_comment_input)


def handle_comment_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.comment = message.text.strip()
    bot.send_message(message.chat.id, 'Добавьте фото или документы.')
    bot.register_next_step_handler(message, handle_end_we_send_input)


def handle_end_we_send_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.end_we_send = message.text.strip()

    application_text = (
        f'Заявка на курьерскую службу:\n'
        f'Тип доставки: Мы отправляем\n'
        f'Имя: {user_state.name_receive}\n'
        f'Телефон: {user_state.phone_to}\n'
        f'Адрес доставки: {user_state.to_adress}\n'
        f'Наименование груза или документов: {user_state.name_docs}\n'
        f'Крайний срок доставки: {user_state.deadline}\n'
        f'Комментарий: {user_state.comment}\n'
        f'Сообщение от: {message.from_user.first_name}\n'
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text)

    bot.send_message(message.chat.id, 'Готово! Ваша заявка принята.')



    del request_courier_service_dict[message.from_user.id]

@bot.callback_query_handler(func=lambda call: call.data == 'we_take')
def we_take_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Мы получаем.")
    user_state = RequestCourierService()
    request_courier_service_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Укажите имя отправителя')
    bot.register_next_step_handler(call.message, handle_from_name2_input)


def handle_from_name2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_send = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите адрес откуда забираем')
    bot.register_next_step_handler(message, handle_from_adress2_input)


def handle_from_adress2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.from_adress = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите номер телефона отправителя')
    bot.register_next_step_handler(message, handle_phone_from2_input)


def handle_phone_from2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.phone_from = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите наименование груза или документов')
    bot.register_next_step_handler(message, handle_name_docs2_input)


def handle_name_docs2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.name_docs = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите крайний срок доставки.')
    bot.register_next_step_handler(message, handle_delivery_deadline2_input)


def handle_delivery_deadline2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.deadline = message.text.strip()
    bot.send_message(message.chat.id, 'Добавьте комментарий.')
    bot.register_next_step_handler(message, handle_comment2_input)


def handle_comment2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.comment = message.text.strip()
    bot.send_message(message.chat.id, 'укажите имя получателя в Санкт-Петербурге.')
    bot.register_next_step_handler(message, handle_to_name_spb2_input)


def handle_to_name_spb2_input(message):
    user_state = request_courier_service_dict[message.from_user.id]
    user_state.to_name_spb = message.text.strip()
    bot.send_message(message.chat.id, 'Готово! Ваша заявка принята.')

    application_text = (
        f'Заявка на курьерскую службу:\n'
        f'Тип доставки: Мы получаем\n'
        f'Имя: {user_state.name_send}\n'
        f'Адрес доставки: {user_state.to_adress}\n'
        f'Наименование груза или документов: {user_state.name_docs}\n'
        f'Крайний срок доставки: {user_state.deadline}\n'
        f'Комментарий: {user_state.comment}\n'
        f'Сообщение от: {message.from_user.first_name}\n'
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text)

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
    user_state = guest_dict.get(message.from_user.id)
    if not user_state:
        user_state = RequestGuest()
        guest_dict[message.from_user.id] = user_state
    bot.send_message(message.chat.id, 'Укажите дату встречи.')
    bot.register_next_step_handler(message, handle_date_input)


def handle_date_input(message):  # Получаем ответ на вопрос "Дата встречи?"
    guest_state = guest_dict[message.from_user.id]
    guest_state.date = message.text.strip()

    bot.send_message(message.chat.id,'Укажите время встречи.')
    bot.register_next_step_handler(message, handle_time_input)


def handle_time_input(message):  # Получаем ответ на вопрос "Время встречи?"
    guest_state = guest_dict[message.from_user.id]
    guest_state.time = message.text.strip()

    bot.send_message(message.chat.id,'Укажите что именно требуется.')
    bot.register_next_step_handler(message, handle_information_input)


def handle_information_input(message):  # Получаем ответ на вопрос "Что именно требуется?"
    guest_state = guest_dict[message.from_user.id]
    guest_state.information = message.text.strip()

    # Все данные введены, отправляем подтверждение
    bot.send_message(
        message.chat.id, 'Готово!')

    application_text = (
        f'Встретить гостя, курьера и тд:\n'
        f'Дата встречи: {guest_state.date}\n'
        f'Время встречи: {guest_state.time}\n'
        f'Что именно требуется: {guest_state.information}\n'
        f'Сообщение от: {message.from_user.first_name}\n'
    )

    bot.send_message(DELIVERY_CHANNEL_ID, application_text)



    del guest_dict[message.from_user.id]

#-------------------------Заказ канцелярии-----------------------------------------------------------
class RequestOffice():
    def __init__(self):
        self.article = None

office_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Заказ канцелярии')
def office(message):
    keyboard = [
        [InlineKeyboardButton(text='Срочно', callback_data='fast_order')],
        [InlineKeyboardButton(text='Ближайшая доставка', callback_data='near_delivery')],
    ]

    markup = types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, 'Выберите тип заказа:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'fast_order')
def fast_order_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Срочный заказ.")
    user_state = RequestOffice()
    office_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, """Заказ осуществляется через компанию Комус. 
    Вставьте артикул или перечислите необходимые товары для заказа:""")
    bot.register_next_step_handler(call.message, handle_article_input)


def handle_article_input(message):
    user_state = office_dict[message.from_user.id]
    user_state.article = message.text.strip()
    bot.send_message(message.chat.id, 'Ваш заказ принят. Хорошего дня!')

    application_text = (
        f'Заказ канцелярии:\n'
        f'Номер заказа {user_state.article}\n'
    )
    bot.send_message(DELIVERY_CHANNEL_ID, application_text)


@bot.callback_query_handler(func=lambda call: call.data == 'near_delivery')
def near_delivery_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Ближайшая доставка.")
    user_state = RequestOffice()
    office_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, """Заказ осуществляется через компанию Комус. 
    Вставьте артикул или перечислите необходимые товары для заказа:""")
    bot.register_next_step_handler(call.message, handle_article_input)


#----------------------------------Сообщить о проблеме---------------
class ReportProblem():
    def __init__(self):
        self.description = None

report_problem_dict = {}

@bot.message_handler(func=lambda m: m.text == 'Сообщить о проблеме')
def report_problem(message):
    keyboard = [
        [InlineKeyboardButton(text='Поломка', callback_data='crash')],
        [InlineKeyboardButton(text='Проблема', callback_data='problem')],
    ]
    markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, 'Выберите тип заявки:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'crash')
def crash_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Поломка.")
    user_state = ReportProblem()
    report_problem_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Пожалуйста, опишите ситуацию:')
    bot.register_next_step_handler(call.message, handle_description_input)



def handle_description_input(message):
    user_state = report_problem_dict[message.from_user.id]
    user_state.description = message.text.strip()
    bot.send_message(message.chat.id, 'Спасибо, ваша заявка отправлена. Хорошего дня!')

    del report_problem_dict[message.from_user.id]


@bot.callback_query_handler(func=lambda call: call.data == 'problem')
def problem_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы выбрали: Проблема.")
    user_state = ReportProblem()
    report_problem_dict[call.from_user.id] = user_state
    bot.send_message(call.message.chat.id, 'Пожалуйста, опишите ситуацию:')
    bot.register_next_step_handler(call.message, handle_description2_input)


def handle_description2_input(message):
    user_state = report_problem_dict[message.from_user.id]
    user_state.description = message.text.strip()
    bot.send_message(message.chat.id, 'Спасибо, ваша заявка отправлена. Хорошего дня!')

    del report_problem_dict[message.from_user.id]

#---------------------------------Запуск бота-----------------------------------------
bot.polling(none_stop=True)