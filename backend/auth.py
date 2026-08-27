import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Añadimos el permiso (scope) para leer correos
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def generar_token():
    print("--- Autenticación Multi-Cuenta de Google ---")
    nombre_cuenta = input("Ingresa un identificador (ej. personal, universidad): ").strip()
    archivo_token = f'token_google_{nombre_cuenta}.json'

    if not os.path.exists('credentials.json'):
        print("❌ Error: No se encontró credentials.json")
        return

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open(archivo_token, 'w') as token:
        token.write(creds.to_json())
        
    print(f"✅ ¡Token guardado exitosamente como {archivo_token}!")

if __name__ == '__main__':
    generar_token()