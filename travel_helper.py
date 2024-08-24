import gspread
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Google Sheets setup
gs = gspread.service_account(filename='credentials.json')
sh = gs.open_by_key('1A7mr9MAA1gomAwOv3NeoVhIPAYOgf1mv3fxTlbcQjf4')
wks = sh.get_worksheet(0)

# Define expected headers
expected_headers = [
    'id', 'Agency_Name', 'Country', 'City_Town', 'Hotel_Name', 
    'Hotel_Rating_Stars', 'Available_Dates_To_Fly', 'Available_Return_Dates', 'Total_Price', 'How_Many_Nights'
]

# Print the headers from the Google Sheet
actual_headers = wks.row_values(1)
print("Actual Headers:", actual_headers)

# Telegram bot setup
TOKEN = '7256193277:AAEMtDw3bqG8DgImbcR0Y4w8Znq39NatknA'  # Replace with your bot's token

# Helper function to parse date range from selection
def parse_date_range(selection):
    month_map = {
        'Sep': (9, 2024),
        'Oct': (10, 2024),
        'Nov': (11, 2024),
        'Dec': (12, 2024),
        'Jan': (1, 2025),
        'Feb': (2, 2025),
        'Mar': (3, 2025)
    }
    parts = selection.split('_')
    if len(parts) == 2:
        month_year = parts[1]
        if month_year in month_map:
            month, year = month_map[month_year]
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            return start_date, end_date
    return None, None

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🇪🇬 Egypt Sharlem sheic", callback_data='1')],
        [InlineKeyboardButton("🇪🇬 Xurgada", callback_data='2')],
        [InlineKeyboardButton("🇹🇳 Tunis", callback_data='3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hi, I am a bot that will help you to find hot deals. "
        "Please share a few important things that you want me to help you with.\n"
        "What country are you looking for?",
        reply_markup=reply_markup
    )

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    country = ""
    if query.data == '1':
        country = "Egypt"
    elif query.data == '2':
        country = "Egypt"
    elif query.data == '3':
        country = "Tunis"

    print(f"country = {country} and query.data is {query.data}")

    # Proceed to nights selection
    await query.edit_message_text(
        text="Please select the number of nights:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("6", callback_data=f'{query.data}_6')],
            [InlineKeyboardButton("8", callback_data=f'{query.data}_8')],
            [InlineKeyboardButton("10", callback_data=f'{query.data}_10')]
        ])
    )

async def night_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    print(f"query = {query}")
    data = query.data.split('_')
    country = ""
    if data[0] == '1':
        country = "Egypt"
    elif data[0] == '2':
        country = "Egypt"
    elif data[0] == '3':
        country = "Tunis"

    nights = data[1]

    print(f"data {data}")
    print(f"country {country}")
    print(f"nights {nights}")

    # Proceed to date selection
    await query.edit_message_text(
        text="Please select your preferred date range or choose 'Any':",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("2024 - Sep", callback_data=f'{data[0]}_{nights}_2024_Sep')],
            [InlineKeyboardButton("2024 - Oct", callback_data=f'{data[0]}_{nights}_2024_Oct')],
            [InlineKeyboardButton("2024 - Nov", callback_data=f'{data[0]}_{nights}_2024_Nov')],
            [InlineKeyboardButton("2024 - Dec", callback_data=f'{data[0]}_{nights}_2024_Dec')],
            [InlineKeyboardButton("2025 - Jan", callback_data=f'{data[0]}_{nights}_2025_Jan')],
            [InlineKeyboardButton("2025 - Feb", callback_data=f'{data[0]}_{nights}_2025_Feb')],
            [InlineKeyboardButton("2025 - Mar", callback_data=f'{data[0]}_{nights}_2025_Mar')],
            [InlineKeyboardButton("Any", callback_data=f'{data[0]}_{nights}_any')]
        ])
    )

