# LifeStyle-Core

> Sistema operativo personal híbrido para la orquestación automatizada de tiempo, conocimiento y procesos bajo una arquitectura local/cloud con un costo operativo de $0 USD.

[🌐 Ver demo en vivo](https://www.google.com/search?q=https://lifestyle-core.streamlit.app)

---

## 🎯 Contexto

Gestionar múltiples frentes operativos —como estudios universitarios, entrenamiento físico, finanzas, marca personal y liderazgo en proyectos— suele requerir el uso de más de 30 aplicaciones fragmentadas.

Esta desconexión genera una alta fricción cognitiva y silos de información entre las distintas áreas de la vida diaria, perdiendo tiempo valioso en sincronizaciones manuales.

Este proyecto propone un **Single Source of Truth (SSOT)** que centraliza la captura pasiva y activa de información, la procesa mediante un motor centralizado en Python y la distribuye de forma estructurada hacia herramientas de gestión de tiempo y conocimiento.

El foco del proyecto está en automatizar la **orquestación operativa personal**, eliminando aplicaciones redundantes bajo una arquitectura de costo cero.

---

## 💡 Solución

Se desarrolló una plataforma modular híbrida que centraliza:

* Captura e ingesta unificada de datos (correo y calendarios).
* Motor de procesamiento centralizado en FastAPI con base de datos local SQLite.
* Integración estructurada con Obsidian (Segundo Cerebro) mediante generación automática de archivos Markdown.
* Sincronización multi-cuenta con Google Calendar.
* Dashboard visual unificado para la gestión y aprobación de tareas.

La solución prioriza una experiencia limpia y centralizada, permitiendo que el usuario pueda:

```text
Capturar eventos / notas
        │
        ▼
Motor FastAPI & Staging (SQLite)
        │
        ├──► Sincronización Google Calendar
        └──► Inyección de Notas Markdown en Obsidian
        │
        ▼
Dashboard Unificado (Streamlit)

```

---

## 🚀 Funcionalidades

### Dashboard Unificado

* Vista centralizada de flujos de trabajo en 4 cuadrantes.
* Monitoreo del estado del sistema en tiempo real.
* Visualización de eventos próximos de Google Calendar.
* Bandeja de entrada simulada para gestión de correos recientes.

### Gestión de Tareas y Notas

* Registro estructurado de tareas por dominios personalizados.
* Creación automática de archivos Markdown con metadatos (Frontmatter YAML) directamente en la bóveda de Obsidian.
* Explorador interactivo con filtrado por texto y dominios.

### Integraciones y Multi-cuenta

* Soporte para la lectura de múltiples cuentas de Google Calendar y Gmail de manera simultánea.
* Arquitectura de persistencia local basada en archivos seguros.

---

## 🏗️ Arquitectura

El proyecto utiliza una arquitectura híbrida dividida en 4 capas principales orientadas a la soberanía de los datos.

```text
                Capa 1: Captura Pasiva
            (APIs de Google / IMAP / Webhooks)
                           │
                           ▼
                 Capa 2: Motor Central
                 (FastAPI + SQLite)
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
         ▼                                   ▼
Capa 3: Destinos de Persistencia     Capa 4: Interfaz Web
(Google Calendar / Obsidian Vault)    (Streamlit Dashboard)

```

La aplicación separa la lógica de la API, la gestión de bases de datos locales, el manejo de credenciales y la interfaz visual.

### Estructura principal

```text
/
├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   └── test_google.py
├── docs/
├── frontend/
├── dashboard.py
├── dominios.json
├── requirements.txt
└── .env.example

```

---

## 🛠️ Tech Stack

### Backend & Core

* Python 3.11+
* FastAPI
* Pydantic
* SQLAlchemy

### Persistencia y Datos

* SQLite
* Markdown (Obsidian Vault)
* Pandas

### Frontend & Interfaz

* Streamlit

### Integraciones

* Google API Client (OAuth2 Calendar/Gmail)
* Streamlit Community Cloud

### Development

* Git
* GitHub
* Docker / PM2 (Soporte local)

---

## 📐 Diseño de la solución

La solución fue diseñada bajo un principio de **soberanía y cero costo operativo ($0 USD)**.

En lugar de depender de servicios de pago o infraestructuras en la nube costosas, se priorizó el aprovechamiento de capas gratuitas de APIs y el procesamiento local respaldado por una base de datos ligera.

> **Captura centralizada → Procesamiento local en Staging (SQLite) → Escritura directa en archivos de conocimiento (Obsidian) y tiempo (Calendar).**

---

## 📋 Alcance actual

### MVP

El alcance actual incluye:

* API backend funcional con FastAPI.
* Persistencia local con SQLite.
* Integración de lectura multi-cuenta con Google Calendar y Gmail.
* Creación automatizada de archivos Markdown estructurados en Obsidian.
* Interfaz gráfica en Streamlit con modo dual (entorno local privado vs. demo pública en la nube con datos mock).
* Aislamiento estricto de credenciales y tokens mediante variables de entorno (`.env`).

### Fuera del alcance actual

El MVP no incluye inicialmente:

* Automatización completa por WhatsApp mediante Webhooks (en fase de pruebas locales).
* Inferencia masiva mediante modelos LLM locales avanzados (Ollama) o en la nube (Groq/Gemini) integrada en producción continua.
* Aplicación móvil nativa.

---

## 🔮 Roadmap

### Fase 1 — MVP Base

* [x] Arquitectura de 4 capas
* [x] Conexión FastAPI con SQLite
* [x] Integración de Google Calendar y Gmail multi-cuenta
* [x] Generación de notas en Obsidian
* [x] Dashboard básico en Streamlit
* [x] Despliegue de demo segura en la nube

### Fase 2 — Automatización de Capa 1

* [ ] Listener local de WhatsApp (Baileys / whatsapp-web.js)
* [ ] Ingesta automatizada de correos vía IMAP
* [ ] Pipeline de parsing estructurado de datos

### Fase 3 — Motor de Inteligencia Artificial

* [ ] Integración con Groq Cloud API (Llama-3) para inferencia rápida
* [ ] Integración con Google Gemini Flash para contexto amplio
* [ ] Motor NER local opcional (Ollama) para datos sensibles

### Fase 4 — Ecosistema Completo

* [ ] Conexión nativa con ClickUp (Free Tier) para proyectos de emprendimiento
* [ ] Automatización completa de sincronización bidireccional

---

## 🧪 Estado del proyecto

**MVP funcional — Portfolio Project**

El proyecto se encuentra desplegado en su versión de demostración pública e integra un panel de control interactivo en Streamlit Cloud.

La lógica central de la API y la conexión con herramientas de productividad operan de manera estable bajo un esquema de seguridad *Zero Trust*.

---

## 🔐 Seguridad y configuración

Las credenciales de acceso, llaves de API y tokens de autenticación de Google se manejan de manera estricta bajo el principio de menor privilegio.

* Los archivos de credenciales (`credentials.json`, `token_google_*.json`) y los archivos de configuración de entorno (`.env`) están excluidos permanentemente del control de versiones mediante `.gitignore`.
* Se provee una plantilla de configuración (`.env.example`) para facilitar el despliegue seguro sin comprometer datos personales.

---

## 🧠 Decisiones técnicas

### ¿Por qué FastAPI y SQLite?

FastAPI permite construir una API de alto rendimiento con validación automática de tipos gracias a Pydantic, ideal para un entorno ágil. SQLite ofrece una persistencia local sumamente eficiente, ligera y sin costos de servidores dedicados, cumpliendo con la restricción de presupuesto de $0 USD.

### ¿Por qué Streamlit para la interfaz?

Permite prototipar y desplegar dashboards analíticos interactivos en Python de forma inmediata, conectando de manera directa la lógica de backend con una interfaz visual funcional para la web sin la sobrecarga de mantener un framework frontend complejo.

### ¿Por qué integración con Obsidian?

En lugar de duplicar información en bases de datos cerradas, aprovechar archivos Markdown locales permite mantener la soberanía absoluta sobre el segundo cerebro del usuario, facilitando la portabilidad y el control total de los datos.

---

## 📊 Flujo principal

```text
Fuentes Externas (Calendar / Gmail)
                  │
                  ▼
          FastAPI (Backend)
                  │
                  ▼
         Staging Area (SQLite)
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
Vault Obsidian        Dashboard Streamlit
(Archivos .md)        (Interfaz de Control)

```

---

## ⚙️ Instalación local

### Requisitos

* Python 3.11 o superior
* Git

### Clonar repositorio

```bash
git clone https://github.com/Victopvl/LifeStyle-Core.git
cd LifeStyle-Core

```

### Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

```

### Configuración de variables de entorno

Crea un archivo `.env` en la raíz basado en el archivo `.env.example`:

```text
OBSIDIAN_VAULT_PATH="./vault_demo"
DATABASE_URL=sqlite:///./lifestyle.db

```

### Ejecución del Dashboard

```bash
streamlit run dashboard.py

```

---

## ⚠️ Limitaciones actuales

El MVP presenta limitaciones de diseño deliberadas para mantener la simplicidad:

* La versión pública desplegada en la nube opera con una bóveda de demostración aislada y datos simulados para proteger la privacidad del usuario.
* Las integraciones automatizadas masivas de mensajería requieren ejecución en entorno local debido a las restricciones de sesión de las APIs de mensajería web.

---

## 📚 Aprendizajes

Este proyecto permitió consolidar competencias en:

* Diseño e implementación de arquitecturas orientadas a servicios (SOA).
* Desarrollo de APIs asíncronas con FastAPI y validación estricta de esquemas.
* Integración de servicios de terceros mediante OAuth2 (Google APIs).
* Manipulación automatizada del sistema de archivos mediante programación (generación de Markdown).
* Prácticas de seguridad de la información (*Zero Trust* y gestión de secretos).

---

## 🎯 Capacidades demostradas

Este proyecto demuestra competencias técnicas avanzadas en:

**Systems Architecture**

* Diseño de sistemas híbridos de múltiples capas (local y cloud).
* Centralización de fuentes de datos heterogéneas (SSOT).

**Backend Development**

* Construcción de microservicios robustos con Python y FastAPI.
* Gestión de bases de datos locales eficientes (SQLite).

**API Integration**

* Autenticación y consumo seguro de APIs de Google (Calendar y Gmail).

**Security & DevOps**

* Gestión segura de secretos y control riguroso de versiones (`.gitignore`).
* Despliegue de aplicaciones analíticas en la nube con aislamiento de entornos.

---

## 👩🏻‍💻 Autora

**Victoria Vallejos**

Consultora TI & Workspaces Architect

Estudiante de Ingeniería Civil Informática — Universidad Andrés Bello

Áreas de especialización:

* Digitalización de procesos.
* Arquitectura de workspaces.
* Gestión de proyectos TI.
* Diseño de soluciones digitales.
* Optimización operativa para PyMEs.

### Links

* [Portfolio](https://victopvl.github.io/)
* [GitHub](https://github.com/Victopvl)

---

## 📄 Licencia

Proyecto desarrollado con fines de demostración profesional y portfolio.