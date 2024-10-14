import gspread
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Google Sheets setup
gs = gspread.service_account(filename='credentials.json')
sh = gs.open_by_key('1A7mr9MAA1gomAwOv3NeoVhIPAYOgf1mv3fxTlbcQjf4')
wks = sh.get_worksheet(2)


# Print the headers from the Google Sheet
actual_headers = wks.row_values(1)
print("Actual Headers:", actual_headers)

# Telegram bot setup
# TOKEN = '7256193277:AAEMtDw3bqG8DgImbcR0Y4w8Znq39NatknA'  # Replace with your bot's token -> production bot  in digital ocean alreadyt 

# TOKEN = '7503880736:AAHIaSVXCVfwCUFd61pnoXpktQBO86o3JE4' #'7503880736:AAHIaSVXCVfwCUFd61pnoXpktQBO86o3JE4'  travelBot 
# 7503880736:AAHIaSVXCVfwCUFd61pnoXpktQBO86o3JE4 travelbot_to_debug 
# folder_id = '1sLAd03ExRZmUJseTudYIuyUOc4xfRJLu'  # Change this to your Google Drive folder ID

# this is manage_property bot 8161843406:AAEoVlSCLJbqBcWRSGN-RjiuUxHKk7tDBvY
TOKEN = '8161843406:AAEoVlSCLJbqBcWRSGN-RjiuUxHKk7tDBvY'
your_google_sheet_id = "1A7mr9MAA1gomAwOv3NeoVhIPAYOgf1mv3fxTlbcQjf4"
your_google_drive_folder_id = "1sLAd03ExRZmUJseTudYIuyUOc4xfRJLu"

import gspread
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Google Sheets setup
gs = gspread.service_account(filename='credentials.json')
sh = gs.open_by_key('1A7mr9MAA1gomAwOv3NeoVhIPAYOgf1mv3fxTlbcQjf4')
wks = sh.get_worksheet(2)

# Print the headers from the Google Sheet
actual_headers = wks.row_values(1)
print("Actual Headers:", actual_headers)

# Telegram bot setup

your_google_drive_folder_id = "1sLAd03ExRZmUJseTudYIuyUOc4xfRJLu"

# ----
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Suppress httpx logs
httpx_logger = logging.getLogger('httpx')
httpx_logger.setLevel(logging.WARNING)


# Google Drive setup
def setup_drive_service():
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_to_drive(file_path, file_name):
    service = setup_drive_service()
    folder_id = your_google_drive_folder_id

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    return file.get('webViewLink')

# Conversation states
ASK_NAME, ASK_SSN, ASK_ISSUE_TEXT, ASK_ISSUE_MEDIA = range(4)

# Function to validate user name and SSN
def validate_user(name: str, last_four_ssn: str):
    records = wks.get_all_records()
    for record in records:
        sheet_name = record.get('Name', '').strip().lower()
        sheet_ssn = str(record.get('SSN', ''))
        if sheet_name == name.strip().lower() and sheet_ssn[-4:] == last_four_ssn:
            return True
    return False

# Start command: Presents the inline keyboard
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Let's pass identity validation?", callback_data='validate_identity')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello, I'm an automated assistant here to help you.\n"
        "Key Features include:\n"
        "  * Automated Rent Reminders: Send automatic rent reminders directly to tenants.\n"
        "  * Maintenance Requests: Tenants can submit maintenance requests, including photos or videos.",
        reply_markup=reply_markup
    )

# Handler when user presses "Let's pass identity validation?"
async def validate_identity(update: Update, context: CallbackContext):
    logger.info('validate_identity called with update=%s, context=%s', update, context)

    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Please provide your full name for verification.")
    return ASK_NAME

# Step 1: Process the name and ask for SSN
async def ask_for_ssn(update: Update, context: CallbackContext):
    logger.info('ask_for_ssn called with update=%s, context=%s', update, context)

    context.user_data['name'] = update.message.text.strip()
    await update.message.reply_text("Please provide the last 4 digits of your SSN.")
    return ASK_SSN