async def date_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    print(f"[DEBUG] Received callback query: {query}")
    await query.answer()

    # Split the callback data
    data = query.data.split('_')
    print(f"[DEBUG] Split data: {data}")

    # Initialize variables
    country = ""
    nights = None
    date_range = None
    start_date, end_date = None, None

    # Determine country based on data[0]
    if len(data) >= 2:
        if data[0] == '1':
            country = "Egypt"
        elif data[0] == '2':
            country = "Egypt"
        elif data[0] == '3':
            country = "Tunis"

    # Determine nights and date range
    if len(data) >= 2:
        nights = data[1]
    
    # Check if 'any' is selected or a specific date range
    if len(data) == 3 and data[2] == "any":
        date_range = 'any'
    elif len(data) == 4:
        date_range = data[2] + "_" + data[3]
    else:
        print("[ERROR] Unexpected callback data format")
        await query.edit_message_text(text="🚫 Invalid selection. Please try again.")
        return

    print(f"[DEBUG] Country: {country}, Nights: {nights}, Date Range: {date_range}")

    if date_range == 'any':
        start_date, end_date = None, None
    else:
        start_date, end_date = parse_date_range(date_range)

    if date_range != 'any' and (start_date is None or end_date is None):
        response = "🚫 Invalid date range selected. Please try again."
        keyboard = [[InlineKeyboardButton("Back to Main Menu", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=response, reply_markup=reply_markup)
        return

    # Read data from Google Sheet based on the selection
    records = wks.get_all_records(expected_headers=expected_headers)
    print(f"[DEBUG] Filtering for Country: {country}, Nights: {nights}, Date Range: {date_range}")

    found_records = []
    for record in records:
        try:
            available_dates_to_fly = datetime.strptime(record["Available_Dates_To_Fly"], '%m/%d/%Y')
            available_return_dates = datetime.strptime(record["Available_Return_Dates"], '%m/%d/%Y')

            if (date_range == 'any') or \
               (available_dates_to_fly <= end_date and available_return_dates >= start_date) or \
               (available_dates_to_fly >= start_date and available_dates_to_fly <= end_date) or \
               (available_return_dates >= start_date and available_return_dates <= end_date):
                if record["Country"].strip() == country and str(record["How_Many_Nights"]) == nights:
                    found_records.append(record)
        except ValueError as e:
            print(f"[DEBUG] Date parsing error: {e}")  # Handle invalid date format

    print(f"[DEBUG] Found records: {found_records}")

    if found_records:
        response = "We found some great hot deals for you:\n\n"
        for record in found_records:
            response += (
                f"📍 **City/Town**: {record['City_Town']}\n"
                f"🏨 **Hotel Name**: {record['Hotel_Name']}\n"
                f"⭐ **Hotel Rating**: {record['Hotel_Rating_Stars']}\n"
                f"✈️ **Available Dates to Fly**: {record['Available_Dates_To_Fly']}\n"
                f"🏠 **Available Return Dates**: {record['Available_Return_Dates']}\n"
                f"💲 **Total Price**: ${record['Total_Price']}\n\n"
            )
        response += (
            "📞 If any of these deals look good to you, please contact the respective agency for more details.\n"
            "🔄 If you want to search for more deals or choose another country, simply select from the options below."
        )
    else:
        response = (
            "🚫 Sorry, no hot deals were found for the selected options. Please try different criteria or choose another country.\n\n"
            "🔙 You can go back to the main menu and start a new search."
        )

    # Add a button to go back to the main menu
    keyboard = [
        [InlineKeyboardButton("Back to Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=response, reply_markup=reply_markup)


async def handle_back_to_main(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    # Ensure we are using the correct method to send the response
    chat_id = query.message.chat_id
    await context.bot.send_message(
        chat_id=chat_id,
        text="Hi, I am a bot that will help you to find hot deals. "
             "Please share a few important things that you want me to help you with.\n"
             "What country are you looking for?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🇪🇬 Egypt Sharlem sheic", callback_data='1')],
            [InlineKeyboardButton("🇪🇬 Xurgada", callback_data='2')],
            [InlineKeyboardButton("🇹🇳 Tunis", callback_data='3')]
        ])
    )

async def handle_text_input(update: Update, context: CallbackContext):
    # Respond to any text input with a prompt to select from the buttons
    keyboard = [
        [InlineKeyboardButton("🇪🇬 Egypt Sharlem sheic", callback_data='1')],
        [InlineKeyboardButton("🇪🇬 Xurgada", callback_data='2')],
        [InlineKeyboardButton("🇹🇳 Tunis", callback_data='3')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hey, please choose one of the given countries by clicking on the options below:",
        reply_markup=reply_markup
    )


async def debug_callback_data(update: Update, context: CallbackContext):
    query = update.callback_query
    print(f"[DEBUG] Global handler: Received callback data: {query.data}")


# Define main function to run the bot
def main():
    # Create the application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern='^[1-3]$'))
    app.add_handler(CallbackQueryHandler(night_selection, pattern='^[1-3]_(6|8|10)$'))
    app.add_handler(CallbackQueryHandler(date_selection, pattern='^[1-3]_(6|8|10)_(2024|2025)_(Sep|Oct|Nov|Dec|Jan|Feb|Mar|any)$'))
    app.add_handler(CallbackQueryHandler(date_selection, pattern='^[1-3]_(6|8|10)_any$'))
    app.add_handler(CallbackQueryHandler(handle_back_to_main, pattern='^back_to_main$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    app.add_handler(CallbackQueryHandler(debug_callback_data))
    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
