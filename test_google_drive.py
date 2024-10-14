from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Function to set up Google Drive API
def setup_drive_service():
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    service = build('drive', 'v3', credentials=creds)
    return service

# Function to upload a file to Google Drive
def upload_to_drive(file_path, file_name):
    service = setup_drive_service()
    
    # Folder ID where the files will be uploaded (replace with your actual folder's ID)
    folder_id = '1sLAd03ExRZmUJseTudYIuyUOc4xfRJLu'  # Change this to your Google Drive folder ID

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]  # The ID of the folder where you want to upload the file
    }

    # Create a MediaFileUpload object for the file
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()

    # Return the Google Drive file link
    return file.get('webViewLink')

# Test the upload functionality
if __name__ == '__main__':
    # Path to the local file you want to upload
    file_path = './logo.png'  # Since logo.png is in your current directory
    
    # Name the file as it will appear in Google Drive
    file_name = 'logo.png'  # The name you want to give the file in Drive

    # Call the upload function and print the link
    file_link = upload_to_drive(file_path, file_name)
    print(f'File uploaded to Google Drive: {file_link}')
