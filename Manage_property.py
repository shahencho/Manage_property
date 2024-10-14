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
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext, ConversationHandler
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os
from datetime import datetime

# Set up logging


# Google Sheets setup
gs = gspread.service_account(filename='credentials.json')
sh = gs.open_by_key(your_google_sheet_id)  # Replace with your Google Sheet ID
wks = sh.worksheet('Manage_Properties')  # Replace with the correct worksheet name

# Google Drive setup
def setup_drive_service():
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_to_drive(file_path, file_name):
    service = setup_drive_service()
    
    # Folder ID where the files will be uploaded (replace with your actual folder's ID)
    folder_id = your_google_drive_folder_id  # Change this to your Google Drive folder ID

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

# Start command: Initiates the verification process
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Please provide your full name for verification.")
    return ASK_NAME

# Step 1: Process the name and ask for SSN
async def ask_for_ssn(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text.strip()
    await update.message.reply_text("Please provide the last 4 digits of your SSN.")
    return ASK_SSN

# Step 2: Validate SSN
async def validate_ssn(update: Update, context: CallbackContext):
    ssn_last_four = update.message.text.strip()
    name = context.user_data.get('name')

    if len(ssn_last_four) != 4 or not ssn_last_four.isdigit():
        await update.message.reply_text("Invalid SSN. Please provide a valid 4-digit SSN.")
        return ASK_SSN

    # Validate the user with Google Sheets
    if validate_user(name, ssn_last_four):
        await update.message.reply_text("Verification successful! You are now allowed to proceed.")
        await show_main_menu(update, context)  # Show the main menu
        return ConversationHandler.END  # End the verification conversation
    else:
        await update.message.reply_text("Verification failed. Please try again.")
        return ASK_NAME  # Restart the verification process

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

# Report issue flow
async def report_issue_text(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback
    await query.message.reply_text("Please describe the issue in a text message.")
    return ASK_ISSUE_TEXT

async def process_issue_text(update: Update, context: CallbackContext):
    context.user_data['issue_text'] = update.message.text.strip()
    await update.message.reply_text("Please upload a photo or video of the issue (optional). Type /skip if you want to submit without media.")
    return ASK_ISSUE_MEDIA

async def handle_issue_media(update: Update, context: CallbackContext):
    file = None
    file_link = None

    if update.message.photo:
        file = await update.message.photo[-1].get_file()  # Get the File object
    elif update.message.video:
        file = await update.message.video.get_file()  # Get the File object

    if file:
        # Save the file locally
        file_path = f"downloads/{file.file_path.split('/')[-1]}"
        
        # Download the file from Telegram servers
        await file.download_to_drive(file_path)
        
        # Upload to Google Drive
        file_link = upload_to_drive(file_path, file.file_path.split('/')[-1])

        # Clean up local file after uploading
        os.remove(file_path)

    # If no file was provided, skip media
    file_link = file_link if file_link else "No media uploaded"
    
    # Log the issue in Google Sheets
    log_issue_in_sheet(context.user_data['issue_text'], file_link)

    await update.message.reply_text("Thank you! Your issue has been submitted.")
    return ConversationHandler.END


# Skip media upload
async def skip_media(update: Update, context: CallbackContext):
    file_link = "No media uploaded"
    log_issue_in_sheet(context.user_data['issue_text'], file_link)
    await update.message.reply_text("Thank you! Your issue has been submitted.")
    return ConversationHandler.END

# Function to log issue details in Google Sheets
def log_issue_in_sheet(issue_text, file_link):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wks.append_row([issue_text, file_link, timestamp])

# Main function to start the bot and set up handlers
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Conversation handler for user verification (name and SSN)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_ssn)],
            ASK_SSN: [MessageHandler(filters.TEXT & ~filters.COMMAND, validate_ssn)],
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, start)]
    )

    # Conversation handler for reporting issues
    issue_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(report_issue_text, pattern='report_issues')],
        states={
            ASK_ISSUE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_issue_text)],
            ASK_ISSUE_MEDIA: [
                MessageHandler(filters.PHOTO | filters.VIDEO, handle_issue_media),
                CommandHandler("skip", skip_media)
            ],
        },
        fallbacks=[CommandHandler("skip", skip_media)],
        per_message=True  # Track conversations for every message
    )


    # Add handlers
    app.add_handler(conv_handler)
    app.add_handler(issue_handler)

    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
