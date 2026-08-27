import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permiso: Solo lectura de calendario
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None
    # Usaremos token_personal.json pensando en tu diseño multi-cuenta
    if os.path.exists('token_personal.json'):
        creds = Credentials.from_authorized_user_file('token_personal.json', SCOPES)
    
    # Si no hay token, abrimos el navegador para pedir permiso
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token_personal.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print("⏳ Buscando tu próximo evento en el calendario...")
        
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print("✅ No tienes eventos próximos. ¡Agenda limpia!")
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"📅 Próximo evento: {event['summary']} a las {start}")

    except Exception as error:
        print(f"❌ Ocurrió un error: {error}")

if __name__ == '__main__':
    main()