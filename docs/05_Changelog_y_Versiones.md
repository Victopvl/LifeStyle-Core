# 📂 Historial de Versiones y Changelog - LifeStyle-Core

Este documento registra la evolución técnica, hitos y actualizaciones del orquestador.

---

## 🚀 Versión 0.2.0 (Actual - Arquitectura Full-Stack)
*Fecha de liberación: Agosto 2026*

### 🛠️ Nuevas Características y Mejoras:
*   **Migración a Arquitectura Desacoplada (Client-Server):** Separación total entre el backend y el frontend.
*   **Backend (FastAPI):**
    *   Implementación de base de datos relacional local con **SQLite** y SQLAlchemy ORM (`database.py`).
    *   Creación de rutas completas para el ciclo **CRUD** (Crear, Listar, Actualizar estado y Eliminar tareas).
    *   Configuración de **CORS** (`CORSMiddleware`) para permitir la comunicación segura con el frontend.
*   **Frontend (Next.js & React):**
    *   Diseño de una interfaz moderna, responsiva y en modo oscuro utilizando **Tailwind CSS**.
    *   Conexión en tiempo real con la API mediante peticiones asíncronas (`fetch` usando `127.0.0.1:8000`).
    *   Incorporación de interactividad en el Dashboard (botones dinámicos para completar, tachar y eliminar tareas).
*   **Control de Versiones y DevOps:**
    *   Respaldo oficial y sincronización de la nueva estructura en el repositorio remoto de **GitHub**.

---

## 📌 Versión 0.1.0 (Prototipo Inicial)
*   Creación del concepto base del orquestador.
*   Pruebas iniciales de lógica de scripts en Python (`app.py` y estructura de comandos por consola).