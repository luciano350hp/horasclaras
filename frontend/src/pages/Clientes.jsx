import { useState } from "react";
import { api } from "../api.js";
import { dinero, useLista } from "../hooks.js";

const VACIO = { nombre: "", tipo: "hora", tarifa: "", descuento_repeticion: "50" };

export default function Clientes() {
  const { datos, error, setError, recargar } = useLista(api.clientes);
  const [f, setF] = useState(VACIO);

  async function crear(e) {
    e.preventDefault();
    setError("");
    try {
      await api.crearCliente(f);
      setF(VACIO);
      recargar();
    } catch (err) { setError(err.message); }
  }
  async function borrar(id) {
    if (confirm("¿Borrar el cliente y todas sus horas/traducciones?")) { await api.borrarCliente(id); recargar(); }
  }

  return (
    <>
      <form className="card fila" onSubmit={crear}>
        <input placeholder="Nombre del cliente" value={f.nombre} onChange={(e) => setF({ ...f, nombre: e.target.value })} required />
        <select value={f.tipo} onChange={(e) => setF({ ...f, tipo: e.target.value })}>
          <option value="hora">Por hora (clases)</option>
          <option value="palabra">Por palabra (traducciones)</option>
        </select>
        <input type="number" step="0.01" min="0.01" placeholder="Tarifa (ej: 25.00)" value={f.tarifa} onChange={(e) => setF({ ...f, tarifa: e.target.value })} required />
        {f.tipo === "palabra" && (
          <input type="number" min="0" max="100" placeholder="% desc. palabras repetidas" value={f.descuento_repeticion} onChange={(e) => setF({ ...f, descuento_repeticion: e.target.value })} />
        )}
        <button>Agregar cliente</button>
      </form>
      {error && <p className="error">{error}</p>}
      {datos.length === 0 ? (
        <div className="card vacio"><b>Sin clientes todavía</b>Creá tu primer cliente arriba.</div>
      ) : (
        <table>
          <thead><tr><th>Nombre</th><th>Modalidad de cobro</th><th>Tarifa</th><th>Desc. repetidas</th><th>Acciones</th></tr></thead>
          <tbody>
            {datos.map((c) => (
              <tr key={c.id}>
                <td><b>{c.nombre}</b></td>
                <td><span className={"badge " + c.tipo}>{c.tipo === "hora" ? "🕐 Por hora" : "📝 Por palabra"}</span></td>
                <td>{dinero(c.tarifa)} {c.tipo === "hora" ? "/hora" : "/palabra"}</td>
                <td>{c.tipo === "palabra" ? `${Number(c.descuento_repeticion)} %` : "—"}</td>
                <td><button className="sec" onClick={() => borrar(c.id)}>Borrar</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div className="card" style={{ background: "#f9fafb", padding: 14 }}>
        <p style={{ margin: 0, fontSize: 13, color: "var(--tinta-suave)" }}>
          <b style={{ color: "var(--tinta)" }}>Tipos de cliente:</b>{" "}
          <span className="badge hora" style={{ marginLeft: 6 }}>🕐 Por hora</span> = clases (se cobra por minutos trabajados) &nbsp;·&nbsp;
          <span className="badge palabra" style={{ marginLeft: 6 }}>📝 Por palabra</span> = traducciones (se cobra por palabras, con descuento en las repetidas)
        </p>
      </div>
      <p className="nota" style={{ marginTop: 8 }}>Máximo 10 clientes. La tarifa debe ser mayor a 0. El descuento por repetición aplica solo a las palabras repetidas.</p>
    </>
  );
}