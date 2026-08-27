import os
import glob
import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from sqlalchemy.orm import Session
from pydantic import BaseModel
import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="LifeStyle-Core API",
    description="Motor central del Orquestador de Tareas e Integraciones"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MODELO DE DATOS PARA TAREAS Y NOTAS ---
class TareaCreate(BaseModel):
    titulo: str
    contenido: str = ""
    dominio: str

RUTA_OBSIDIAN = r"G:\Mi unidad\DriveSyncFiles\OBSIDIAN_VICTO"

@app.get("/")
def leer_raiz():
    return {"estado": "activo"}

@app.get("/tareas")
def obtener_tareas(db: Session = Depends(get_db)):
    return db.query(database.Tarea).all()

@app.post("/tareas")
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    # 1. Guardar en SQLite
    nueva_tarea = database.Tarea(
        titulo=tarea.titulo,
        contenido=tarea.contenido,
        dominio=tarea.dominio,
        estado="pendiente"
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)

    # 2. Guardar en la bóveda de Obsidian como archivo .md
    if os.path.exists(RUTA_OBSIDIAN):
        nombre_archivo = "".join([c for c in tarea.titulo if c.isalnum() or c == ' ']).strip()
        ruta_archivo = os.path.join(RUTA_OBSIDIAN, f"{nombre_archivo}.md")

        contenido_md = f"---\ndominio: {tarea.dominio}\nestado: pendiente\n---\n\n# {tarea.titulo}\n\n{tarea.contenido}\n"

        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(contenido_md)
            print(f"✅ Nota creada en Obsidian: {nombre_archivo}.md")
        except Exception as e:
            print(f"❌ Error al guardar en Obsidian: {e}")
    else:
        print(f"⚠️ No se encontró la ruta de Obsidian: {RUTA_OBSIDIAN}")

    return nueva_tarea

# --- RUTA PARA MARCAR COMPLETADA/PENDIENTE ---
@app.put("/tareas/{tarea_id}")
def actualizar_estado(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(database.Tarea).filter(database.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    tarea.estado = "completado" if tarea.estado == "pendiente" else "pendiente"
    db.commit()
    db.refresh(tarea)
    return tarea

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(database.Tarea).filter(database.Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada"}

# --- RUTA MULTI-CUENTA DE GOOGLE CALENDAR ---
@app.get("/api/calendar/upcoming")
def get_upcoming_events():
    archivos_token = glob.glob('token_google_*.json')
    
    if not archivos_token:
        if os.path.exists('token_personal.json'):
            archivos_token = ['token_personal.json']
        else:
            raise HTTPException(status_code=401, detail="No hay cuentas de Google vinculadas.")

    todos_los_eventos = []

    for archivo in archivos_token:
        nombre_cuenta = archivo.replace('token_google_', '').replace('.json', '')
        creds = Credentials.from_authorized_user_file(archivo, SCOPES)
        
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(archivo, 'w') as token:
                    token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=3, singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                todos_los_eventos.append({
                    "cuenta": nombre_cuenta,
                    "summary": event.get('summary', 'Sin título'),
                    "start": start,
                    "link": event.get('htmlLink', '#')
                })
        except Exception as error:
            print(f"Error leyendo calendario de {nombre_cuenta}: {error}")

    todos_los_eventos = sorted(todos_los_eventos, key=lambda x: x['start'])
    return {"success": True, "events": todos_los_eventos}

# --- RUTA MULTI-CUENTA DE GMAIL (CORREOS RECIENTES) ---
@app.get("/api/gmail/unread")
def get_unread_emails():
    archivos_token = glob.glob('token_google_*.json')
    
    if not archivos_token:
        raise HTTPException(status_code=401, detail="No hay cuentas de Gmail vinculadas.")

    todos_los_correos = []

    for archivo in archivos_token:
        nombre_cuenta = archivo.replace('token_google_', '').replace('.json', '')
        creds = Credentials.from_authorized_user_file(archivo, SCOPES)
        
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(archivo, 'w') as token:
                    token.write(creds.to_json())

        try:
            service = build('gmail', 'v1', credentials=creds)
            # Ampliamos la consulta para buscar en cualquier estado del buzón del usuario
            results = service.users().messages().list(userId='me', maxResults=5, includeSpamTrash=False).execute()
            messages = results.get('messages', [])

            for msg in messages:
                txt = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = txt['payload']['headers']
                
                asunto = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sin Asunto')
                remitente = next((h['value'] for h in headers if h['name'] == 'From'), 'Desconocido')
                remitente_limpio = remitente.split('<')[0].strip()
                
                todos_los_correos.append({
                    "cuenta": nombre_cuenta,
                    "asunto": asunto,
                    "remitente": remitente_limpio,
                    "link": f"https://mail.google.com/mail/u/0/#inbox/{msg['id']}"
                })
        except Exception as e:
            print(f"Error leyendo correos de {nombre_cuenta}: {e}")

    return {"success": True, "emails": todos_los_correos}