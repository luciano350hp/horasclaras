import { useEffect, useRef, useState } from "react";
import { api } from "../api.js";

const BIENVENIDA = {
  rol: "assistant",
  contenido: "¡Hola! Soy el asistente de HorasClaras. Preguntame cómo se calcula un cobro, qué es una hora no facturable, cuántos clientes podés tener, etc.",
};

export default function Asistente() {
  const [mensajes, setMensajes] = useState([BIENVENIDA]);
  const [texto, setTexto] = useState("");
  const [cid, setCid] = useState(() => localStorage.getItem("chat_cid") || undefined);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");
  const fin = useRef(null);

  useEffect(() => { fin.current?.scrollIntoView({ behavior: "smooth" }); }, [mensajes]);

  async function enviar(e) {
    e.preventDefault();
    const pregunta = texto.trim();
    if (!pregunta || cargando) return;
    setTexto(""); setError(""); setCargando(true);
    setMensajes((m) => [...m, { rol: "user", contenido: pregunta }]);
    try {
      const r = await api.chat(pregunta, cid);
      setCid(r.conversation_id);
      localStorage.setItem("chat_cid", r.conversation_id);
      setMensajes((m) => [...m, { rol: "assistant", contenido: r.respuesta, fuentes: r.fuentes }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <div className="card">
      <h3>Asistente virtual (CU-10)</h3>
      <p className="nota">Preguntale al asistente sobre el sistema. El historial se guarda por conversación.</p>
      <div className="chat">
        {mensajes.map((m, i) => (
          <div key={i} className={"burbuja " + m.rol}>
            {m.contenido}
            {m.fuentes?.length > 0 && <small>Fuentes: {m.fuentes.join(", ")}</small>}
          </div>
        ))}
        {cargando && <div className="burbuja assistant">Pensando…</div>}
        <div ref={fin} />
      </div>
      {error && <p className="error">{error}</p>}
      <form className="fila" onSubmit={enviar}>
        <input className="ancho" placeholder="Escribí tu pregunta…" value={texto} onChange={(e) => setTexto(e.target.value)} maxLength={1000} disabled={cargando} />
        <button disabled={cargando || !texto.trim()}>Enviar</button>
        <button type="button" className="sec" onClick={() => { localStorage.removeItem("chat_cid"); setCid(undefined); setMensajes([BIENVENIDA]); }}>
          Nueva conversación
        </button>
      </form>
    </div>
  );
}