# Step 2: Process the SSN and validate
async def validate_ssn(update: Update, context: CallbackContext):
    logger.info('validate_ssn called with update=%s, context=%s', update, context)

    ssn_last_four = update.message.text.strip()
    name = context.user_data.get('name')

    if len(ssn_last_four) != 4 or not ssn_last_four.isdigit():
        await update.message.reply_text("Please provide a valid 4-digit SSN.")
        return ASK_SSN

    if validate_user(name, ssn_last_four):
        await update.message.reply_text("Verification successful! You are now allowed to proceed.")
        await show_main_menu(update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Verification failed. Please try again.")
        return ASK_NAME

# Function to display the main menu with buttons after successful verification
async def show_main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Check your bills", callback_data='check_bills')],
        [InlineKeyboardButton("Contact Management", callback_data='contact_management')],
        [InlineKeyboardButton("Report Issues", callback_data='report_issues')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("What would you like to do?", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text("What would you like to do?", reply_markup=reply_markup)

# Handle the main menu selections
async def handle_menu_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'check_bills':
        await show_user_bills(update, context)
    elif query.data == 'contact_management':
        await query.edit_message_text("You chose to contact management.")
    elif query.data == 'report_issues':
        await report_issue_text(update, context)
    elif query.data == 'go_to_main_menu':
        await show_main_menu(update, context)

# Fetch and display user bills
async def show_user_bills(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    name = context.user_data['name']
    records = wks.get_all_records()

    user_data = None
    for record in records:
        if record['Name'].strip().lower() == name.strip().lower():
            user_data = record
            break

    if user_data:
        ssn_last_four = str(user_data['SSN'])[-4:]

        bill_message = (
            f"Here are your bills:\n"
            f"Name: {user_data['Name']}\n"
            f"SSN: {ssn_last_four}\n"
            f"Electricity: ${user_data['Electricity']}\n"
            f"Water: ${user_data['Water']}\n"
            f"Internet: ${user_data['Internet']}\n"
            f"Heating: ${user_data['Heating']}\n"
            f"Parking: ${user_data['Parking']}"
        )

        keyboard = [
            [InlineKeyboardButton("Go to Main Menu", callback_data='go_to_main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(bill_message, reply_markup=reply_markup)
    else:
        await query.edit_message_text("We could not find your billing information. Please try again.")

# Report issues flow
async def report_issue_text(update: Update, context: CallbackContext):

    logger.info('report_issue called with update=%s, context=%s', update, context)

    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Please describe the issue in a text message.")
    return ASK_ISSUE_TEXT

async def process_issue_text(update: Update, context: CallbackContext):
    context.user_data['issue_text'] = update.message.text.strip()
    await update.message.reply_text("Please upload a photo or video of the issue. Type /skip if you want to submit without media.")
    return ASK_ISSUE_MEDIA

async def handle_issue_media(update: Update, context: CallbackContext):
    file = None
    file_link = None

    if update.message.photo:
        file = await update.message.photo[-1].get_file()
    elif update.message.video:
        file = await update.message.video.get_file()

    if file:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        file_path = f"downloads/{file.file_path.split('/')[-1]}"
        await file.download_to_drive(file_path)


        file_link = upload_to_drive(file_path, file.file_path.split('/')[-1])

        os.remove(file_path)

    file_link = file_link if file_link else "No media uploaded"
    log_issue_in_sheet(context.user_data.get('issue_text', 'No description provided'), file_link)

    await update.message.reply_text(f"Thank you! Your issue has been submitted. File link: {file_link}")
    return ConversationHandler.END

async def skip_media(update: Update, context: CallbackContext):
    issue_text = context.user_data.get('issue_text', 'No description provided')
    log_issue_in_sheet(issue_text, "No media uploaded")
    await update.message.reply_text("Thank you! Your issue has been submitted without media.")
    return ConversationHandler.END

def log_issue_in_sheet(issue_text, file_link):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wks.append_row([issue_text, file_link, timestamp])

async def fallback(update: Update, context: CallbackContext):

    logger.info('fallback called with update=%s, context=%s', update, context)

    await update.message.reply_text("I didn't understand that. Please type /start to begin.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(validate_identity, pattern='validate_identity')],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_ssn)],
            ASK_SSN: [MessageHandler(filters.TEXT & ~filters.COMMAND, validate_ssn)],
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, fallback)],
        per_message=False
    )

    issue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(report_issue_text, pattern='report_issues')],
        states={
            ASK_ISSUE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_issue_text)],
            ASK_ISSUE_MEDIA: [
                MessageHandler(filters.PHOTO | filters.VIDEO, handle_issue_media),
                CommandHandler("skip", skip_media)
            ]
        },
        fallbacks=[CommandHandler("skip", skip_media)],
        per_message=False
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(issue_handler)
    app.add_handler(CallbackQueryHandler(handle_menu_selection, pattern='^(check_bills|contact_management|report_issues|go_to_main_menu)$'))

    app.run_polling()

if __name__ == '__main__':
    main()
