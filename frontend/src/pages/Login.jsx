import { useState } from "react";
import { api } from "../api.js";

export default function Login({ onEntrar }) {
  const [modo, setModo] = useState("login");
  const [f, setF] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  async function enviar(e) {
    e.preventDefault();
    setError("");
    try {
      if (modo === "registro") await api.registro(f);
      const { access_token } = await api.login(f);
      localStorage.setItem("token", access_token);
      onEntrar(await api.me());
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form className="login card" onSubmit={enviar}>
      <h1>HorasClaras</h1>
      <p>{modo === "login" ? "Ingresá a tu cuenta" : "Creá tu cuenta"}</p>
      <input type="email" placeholder="Email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} required />
      <input type="password" placeholder="Contraseña (mín. 6 caracteres)" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} required minLength={6} />
      {error && <p className="error">{error}</p>}
      <button>{modo === "login" ? "Entrar" : "Registrarme"}</button>
      <button type="button" className="sec" onClick={() => setModo(modo === "login" ? "registro" : "login")}>
        {modo === "login" ? "No tengo cuenta → Registrarme" : "Ya tengo cuenta → Entrar"}
      </button>
    </form>
  );
}