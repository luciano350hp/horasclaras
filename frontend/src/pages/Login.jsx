import { useState } from "react";
import { api } from "../api.js";

export default function Login({ onEntrar }) {
  const [modo, setModo] = useState("login"); // "login" | "registro" | "reset"
  const [f, setF] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  async function enviar(e) {
    e.preventDefault();
    setError(""); setOk("");
    try {
      if (modo === "registro") {
        await api.registro(f);
        const { access_token } = await api.login(f);
        localStorage.setItem("token", access_token);
        onEntrar(await api.me());
      } else if (modo === "reset") {
        await api.resetPassword(f);
        setOk("Contraseña actualizada. Ahora ingresá con la nueva.");
        setModo("login");
        setF({ email: f.email, password: "" });
      } else {
        const { access_token } = await api.login(f);
        localStorage.setItem("token", access_token);
        onEntrar(await api.me());
      }
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form className="login card" onSubmit={enviar}>
      <h1>HorasClaras</h1>
      <p>
        {modo === "login" ? "Ingresá a tu cuenta" :
         modo === "registro" ? "Creá tu cuenta" :
         "Restablecer contraseña"}
      </p>
      <input type="email" placeholder="Email" value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} required />
      {modo !== "reset" && (
        <input type="password" placeholder="Contraseña (mín. 6 caracteres)" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} required minLength={6} />
      )}
      {modo === "reset" && (
        <input type="password" placeholder="Nueva contraseña (mín. 6 caracteres)" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} required minLength={6} />
      )}
      {error && <p className="error">{error}</p>}
      {ok && <p className="ok">{ok}</p>}
      <button>
        {modo === "login" ? "Entrar" : modo === "registro" ? "Registrarme" : "Actualizar contraseña"}
      </button>
      {modo === "login" && (
        <>
          <button type="button" className="sec" onClick={() => setModo("registro")}>
            No tengo cuenta → Registrarme
          </button>
          <button type="button" className="sec" onClick={() => setModo("reset")}>
            Olvidé mi contraseña
          </button>
        </>
      )}
      {(modo === "registro" || modo === "reset") && (
        <button type="button" className="sec" onClick={() => setModo("login")}>
          Volver al login
        </button>
      )}
    </form>
  );
}