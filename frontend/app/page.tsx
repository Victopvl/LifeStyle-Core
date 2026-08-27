"use client";

import { useEffect, useState } from "react";

interface Tarea {
  id: number;
  titulo: string;
  contenido: string;
  dominio: string;
  estado: string;
}

interface EventoCalendar {
  cuenta: string;
  summary: string;
  start: string;
  link: string;
}

interface Email {
  cuenta: string;
  asunto: string;
  remitente: string;
  link: string;
}

export default function Home() {
  const [tareas, setTareas] = useState<Tarea[]>([]);
  const [eventos, setEventos] = useState<EventoCalendar[]>([]);
  const [emails, setEmails] = useState<Email[]>([]);
  
  const [titulo, setTitulo] = useState("");
  const [contenido, setContenido] = useState("");
  const [dominio, setDominio] = useState("");
  
  const [cargandoCalendar, setCargandoCalendar] = useState(true);
  const [cargandoEmails, setCargandoEmails] = useState(true);

  useEffect(() => {
    obtenerTareas();
    obtenerEventosCalendar();
    obtenerEmails();
  }, []);

  const obtenerTareas = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/tareas");
      if (res.ok) {
        const data = await res.json();
        setTareas(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error("Error al obtener tareas:", err);
    }
  };

  const obtenerEventosCalendar = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/calendar/upcoming");
      if (res.ok) {
        const data = await res.json();
        setEventos(data.events || []);
      }
    } catch (err) {
      console.error("Error al obtener eventos de Calendar:", err);
    } finally {
      setCargandoCalendar(false);
    }
  };

  const obtenerEmails = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/gmail/unread");
      if (res.ok) {
        const data = await res.json();
        setEmails(data.emails || []);
      }
    } catch (err) {
      console.error("Error al obtener correos:", err);
    } finally {
      setCargandoEmails(false);
    }
  };

  const agregarTarea = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!titulo.trim() || !dominio.trim()) return;

    try {
      const res = await fetch("http://127.0.0.1:8000/tareas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ titulo, contenido, dominio }),
      });

      if (res.ok) {
        setTitulo("");
        setContenido("");
        setDominio("");
        obtenerTareas();
      }
    } catch (err) {
      console.error("Error al agregar nota:", err);
    }
  };

  const toggleCompletada = async (id: number) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/tareas/${id}`, { method: "PUT" });
      if (res.ok) obtenerTareas();
    } catch (err) {
      console.error("Error al actualizar:", err);
    }
  };

  const eliminarTarea = async (id: number) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/tareas/${id}`, { method: "DELETE" });
      if (res.ok) obtenerTareas();
    } catch (err) {
      console.error("Error al eliminar:", err);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      {/* Contenedor adaptado al ancho completo de la pantalla con un margen controlado */}
      <div className="w-full max-w-[1600px] mx-auto space-y-6">
        
        {/* Encabezado */}
        <header className="border-b border-slate-800 pb-4">
          <h1 className="text-3xl font-bold text-cyan-400">🚀 LifeStyle-Core</h1>
          <p className="text-slate-400">Orquestador inteligente centralizado (Full-Stack)</p>
        </header>

        {/* FILA 1: CALENDAR + EMAILS (2 Columnas simétricas a ancho completo) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          
          {/* Próximos Eventos */}
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col h-[420px]">
            <h2 className="text-lg font-semibold mb-4 text-cyan-300 flex items-center gap-2 shrink-0">
              📅 Próximos Eventos
            </h2>
            <div className="overflow-y-auto pr-1 space-y-3 flex-grow custom-scrollbar">
              {cargandoCalendar ? (
                <p className="text-slate-400 text-sm">Cargando eventos...</p>
              ) : eventos.length === 0 ? (
                <p className="text-slate-400 text-sm">No hay eventos próximos.</p>
              ) : (
                eventos.map((evt, idx) => (
                  <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                    <div className="overflow-hidden pr-2">
                      <span className="bg-cyan-950 text-cyan-400 text-[10px] uppercase font-bold px-1.5 py-0.5 rounded mr-1">
                        {evt.cuenta}
                      </span>
                      <p className="font-medium text-slate-200 text-sm truncate mt-1">{evt.summary}</p>
                      <p className="text-xs text-slate-400 mt-0.5">{new Date(evt.start).toLocaleString()}</p>
                    </div>
                    <a href={evt.link} target="_blank" rel="noreferrer" className="text-xs text-cyan-400 hover:underline shrink-0">
                      Ver
                    </a>
                  </div>
                ))
              )}
            </div>
          </section>

          {/* Bandeja de Entrada */}
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col h-[420px]">
            <h2 className="text-lg font-semibold mb-4 text-cyan-300 flex items-center gap-2 shrink-0">
              ✉️ Bandeja de Entrada (Recientes)
            </h2>
            <div className="overflow-y-auto pr-1 space-y-3 flex-grow custom-scrollbar">
              {cargandoEmails ? (
                <p className="text-slate-400 text-sm">Leyendo correos...</p>
              ) : emails.length === 0 ? (
                <p className="text-slate-400 text-sm">No se encontraron correos recientes.</p>
              ) : (
                emails.map((mail, idx) => (
                  <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                    <div className="overflow-hidden pr-2">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="bg-slate-800 text-cyan-400 text-[10px] uppercase font-bold px-1.5 py-0.5 rounded">
                          {mail.cuenta}
                        </span>
                        <p className="text-xs text-slate-400 truncate">{mail.remitente}</p>
                      </div>
                      <p className="font-medium text-slate-200 text-sm truncate">{mail.asunto}</p>
                    </div>
                    <a href={mail.link} target="_blank" rel="noreferrer" className="text-xs text-cyan-400 hover:underline shrink-0">
                      Abrir
                    </a>
                  </div>
                ))
              )}
            </div>
          </section>

        </div>

        {/* FILA 2: FORMULARIO DE NOTAS + DASHBOARD DE TAREAS (2 Columnas simétricas a ancho completo) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          
          {/* Formulario de Registro */}
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col h-[520px]">
            <h2 className="text-lg font-semibold mb-4 text-cyan-300 shrink-0">✍️ Registrar Nueva Nota / Tarea</h2>
            <form onSubmit={agregarTarea} className="space-y-4 flex-grow flex flex-col justify-between">
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Título</label>
                  <input
                    type="text"
                    placeholder="Ej: Idea brillante, Reunión..."
                    value={titulo}
                    onChange={(e) => setTitulo(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 font-medium"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Cuerpo de la nota (Opcional)</label>
                  <textarea
                    placeholder="Escribe todo el detalle, contenido o apuntes aquí..."
                    value={contenido}
                    onChange={(e) => setContenido(e.target.value)}
                    rows={3}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 resize-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Categoría / Etiqueta</label>
                  <input
                    type="text"
                    list="categorias-sugeridas"
                    placeholder="Escribe una categoría nueva o selecciona una..."
                    value={dominio}
                    onChange={(e) => setDominio(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
                    required
                  />
                  <datalist id="categorias-sugeridas">
                    <option value="Ingeniería e IA" />
                    <option value="Marca Personal" />
                    <option value="Finanzas" />
                    <option value="Salud" />
                    <option value="Diario" />
                  </datalist>
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-cyan-500 hover:bg-cyan-600 font-semibold p-3 rounded-lg text-slate-950 transition text-sm shrink-0"
              >
                Guardar en Base de Datos y Obsidian
              </button>
            </form>
          </section>

          {/* Dashboard de Notas y Tareas con Scroll */}
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col h-[520px]">
            <h2 className="text-lg font-semibold mb-4 text-cyan-300 shrink-0">📋 Dashboard de Notas y Tareas</h2>
            <div className="overflow-y-auto pr-1 space-y-3 flex-grow custom-scrollbar">
              {tareas.length === 0 ? (
                <p className="text-slate-400 text-sm">No hay notas registradas aun.</p>
              ) : (
                tareas.map((t) => (
                  <div key={t.id} className="flex flex-col gap-2 bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                    <div className="flex items-start justify-between">
                      <div className="overflow-hidden pr-2">
                        <p className={`font-medium text-base truncate ${t.estado === "completado" ? "text-slate-500 line-through" : "text-slate-200"}`}>
                          {t.titulo}
                        </p>
                        <span className="inline-block bg-cyan-950 text-cyan-400 text-[10px] px-2 py-0.5 rounded mt-1">
                          {t.dominio || "General"}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5 shrink-0">
                        <button
                          onClick={() => toggleCompletada(t.id)}
                          className={`px-2.5 py-1 rounded text-xs transition ${
                            t.estado === "completado" ? "bg-emerald-950 hover:bg-emerald-900 text-emerald-400" : "bg-slate-800 hover:bg-slate-700 text-slate-300"
                          }`}
                        >
                          {t.estado === "completado" ? "Deshacer" : "Completar"}
                        </button>
                        <button
                          onClick={() => eliminarTarea(t.id)}
                          className="bg-red-950 hover:bg-red-900 text-red-400 px-2.5 py-1 rounded text-xs transition"
                        >
                          Eliminar
                        </button>
                      </div>
                    </div>
                    {t.contenido && (
                      <div className="text-xs text-slate-400 bg-slate-900 p-2.5 rounded border border-slate-800/60 whitespace-pre-wrap">
                        {t.contenido}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </section>

        </div>

      </div>
    </main>
  );
}