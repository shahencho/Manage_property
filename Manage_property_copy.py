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
    service = build('drive', 'v3', credentials=creds, cache_discovery=False)
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
# Combine all conversation states in one range to ensure uniqueness
ASK_NAME, ASK_SSN, ASK_ISSUE_TEXT, ASK_ISSUE_MEDIA, ASK_USER_QUERY = range(5)

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

    logger.info('show_main_menu is  called with update=%s, context=%s', update, context)



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


# ASK_USER_QUERY = range(1)


# Handle the main menu selections
async def handle_menu_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'check_bills':
        await show_user_bills(update, context)
    elif query.data == 'contact_management':
        await handle_contact_management(update, context)  # New handler for 'Contact Management'

        # await query.edit_message_text("You chose to contact management.")
    elif query.data == 'report_issues':
        await report_issue_text(update, context)
    elif query.data == 'go_to_main_menu':
        await show_main_menu(update, context)


# Function to handle contact management
async def handle_contact_management(update: Update, context: CallbackContext):
    logger.info("handle_contact_management called with update=%s", update)
    query = update.callback_query
    await query.answer()

    # Prompt user to send their query
    logger.info("Asking user for contact query")
    await query.message.reply_text(
        "If you have an urgent question, please reach out to this phone number: 833 313-2564.\n"
        "Otherwise, please type your message below, and we will contact you soon."
    )
    logger.info("Returning state: ASK_USER_QUERY")
    return ASK_USER_QUERY

# Function to process the user's query and log it to Google Sheets
async def process_user_query(update: Update, context: CallbackContext):
    logger.info("process_user_query called with update=%s", update)

    user_message = update.message.text.strip()
    user_name = update.message.from_user.first_name  # Get the user's first name (or use username)

    logger.info(f"User query: {user_message}")
    logger.info(f"User name: {user_name}")

    # Log the user's query to Google Sheets
    try:
        log_user_query_in_sheet(user_name, user_message)
        logger.info("User query logged successfully")
    except Exception as e:
        logger.error(f"Failed to log user query to Google Sheets: {e}")

    # Respond to the user and provide a "Return to Main Menu" option
    await update.message.reply_text("Thank you for your message, we will contact you soon.")

    # Show return to main menu button
    keyboard = [
        [InlineKeyboardButton("Return to Main Menu", callback_data='go_to_main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    logger.info("Returning to main menu")
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    return ConversationHandler.END  # End the conversation after handling the query

# Function to log user query to Google Sheets
def log_user_query_in_sheet(user_name: str, user_message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wks.append_row([user_name, user_message, timestamp])  # Add user name in Column A, message in Column B, timestamp in Column C

    logger.info("log_user_query_in_sheet is called.User query logged successfully")


# Fetch and display user bills
async def show_user_bills(update: Update, context: CallbackContext):

      # Log the user's query
    logger.info(f"show_user_bills called with update=%s, context=%s", update, context)

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
    print("/n we are now in process_issue_text function /n "+CallbackContext.__name__)

    context.user_data['issue_text'] = update.message.text.strip()
    await update.message.reply_text("Please upload a photo or video of the issue. Type /skip if you want to submit without media.")
    return ASK_ISSUE_MEDIA






async def skip_media(update: Update, context: CallbackContext):
    issue_text = context.user_data.get('issue_text', 'No description provided')
    log_issue_in_sheet(issue_text, "No media uploaded")
    await update.message.reply_text("Thank you! Your issue has been submitted without media.")
    # Ask user if they want to upload more or go to main menu
    keyboard = [
        [InlineKeyboardButton("Return to Main Menu", callback_data='go_to_main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return ConversationHandler.END


from telegram import ReplyKeyboardMarkup, KeyboardButton

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

    # Create inline buttons for user decision
    keyboard = [
        [InlineKeyboardButton("Upload More Media", callback_data='upload_more_media')],
        [InlineKeyboardButton("Go to Main Menu", callback_data='go_to_main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Thank you! Your issue has been submitted. File link: {file_link}\nWould you like to upload more media?",
        reply_markup=reply_markup
    )

    return ASK_ISSUE_MEDIA  # Stay in ASK_ISSUE_MEDIA state to handle the user's decision

# Function to process the user's query
# Function to process the user's message
# async def process_user_query(update: Update, context: CallbackContext):
#     logger.info("process_user_query called with update=%s", update)

#     user_message = update.message.text.strip()
#     logger.info("User query: %s", user_message)

#     # Respond to the user and provide a "Return to Main Menu" option
#     await update.message.reply_text("Thank you for your message, we will contact you soon.")

#     # Show return to main menu button
#     keyboard = [
#         [InlineKeyboardButton("Return to Main Menu", callback_data='go_to_main_menu')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text("Please choose:", reply_markup=reply_markup)

#     return ConversationHandler.END  # End the conversation after handling the query


# Conversation handler for contact management
# Conversation handler for contact management
contact_management_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(handle_contact_management, pattern='contact_management')],
    states={
        ASK_USER_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_user_query)]
    },
    fallbacks=[CommandHandler("start", start)]
)


# Handle the user's decision for uploading more media or returning to the main menu
async def handle_media_decision(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'upload_more_media':
        await query.edit_message_text("Please upload the next photo or video.")
        return ASK_ISSUE_MEDIA  # Stay in the media upload state

    elif query.data == 'go_to_main_menu':
        await show_main_menu(update, context)
        return ConversationHandler.END  # End the media upload state and go back to the main menu


# Handler for the 'Upload More' and 'Return to Main Menu' options
# async def handle_more_media_or_menu(update: Update, context: CallbackContext):
#     query = update.callback_query
#     await query.answer()

#     if query.data == 'upload_more':
#         await query.message.reply_text("Please upload another photo or video. Type /skip if you want to finish without uploading more media.")
#         return ASK_ISSUE_MEDIA
#     elif query.data == 'go_to_main_menu':
#         await show_main_menu(update, context)
#         return ConversationHandler.END

# Update the conversation handler for reporting issues
issue_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(report_issue_text, pattern='report_issues')],
    states={
        ASK_ISSUE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_issue_text)],
        ASK_ISSUE_MEDIA: [
            MessageHandler(filters.PHOTO | filters.VIDEO, handle_issue_media),
            CommandHandler("skip", skip_media),
            # CallbackQueryHandler(handle_more_media_or_menu, pattern='^(upload_more|go_to_main_menu)$')
        ]
    },
    fallbacks=[CommandHandler("skip", skip_media)]
)




def log_issue_in_sheet(issue_text, file_link):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wks.append_row([issue_text, file_link, timestamp])

async def fallback(update: Update, context: CallbackContext):

    logger.info('fallback called with update=%s, context=%s', update, context)

    await update.message.reply_text("I didn't understand that. Please type /start to begin.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Main conversation handler for identity validation
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(validate_identity, pattern='validate_identity')],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_ssn)],
            ASK_SSN: [MessageHandler(filters.TEXT & ~filters.COMMAND, validate_ssn)],
            # ASK_USER_QUERY is removed from here to avoid state conflict
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, fallback)],
        per_message=False
    )
    # Issue reporting handler
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

    # Add handlers to the bot
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(issue_handler)
    app.add_handler(contact_management_handler)  # Add contact management handler separately
    app.add_handler(CallbackQueryHandler(handle_menu_selection, pattern='^(check_bills|contact_management|report_issues|go_to_main_menu)$'))
    app.add_handler(CallbackQueryHandler(handle_media_decision, pattern='^(upload_more_media|go_to_main_menu)$'))


    app.run_polling()

if __name__ == '__main__':
    main()
