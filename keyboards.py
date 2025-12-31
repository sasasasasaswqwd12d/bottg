from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💅 Записаться", callback_data='book')],
        [InlineKeyboardButton("📸 Посмотреть работы", callback_data='portfolio')],
        [InlineKeyboardButton("📞 Связаться с админом", callback_data='contact')],
    ])

def service_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Маникюр – 1500₽", callback_data='service_manicure')],
        [InlineKeyboardButton("Педикюр – 1500₽", callback_data='service_pedicure')],
        [InlineKeyboardButton("Комбо – 2500₽", callback_data='service_combo')],
        [InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')],
    ])

def time_slots_menu():
    # Пример времён (можно генерировать динамически)
    times = ["09:00", "10:00", "11:00", "12:00", "13:00", "15:00", "16:00", "17:00"]
    buttons = [[InlineKeyboardButton(t, callback_data=f'time_{t}')] for t in times]
    buttons.append([InlineKeyboardButton("⬅️ Назад", callback_data='book')])
    return InlineKeyboardMarkup(buttons)

def admin_approve_menu(booking_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Одобрить", callback_data=f'approve_{booking_id}'),
         InlineKeyboardButton("❌ Отклонить", callback_data=f'reject_{booking_id}')]
    ])

def contact_admin_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📨 Написать админу", url="https://t.me/your_admin_username")]
    ])
