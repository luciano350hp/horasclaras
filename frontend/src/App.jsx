import { useEffect, useState } from "react";
import { api } from "./api.js";
import Clientes from "./pages/Clientes.jsx";
import Horas from "./pages/Horas.jsx";
import Traducciones from "./pages/Traducciones.jsx";
import Calculo from "./pages/Calculo.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Tarifario from "./pages/Tarifario.jsx";
import Waitlist from "./pages/Waitlist.jsx";
import Login from "./pages/Login.jsx";

const TABS = [
  ["dashboard", "Dashboard", Dashboard],
  ["clientes", "Clientes", Clientes],
  ["horas", "Horas", Horas],
  ["traducciones", "Traducciones", Traducciones],
  ["calculo", "Cobro del mes", Calculo],
  ["tarifario", "Tarifario PDF", Tarifario],
  ["waitlist", "Lista de espera", Waitlist],
];

export default function App() {
  const [usuario, setUsuario] = useState(null);
  const [tab, setTab] = useState("dashboard");

  useEffect(() => {
    if (localStorage.getItem("token")) api.me().then(setUsuario).catch(() => localStorage.removeItem("token"));
  }, []);

  if (!usuario) return <Login onEntrar={setUsuario} />;
  const Pagina = TABS.find((t) => t[0] === tab)[2];

  return (
    <div className="app">
      <header>
        <h1>HorasClaras</h1>
        <span>{usuario.email}</span>
        <button className="sec" onClick={() => { localStorage.removeItem("token"); setUsuario(null); }}>
          Salir
        </button>
      </header>
      <nav>
        {TABS.map(([id, nombre]) => (
          <button key={id} className={id === tab ? "activo" : ""} onClick={() => setTab(id)}>
            {nombre}
          </button>
        ))}
      </nav>
      <main><Pagina /></main>
    </div>
  );
}
