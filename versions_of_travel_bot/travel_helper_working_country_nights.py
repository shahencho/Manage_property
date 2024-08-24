import gspread
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
TOKEN = '7256193277:AAEMtDw3bqG8DgImbcR0Y4w8Znq39NatknA'

# Define command handlers
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

    # Ask for the number of nights
    keyboard = [
        [InlineKeyboardButton("6 Nights", callback_data=f'{country}_6')],
        [InlineKeyboardButton("8 Nights", callback_data=f'{country}_8')],
        [InlineKeyboardButton("10 Nights", callback_data=f'{country}_10')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"You selected {country}. How many nights are you looking for?",
        reply_markup=reply_markup
    )

async def night_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Extract country and nights from callback data
    data = query.data.split('_')
    country = data[0]
    nights = data[1]

    # Read data from Google Sheet based on the country and number of nights
    records = wks.get_all_records(expected_headers=expected_headers)
    found_records = [record for record in records if 
                     record["Country"].strip() == country and 
                     str(record["How_Many_Nights"]).strip() == nights]
    
    if found_records:
        response = f"We found hot deals for you in {country} with {nights} nights:\n"
        for record in found_records:
            response += (
                f"Agency: {record['Agency_Name']}\n"
                f"Country: {record['Country']}\n"
                f"City/Town: {record['City_Town']}\n"
                f"Hotel Name: {record['Hotel_Name']}\n"
                f"Hotel Rating: {record['Hotel_Rating_Stars']}\n"
                f"Available Dates to Fly: {record['Available_Dates_To_Fly']}\n"
                f"Available Return Dates: {record['Available_Return_Dates']}\n"
                f"Total Price: {record['Total_Price']}\n"
                f"How Many Nights: {record['How_Many_Nights']}\n\n"
            )
    else:
        response = f"Sorry, no hot deals found for {country} with {nights} nights."

    await query.edit_message_text(text=response)

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

# Define main function to run the bot
def main():
    # Create the application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button, pattern='^[1-3]$'))
    app.add_handler(CallbackQueryHandler(night_selection, pattern='^[A-Za-z]+_(6|8|10)$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))  # Add this line to handle text input

    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
