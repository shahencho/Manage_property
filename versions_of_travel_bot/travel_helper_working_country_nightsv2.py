from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler

# Start command handler
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Egypt", callback_data='2'),
            InlineKeyboardButton("Turkey", callback_data='1'),
            InlineKeyboardButton("Tunisia", callback_data='3')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select a country:', reply_markup=reply_markup)

# Country selection handler
async def country_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    country_map = {'1': 'Turkey', '2': 'Egypt', '3': 'Tunisia'}
    country = country_map.get(query.data, "Unknown")

    context.user_data['country'] = country
    print(f"Country selected: {country}")

    keyboard = [
        [
            InlineKeyboardButton("6", callback_data=f'{query.data}_6'),
            InlineKeyboardButton("8", callback_data=f'{query.data}_8'),
            InlineKeyboardButton("10", callback_data=f'{query.data}_10')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please select the number of nights:", reply_markup=reply_markup)

# Nights selection handler
async def nights_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    country, nights = data[0], data[1]
    
    context.user_data['nights'] = nights
    print(f"Nights selected: {nights} for country: {context.user_data['country']}")

    keyboard = [
        [
            InlineKeyboardButton("2024 - Sep", callback_data=f'{query.data}_2024_Sep'),
            InlineKeyboardButton("2024 - Oct", callback_data=f'{query.data}_2024_Oct'),
            InlineKeyboardButton("2024 - Nov", callback_data=f'{query.data}_2024_Nov'),
            InlineKeyboardButton("2024 - Dec", callback_data=f'{query.data}_2024_Dec'),
            InlineKeyboardButton("2025 - Jan", callback_data=f'{query.data}_2025_Jan'),
            InlineKeyboardButton("2025 - Feb", callback_data=f'{query.data}_2025_Feb'),
            InlineKeyboardButton("2025 - Mar", callback_data=f'{query.data}_2025_Mar'),
            InlineKeyboardButton("Any", callback_data=f'{query.data}_any')
            
        ],
       
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please select your preferred date range or choose 'Any':", reply_markup=reply_markup)

# Date selection handler
async def date_selection(update: Update, context: CallbackContext):
    
    query = update.callback_query
    print(f"Received callback data: {data}")
    await query.answer()

    data = query.data.split('_')
    print(f"Received callback data: {data}")

    if len(data) == 4:
        country, nights, year, month = data
        date_range = f"{year}_{month}"
    elif data[-1] == 'any':
        country, nights = data[0], data[1]
        date_range = "any"
    else:
        print("Unexpected callback data format")
        return

    print(f"Country: {context.user_data['country']}, Nights: {context.user_data['nights']}, Date Range: {date_range}")

    # Further processing based on date_range
    if date_range == "any":
        print("User selected 'Any' date range.")
        # Fetch all records for the country and nights
    else:
        print(f"Filtering records for {context.user_data['country']}, {context.user_data['nights']} nights, date range: {date_range}")
        # Fetch records based on specific year and month

# Main setup for the bot
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()


async def debug_callback_data(update: Update, context: CallbackContext):
    query = update.callback_query
    print(f"[DEBUG] Global handler: Received callback data: {query.data}")

# Adding command and callback query handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(country_selection, pattern=r'^[1-3]$'))
app.add_handler(CallbackQueryHandler(nights_selection, pattern=r'^[1-3]_[6|8|10]$'))
app.add_handler(CallbackQueryHandler(date_selection, pattern=r'^[1-3]_[6|8|10]_[0-9]{4}_[a-zA-Z]{3}$'))
app.add_handler(CallbackQueryHandler(date_selection, pattern=r'^[1-3]_[6|8|10]_any$'))
app.add_handler(CallbackQueryHandler(debug_callback_data))

# Start the bot
app.run_polling()
