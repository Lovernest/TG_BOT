import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your actual bot token
BOT_TOKEN = "8130714163:AAFeqZViWLVEq64Y0Ss4H_biUm0924QzD28"

# Dictionary to track each user's progress
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # If user is new, initialize their data
    if user_id not in user_data:
        user_data[user_id] = {"numbers_left": [1, 2, 3, 4, 5], "tries": 0}

    # Send the initial message with the button
    keyboard = [[InlineKeyboardButton("Get a Random Number 🎲", callback_data="get_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Click the button to get a random number!", reply_markup=reply_markup)

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    # Ensure user data exists
    if user_id not in user_data:
        user_data[user_id] = {"numbers_left": [1, 2, 3, 4, 5], "tries": 0}

    # If user has used all 5 tries, disable the button
    if user_data[user_id]["tries"] >= 5 or not user_data[user_id]["numbers_left"]:
        await query.answer("No more chances left!", show_alert=True)
        return

    # Pick a random number from the remaining ones
    chosen_number = random.choice(user_data[user_id]["numbers_left"])
    user_data[user_id]["numbers_left"].remove(chosen_number)
    user_data[user_id]["tries"] += 1

    # Update the button UI
    keyboard = [[InlineKeyboardButton("Get a Random Number 🎲", callback_data="get_number")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"Your random number is: {chosen_number}", reply_markup=reply_markup)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Secret reset command that doesn't notify the user."""
    user_id = update.message.from_user.id
    user_data[user_id] = {"numbers_left": [1, 2, 3, 4, 5], "tries": 0}
    await update.message.delete()  # Deletes the message so no one sees it

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("rst", reset))  # Secret reset command
    application.add_handler(CallbackQueryHandler(get_number, pattern="^get_number$"))

    application.run_polling()

if __name__ == "__main__":
    main()
