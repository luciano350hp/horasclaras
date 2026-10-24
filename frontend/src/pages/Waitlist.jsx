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
    <form className="card" onSubmit={enviar}>
      <h3>Lista de espera</h3>
      <p>Anotá tu email para enterarte cuando salgan las novedades.</p>
      <div className="fila">
        <input type="email" placeholder="tu@email.com" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <button>Anotarme</button>
      </div>
      {msg.texto && <p className={msg.ok ? "ok" : "error"}>{msg.texto}</p>}
    </form>
  );
}
