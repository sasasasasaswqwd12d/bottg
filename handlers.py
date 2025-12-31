import os
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from database import add_booking, get_photos, add_photo, get_pending_bookings, update_booking_status
from keyboards import main_menu, service_menu, time_slots_menu, admin_approve_menu, contact_admin_button

load_dotenv()
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Добро пожаловать в салон красоты!\nВыберите действие:",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'book':
        await query.edit_message_text("Выберите услугу:", reply_markup=service_menu())
    elif data.startswith('service_'):
        service = data.replace('service_', '')
        context.user_data['service'] = service
        await query.edit_message_text("Выберите удобное время:", reply_markup=time_slots_menu())
    elif data.startswith('time_'):
        time = data.replace('time_', '')
        context.user_data['time'] = time
        service = context.user_data.get('service')
        user = update.effective_user
        booking_id = add_booking(user.id, user.username or str(user.id), service, time)
        # Уведомление админу
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"🔔 Новая заявка на запись!\n"
                 f"Пользователь: @{user.username or user.id}\n"
                 f"Услуга: {service}\n"
                 f"Время: {time}",
            reply_markup=admin_approve_menu(booking_id)
        )
        await query.edit_message_text("✅ Ваша заявка отправлена! Ожидайте подтверждения от администратора.")
    elif data == 'portfolio':
        photos = get_photos('manicure') + get_photos('pedicure') + get_photos('combo')
        if photos:
            await context.bot.send_media_group(chat_id=update.effective_chat.id, media=photos[:10])
        else:
            await query.edit_message_text("📸 Пока нет работ. Следите за обновлениями!")
    elif data == 'contact':
        await query.edit_message_text(
            "Нажмите кнопку ниже, чтобы связаться с админом:",
            reply_markup=contact_admin_button()
        )
    elif data == 'back_to_menu':
        await query.edit_message_text("Выберите действие:", reply_markup=main_menu())
    elif data.startswith('approve_'):
        bid = int(data.replace('approve_', ''))
        update_booking_status(bid, 'approved')
        # Найти пользователя и уведомить
        # (для простоты — можно хранить user_id в БД и отправлять по нему)
        await query.edit_message_text("✅ Запись подтверждена!")
    elif data.startswith('reject_'):
        bid = int(data.replace('reject_', ''))
        update_booking_status(bid, 'rejected')
        await query.edit_message_text("❌ Запись отклонена.")
