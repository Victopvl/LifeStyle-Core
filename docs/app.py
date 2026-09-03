import os
import json
import re
from datetime import datetime
import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURACIÓN (V0.5 - GUI + FILTROS)
# ==========================================

# Usar variable de entorno con un fallback a una carpeta local de prueba
RUTA_OBSIDIAN = os.getenv("OBSIDIAN_VAULT_PATH", "./vault_demo")

ARCHIVO_MEMORIA = "dominios.json"

def cargar_dominios():
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        dominios_por_defecto = {
            "Ingeniería e IA": "01_Ingeniería e IA",
            "Negocios y Cultura Tech": "02_Negocios y Cultura Tech",
            "Marca Personal": "Marca personal",
            "Personal y Gym": "Personal_y_Gym",
        }
        guardar_dominios(dominios_por_defecto)
        return dominios_por_defecto

def guardar_dominios(dominios):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(dominios, f, indent=4, ensure_ascii=False)

if "carpetas" not in st.session_state:
    st.session_state.carpetas = cargar_dominios()

st.set_page_config(page_title="LifeStyle-Core | V0.5", page_icon="🚀", layout="wide")
st.title("🚀 LifeStyle-Core - Orquestador Inteligente")

# ==========================================
# SIDEBAR: GESTIÓN DE DOMINIOS
# ==========================================
with st.sidebar:
    st.subheader("📂 Administrar Dominios")
    nuevo_dominio_nombre = st.text_input("Nombre del nuevo dominio")
    if st.button("Agregar Dominio"):
        if nuevo_dominio_nombre.strip() == "":
            st.warning("Escribe un nombre válido.")
        elif nuevo_dominio_nombre in st.session_state.carpetas:
            st.info("Ese dominio ya existe.")
        else:
            nombre_carpeta_limpio = nuevo_dominio_nombre.strip().replace(" ", "_")
            st.session_state.carpetas[nuevo_dominio_nombre] = nombre_carpeta_limpio
            guardar_dominios(st.session_state.carpetas)
            st.success(f"¡Dominio '{nuevo_dominio_nombre}' guardado!")
            st.rerun()

# ==========================================
# PESTAÑAS PRINCIPALES
# ==========================================
tab_ingreso, tab_dashboard = st.tabs(["📝 Nueva Tarea", "📊 Dashboard de Tareas"])

# ------------------------------------------
# TAB 1: INGRESO DE TAREAS
# ------------------------------------------
with tab_ingreso:
    with st.form("form_tarea"):
        st.subheader("Registrar Nueva Tarea o Nota")
        tarea = st.text_input("¿Qué necesitas registrar o hacer?", placeholder="Ej: Terminar informe de arquitectura")
        fecha_limite = st.date_input("📅 Fecha límite")
        dominio_seleccionado = st.selectbox("📂 ¿A qué dominio pertenece?", list(st.session_state.carpetas.keys()))
        submitted = st.form_submit_button("Crear Nota en Obsidian")

    if submitted:
        if tarea.strip() == "":
            st.warning("⚠️ Escribe el contenido de la tarea antes de guardar.")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            saneado_titulo = tarea[:20].strip().replace(" ", "_")
            nombre_archivo = f"{timestamp}_{saneado_titulo}.md"

            carpeta_destino = st.session_state.carpetas[dominio_seleccionado]
            ruta_carpeta_completa = os.path.join(RUTA_OBSIDIAN, carpeta_destino)
            os.makedirs(ruta_carpeta_completa, exist_ok=True)
            ruta_archivo_completa = os.path.join(ruta_carpeta_completa, nombre_archivo)

            contenido = f"""---
fecha_creacion: {datetime.now().strftime('%Y-%m-%d %H:%M')}
fecha_limite: {fecha_limite.strftime('%Y-%m-%d')}
estado: pendiente
dominio: {dominio_seleccionado}
---

# {tarea}

## 🎯 Acciones / Contexto
- [ ] Revisar requerimientos iniciales
- [ ] Ejecutar primer sprint o bloque de trabajo

---
*Generado automáticamente por LifeStyle-Core v0.5*
"""
            try:
                with open(ruta_archivo_completa, "w", encoding="utf-8") as f:
                    f.write(contenido)
                st.success(f"¡Éxito! Nota creada en **{carpeta_destino}** 🚀")
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")

# ------------------------------------------
# TAB 2: DASHBOARD DE LECTURA CON FILTROS
# ------------------------------------------
with tab_dashboard:
    col_titulo, col_btn = st.columns([0.8, 0.2])
    with col_titulo:
        st.subheader("📋 Resumen de Notas en Obsidian")
    with col_btn:
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            st.rerun()
            
    tareas_leidas = []
    
    # Escanear físicamente las carpetas
    for nombre_dominio, nombre_carpeta in st.session_state.carpetas.items():
        ruta_carpeta = os.path.join(RUTA_OBSIDIAN, nombre_carpeta)
        if os.path.exists(ruta_carpeta):
            for archivo in os.listdir(ruta_carpeta):
                if archivo.endswith(".md"):
                    ruta_archivo = os.path.join(ruta_carpeta, archivo)
                    try:
                        with open(ruta_archivo, "r", encoding="utf-8") as f:
                            contenido = f.read()
                            
                        estado, fecha_lim = "pendiente", "-"
                        match_estado = re.search(r"estado:\s*(.+)", contenido)
                        match_fecha = re.search(r"fecha_limite:\s*(.+)", contenido)
                        match_titulo = re.search(r"^#\s+(.+)", contenido, re.MULTILINE)
                        
                        if match_estado: estado = match_estado.group(1).strip()
                        if match_fecha: fecha_lim = match_fecha.group(1).strip()
                        titulo = match_titulo.group(1).strip() if match_titulo else archivo.replace(".md", "")
                        
                        tareas_leidas.append({
                            "Tarea": titulo,
                            "Dominio": nombre_dominio,
                            "Límite": fecha_lim,
                            "Estado": estado
                        })
                    except Exception:
                        pass
                        
    if tareas_leidas:
        df_tareas = pd.DataFrame(tareas_leidas)
        df_tareas = df_tareas.sort_values(by="Límite")
        
        # --- SECCIÓN DE FILTROS ---
        st.markdown("### 🔍 Filtros de búsqueda")
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            busqueda = st.text_input("Texto en la tarea...", placeholder="Ej: Informe")
        with col_f2:
            dominios_unicos = df_tareas["Dominio"].unique().tolist()
            filtro_dominio = st.multiselect("Filtrar por Dominio", options=dominios_unicos, default=dominios_unicos)
            
        # Aplicar los filtros a los datos
        if busqueda:
            df_tareas = df_tareas[df_tareas["Tarea"].str.contains(busqueda, case=False, na=False)]
        if filtro_dominio:
            df_tareas = df_tareas[df_tareas["Dominio"].isin(filtro_dominio)]
            
        st.dataframe(df_tareas, use_container_width=True, hide_index=True)
    else:
        st.info("No se encontraron notas en tus dominios todavía. ¡Crea una en la otra pestaña!")