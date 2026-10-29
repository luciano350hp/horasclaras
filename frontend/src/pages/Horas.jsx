import { useState } from "react";
import { api } from "../api.js";
import { useLista } from "../hooks.js";

export default function Horas() {
  const clientes = useLista(api.clientes);
  const horas = useLista(api.horas);
  const [f, setF] = useState({ cliente_id: "", fecha: new Date().toISOString().slice(0, 10), horas: 1, tipo: "facturable", observacion: "" });
  const [error, setError] = useState("");
  const porHora = clientes.datos.filter((c) => c.tipo === "hora");
  const nombre = (id) => clientes.datos.find((c) => c.id === id)?.nombre ?? id;

  async function crear(e) {
    e.preventDefault();
    setError("");
    try {
      const { horas: hs, ...resto } = f;
      await api.crearHora({ ...resto, cliente_id: Number(f.cliente_id), minutos: Math.round(Number(hs) * 60), observacion: f.observacion || null });
      horas.recargar();
      setF({ ...f, horas: 1, observacion: "" });
    } catch (err) { setError(err.message); }
  }

  return (
    <>
      <form className="card fila" onSubmit={crear}>
        <select value={f.cliente_id} onChange={(e) => setF({ ...f, cliente_id: e.target.value })} required>
          <option value="">Cliente (solo por hora)…</option>
          {porHora.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
        <input type="date" value={f.fecha} onChange={(e) => setF({ ...f, fecha: e.target.value })} required />
        <input type="number" min="0.25" step="0.25" value={f.horas} onChange={(e) => setF({ ...f, horas: e.target.value })} required title="Horas (ej: 1.5 = una hora y media)" placeholder="Horas" />
        <select value={f.tipo} onChange={(e) => setF({ ...f, tipo: e.target.value })}>
          <option value="facturable">Facturable (se cobra)</option>
          <option value="planificacion">Planificación (no se cobra)</option>
        </select>
        <input placeholder="Observación (opcional)" value={f.observacion} onChange={(e) => setF({ ...f, observacion: e.target.value })} />
        <button>Registrar hora</button>
      </form>
      {(error || horas.error) && <p className="error">{error || horas.error}</p>}
      {horas.datos.length === 0 ? (
        <div className="card vacio"><b>Sin horas registradas</b>Registra tu primera hora arriba.</div>
      ) : (
        <table>
          <thead><tr><th>Fecha</th><th>Cliente</th><th>Horas</th><th>Tipo</th><th>Observación</th><th>Acciones</th></tr></thead>
          <tbody>
            {horas.datos.map((h) => (
              <tr key={h.id}>
                <td>{h.fecha}</td><td><b>{nombre(h.cliente_id)}</b></td><td>{(h.minutos / 60).toFixed(2)} h</td>
                <td><span className={"tag " + h.tipo}>{h.tipo === "facturable" ? "✅ Facturable" : "📋 Planificación"}</span></td>
                <td>{h.observacion || "—"}</td>
                <td><button className="sec" onClick={async () => { await api.borrarHora(h.id); horas.recargar(); }}>Borrar</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}