import { useState } from "react";
import { api } from "../api.js";

export default function Waitlist() {
  const [email, setEmail] = useState("");
  const [msg, setMsg] = useState({ ok: true, texto: "" });

  async function enviar(e) {
    e.preventDefault();
    try {
      await api.waitlist(email);
      setMsg({ ok: true, texto: "¡Listo! Te anotamos en la lista de espera." });
      setEmail("");
    } catch (err) { setMsg({ ok: false, texto: err.message }); }
  }

  return (
    <div className="card">
      <h3>Lista de espera</h3>
      <p className="nota">Anotá tu email para enterarte cuando salgan las novedades. Si el email ya está anotado, te avisa.</p>
      <form className="fila" onSubmit={enviar} style={{ marginTop: 12 }}>
        <input type="email" placeholder="tu@email.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <button>Anotarme</button>
      </form>
      {msg.texto && <p className={msg.ok ? "ok" : "error"} style={{ marginTop: 12 }}>{msg.texto}</p>}
    </div>
  );
}