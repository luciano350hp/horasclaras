import { useState } from "react";
import { api } from "../api.js";
import { useLista } from "../hooks.js";

export default function Horas() {
  const clientes = useLista(api.clientes);
  const horas = useLista(api.horas);
  const [f, setF] = useState({ cliente_id: "", fecha: new Date().toISOString().slice(0, 10), minutos: 60, tipo: "facturable", observacion: "" });
  const [error, setError] = useState("");
  const porHora = clientes.datos.filter((c) => c.tipo === "hora");
  const nombre = (id) => clientes.datos.find((c) => c.id === id)?.nombre ?? id;

  async function crear(e) {
    e.preventDefault();
    setError("");
    try {
      await api.crearHora({ ...f, cliente_id: Number(f.cliente_id), minutos: Number(f.minutos), observacion: f.observacion || null });
      horas.recargar();
    } catch (err) { setError(err.message); }
  }

  return (
    <>
      <form className="card fila" onSubmit={crear}>
        <select value={f.cliente_id} onChange={(e) => setF({ ...f, cliente_id: e.target.value })} required>
          <option value="">Cliente…</option>
          {porHora.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
        <input type="date" value={f.fecha} onChange={(e) => setF({ ...f, fecha: e.target.value })} required />
        <input type="number" min="1" value={f.minutos} onChange={(e) => setF({ ...f, minutos: e.target.value })} required title="Minutos" />
        <select value={f.tipo} onChange={(e) => setF({ ...f, tipo: e.target.value })}>
          <option value="facturable">Facturable</option>
          <option value="planificacion">Planificación (no se cobra)</option>
        </select>
        <input placeholder="Observación" value={f.observacion} onChange={(e) => setF({ ...f, observacion: e.target.value })} />
        <button>Registrar</button>
      </form>
      {(error || horas.error) && <p className="error">{error || horas.error}</p>}
      <table>
        <thead><tr><th>Fecha</th><th>Cliente</th><th>Minutos</th><th>Tipo</th><th>Obs.</th><th /></tr></thead>
        <tbody>
          {horas.datos.map((h) => (
            <tr key={h.id}>
              <td>{h.fecha}</td><td>{nombre(h.cliente_id)}</td><td>{h.minutos}</td>
              <td><span className={"tag " + h.tipo}>{h.tipo}</span></td><td>{h.observacion}</td>
              <td><button className="sec" onClick={async () => { await api.borrarHora(h.id); horas.recargar(); }}>Borrar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
