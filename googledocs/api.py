from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from client import settings
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
		'https://www.googleapis.com/auth/drive.metadata',
		'https://www.googleapis.com/auth/drive.file',
		'https://www.googleapis.com/auth/drive']

user_permission = {
	'type': 'anyone',
	'role': 'writer',
}

def authenticate(store):
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets(os.path.join(settings.BASE_DIR, 'client_secret.json'), SCOPES)
		flags = tools.argparser.parse_args(args=[])
		creds = tools.run_flow(flow, store, flags)
	return creds

def create_sheet(title):
	store = file.Storage('storage.json')
	creds = authenticate(store)
	
	sheet_service = discovery.build('sheets', 'v4', http=creds.authorize(Http()))
	drive_client = discovery.build('drive', 'v3', http=creds.authorize(Http()))

	data = {'properties': {'title': title}}
	sheet = sheet_service.spreadsheets().create(body=data).execute()
	drive_client.permissions().create(fileId=sheet['spreadsheetId'], body=user_permission).execute()

	return sheet['spreadsheetUrl']

def create_doc(title):
	store = file.Storage('storage.json')
	creds = authenticate(store)

	drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

	file_metadata = {
		'name' : title,
		'mimeType' : 'application/vnd.google-apps.document'
	}
	doc = drive_service.files().create(body=file_metadata, fields="id, name, webViewLink").execute()
	drive_service.permissions().create(fileId=doc['id'], body=user_permission).execute()
	
	return doc['webViewLink']
