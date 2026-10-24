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
    if (confirm("¿Borrar el cliente y todas sus horas?")) { await api.borrarCliente(id); recargar(); }
  }

  return (
    <>
      <form className="card fila" onSubmit={crear}>
        <input placeholder="Nombre" value={f.nombre} onChange={(e) => setF({ ...f, nombre: e.target.value })} required />
        <select value={f.tipo} onChange={(e) => setF({ ...f, tipo: e.target.value })}>
          <option value="hora">Por hora</option>
          <option value="palabra">Por palabra</option>
        </select>
        <input type="number" step="0.01" min="0.01" placeholder="Tarifa" value={f.tarifa} onChange={(e) => setF({ ...f, tarifa: e.target.value })} required />
        {f.tipo === "palabra" && (
          <input type="number" min="0" max="100" placeholder="% desc. repetidas" value={f.descuento_repeticion} onChange={(e) => setF({ ...f, descuento_repeticion: e.target.value })} />
        )}
        <button>Agregar cliente</button>
      </form>
      {error && <p className="error">{error}</p>}
      <table>
        <thead><tr><th>Cliente</th><th>Modalidad</th><th>Tarifa</th><th>Desc.</th><th /></tr></thead>
        <tbody>
          {datos.map((c) => (
            <tr key={c.id}>
              <td>{c.nombre}</td>
              <td>{c.tipo === "hora" ? "Por hora" : "Por palabra"}</td>
              <td>{dinero(c.tarifa)}</td>
              <td>{c.tipo === "palabra" ? `${Number(c.descuento_repeticion)} %` : "-"}</td>
              <td><button className="sec" onClick={() => borrar(c.id)}>Borrar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="nota">Máximo 10 clientes.</p>
    </>
  );
}
