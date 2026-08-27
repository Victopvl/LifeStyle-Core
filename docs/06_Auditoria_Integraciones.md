# 🗺️ Auditoría y Estrategia de Integraciones - LifeStyle-Core

Este documento define la hoja de ruta arquitectónica para centralizar las aplicaciones del ecosistema personal en el orquestador LifeStyle-Core.

## ⚖️ La Regla de Oro Arquitectónica
1. **Conectar (API):** Cuando la app depende de interacciones externas (correos, universidad) o sensores de hardware cerrados.
2. **Recrear (Módulo Propio):** Cuando la app es un registro de datos estructurados (entrenamientos, finanzas, salud) que carece de API o cuya privacidad es crítica.
3. **Lectura Local:** Cuando la app exporta archivos de texto plano al disco duro (Markdown/Obsidian).
4. **Consumo Nativo:** Cuando la app es de puro consumo multimedia o redes sociales.

---

## 🟢 1. El Núcleo de Orquestación (Conexión vía API)
*Objetivo: Bandeja de entrada centralizada de notificaciones y eventos.*
*   **Google Calendar & Gmail:** API de Google Workspace.
*   **Outlook:** Microsoft Graph API.
*   **Canvas:** LMS REST API (Notas, fechas de entrega, anuncios).
*   **WhatsApp Business:** Meta Cloud API (Webhooks para notificaciones).
*   **Notion / ClickUp:** Uso de APIs oficiales para sincronización cruzada de tareas.
*   **GitHub / Drive / Docs:** APIs oficiales para visualización de actividad y archivos.

## 🟡 2. Segundo Cerebro e IA (Lectura Local e Integración)
*   **Obsidian:** Lectura nativa de archivos `.md` locales en el backend de Python (sincronizados vía Autosync/OneDrive).
*   **IA (ChatGPT/Gemini/Copilot):** Integración futura de LLMs vía API directo en la interfaz.

## 🔵 3. Salud y Entrenamiento (Recrear + Intermediarios)
*   **Samsung Health / Adidas Running:** Conexión de lectura vía Google Fit API o Health Connect.
*   **Hevy:** Recreación total. Módulo propio `Dashboard de Fuerza` conectado a SQLite.
*   **Clue:** Recreación total por privacidad de datos. Módulo encriptado local.

## 🟠 4. Finanzas Personales (Recrear + Automatización RPA)
*   **Bancos (Falabella, Estado, Mach, Santander, etc.):** 
*   *Estrategia:* Debido a la falta de Open Banking local, se recreará un `Dashboard Financiero`. El backend en Python se programará para **leer recibos de transferencias automáticamente desde Gmail/Outlook** y poblar la base de datos.

## 🟣 5. Aprendizaje y Utilidades (Módulos Propios)
*   **Plataformas de Cursos (Udemy, Coursera, UNAB):** Recreación como módulo `Tracker de Aprendizaje`.
*   **Utilidades:** Clima (OpenWeather API), Mapas (Google Maps API), Reloj/Alarmas (Lógica nativa en Next.js).

## 🟤 6. Consumo Nativo y Multimedia (Fuera del Orquestador)
*   *Redes Sociales:* Instagram, TikTok, Facebook, LinkedIn.
*   *Entretenimiento y Utilidades Cerradas:* Netflix, Spotify, CapCut, Canva, Sudoku.