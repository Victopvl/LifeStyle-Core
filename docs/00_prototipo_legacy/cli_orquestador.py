import os
from datetime import datetime

# ==========================================
# CONFIGURACIÓN (V0.1)
# ==========================================
# Reemplaza esto con la ruta real de tu bóveda de Obsidian
RUTA_OBSIDIAN = r"G:\Mi unidad\DriveSyncFiles\OBSIDIAN_VICTO"

CARPETAS = {
    "1": "01_Ingeniería e IA",
    "2": "02_Negocios y Cultura Tech",
    "3": "Marca personal",
    "4": "Personal_y_Gym"
}

def crear_nota_obsidian():
    print("\n🚀 EL NÚCLEO - Ingreso Rápido de Tareas (V0.1)")
    print("-" * 45)
    
    tarea = input("📝 ¿Qué necesitas registrar o hacer?: ")
    fecha_limite = input("📅 Fecha límite (Ej. Hoy, Mañana, 2024-10-25) [Enter para omitir]: ")
    
    print("\n📂 ¿A qué dominio pertenece?")
    for key, value in CARPETAS.items():
        print(f"[{key}] {value}")
    
    opcion = input("Selecciona el número (1-4): ")
    carpeta_destino = CARPETAS.get(opcion, "Inbox") # Cae en Inbox si te equivocas
    
    # Formateo del archivo
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M")
    nombre_archivo = f"{tarea.replace(' ', '_').replace('/', '-')}.md"
    ruta_completa = os.path.join(RUTA_OBSIDIAN, carpeta_destino)
    
    # Crear carpeta si no existe (por si acaso)
    os.makedirs(ruta_completa, exist_ok=True)
    
    contenido_md = f"""---
fecha_creacion: {fecha_creacion}
deadline: {fecha_limite if fecha_limite else 'Sin fecha'}
estado: pendiente
---
# {tarea}

## 📋 Checklist de Acción
- [ ] Tarea 1
- [ ] Tarea 2

## 📝 Notas
- 
"""
    
    # Escribir el archivo
    with open(os.path.join(ruta_completa, nombre_archivo), "w", encoding="utf-8") as f:
        f.write(contenido_md)
        
    print(f"\n✅ ¡Éxito! Tarea guardada en: {carpeta_destino}/{nombre_archivo}")

if __name__ == "__main__":
    while True:
        crear_nota_obsidian()
        continuar = input("\n¿Ingresar otra tarea? (s/n): ")
        if continuar.lower() != 's':
            print("Apagando El Núcleo. ¡A trabajar!")
            break