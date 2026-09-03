import os
import json
import re
from datetime import datetime
import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURACIÓN (V0.5 - GUI + FILTROS + DASHBOARD)
# ==========================================
st.set_page_config(page_title="LifeStyle-Core | V0.5", page_icon="🚀", layout="wide")

# 1. Detección inteligente de entorno (Local vs Nube)
RUTA_LOCAL_WINDOWS = r"G:\Mi unidad\OBSIDIAN"

if os.path.exists(r"G:\Mi unidad"):
    # Si detecta tu disco duro físico, usa tus datos reales
    RUTA_OBSIDIAN = RUTA_LOCAL_WINDOWS
else:
    # Si está en Streamlit Cloud (Linux), usa una carpeta temporal aislada
    RUTA_OBSIDIAN = "./vault_demo"

os.makedirs(RUTA_OBSIDIAN, exist_ok=True)
ARCHIVO_MEMORIA = "dominios.json"

# 2. Generador de datos ficticios (Solo se ejecuta en la nube)
def inyectar_datos_demo():
    carpeta_demo = os.path.join(RUTA_OBSIDIAN, "01_Ingeniería_e_IA")
    os.makedirs(carpeta_demo, exist_ok=True)
    archivo_prueba = os.path.join(carpeta_demo, "demo_arquitectura.md")
    
    if not os.path.exists(archivo_prueba):
        contenido_demo = """---
fecha_creacion: 2024-10-25 10:00
fecha_limite: 2024-12-31
estado: pendiente
dominio: Ingeniería e IA
---

# Diseñar arquitectura cloud para el portafolio

## 🎯 Acciones / Contexto
- [x] Configurar repositorio en GitHub
- [x] Sanitizar credenciales y `.env`
- [ ] Desplegar en Streamlit Community Cloud

---
*Nota generada automáticamente para el Demo Público*
"""
        with open(archivo_prueba, "w", encoding="utf-8") as f:
            f.write(contenido_demo)

# Si estamos en modo demo, inyectamos la nota de prueba
if RUTA_OBSIDIAN == "./vault_demo":
    inyectar_datos_demo()


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

# Función auxiliar para leer rápidamente notas recientes para el dashboard
def obtener_tareas_recientes():
    tareas = []
    for dom, carpeta in st.session_state.carpetas.items():
        ruta = os.path.join(RUTA_OBSIDIAN, carpeta)
        if os.path.exists(ruta):
            for arch in os.listdir(ruta):
                if arch.endswith(".md"):
                    try:
                        with open(os.path.join(ruta, arch), "r", encoding="utf-8") as f:
                            cont = f.read()
                        estado_match = re.search(r"estado:\s*(.+)", cont)
                        estado = estado_match.group(1).strip() if estado_match else "pendiente"
                        tareas.append({"Tarea": arch.replace(".md", ""), "Dominio": dom, "Estado": estado})
                    except Exception:
                        pass
    return tareas

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
# PESTAÑAS PRINCIPALES (Ahora son 3)
# ==========================================
tab_dash, tab_ingreso, tab_explorar = st.tabs(["👁️ Dashboard Unificado", "📝 Nueva Tarea", "🔍 Explorador Obsidian"])

# ------------------------------------------
# TAB 1: 4 CUADRANTES SIMÉTRICOS (2x2 Grid)
# ------------------------------------------
with tab_dash:
    st.markdown("### Orquestación de Flujos de Trabajo (SSOT)")
    
    # Inyectamos un estilo CSS ligero para asegurar altura simétrica en las tarjetas
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] > [data-testid="stContainer"] {
            height: 240px;
            overflow-y: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # Fila 1
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("📅 Google Calendar (Staging)")
            st.info("**14:00** - Reunión de Arquitectura Cloud")
            st.info("**16:30** - Code Review Portafolio")
            
    with col2:
        with st.container(border=True):
            st.subheader("📝 Bóveda Obsidian (Últimas Notas)")
            tareas_recientes = obtener_tareas_recientes()
            if tareas_recientes:
                for t in tareas_recientes[:3]:
                    st.write(f"- 📂 **{t['Dominio']}**: {t['Tarea']} *(Estado: {t['Estado']})*")
            else:
                st.write("No hay notas recientes en la bóveda.")

    # Fila 2
    col3, col4 = st.columns(2)
    
    with col3:
        with st.container(border=True):
            st.subheader("📧 Gmail Inbox (Unread)")
            st.warning("🔴 **Urgente:** Alerta de facturación AWS")
            st.success("🟢 **Suscripción:** GitHub Copilot activo")
            
    with col4:
        with st.container(border=True):
            st.subheader("⚙️ System Status")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric(label="APIs", value="3/3", delta="Online")
            sc2.metric(label="Costo", value="$0.00", delta="Óptimo")
            sc3.metric(label="Queue", value="0", delta="Sync")

# ------------------------------------------
# TAB 2: INGRESO DE TAREAS (Tu código original)
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
# TAB 3: DASHBOARD DE LECTURA CON FILTROS (Tu código original)
# ------------------------------------------
with tab_explorar:
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