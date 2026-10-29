import { useState } from "react";
import { api } from "../api.js";
import { fechaLocal, useLista } from "../hooks.js";

export default function Traducciones() {
  const clientes = useLista(api.clientes);
  const trads = useLista(api.traducciones);
  const [f, setF] = useState({ cliente_id: "", fecha: fechaLocal(), palabras_totales: "", palabras_repetidas: 0, descripcion: "" });
  const [error, setError] = useState("");
  const porPalabra = clientes.datos.filter((c) => c.tipo === "palabra");
  const nombre = (id) => clientes.datos.find((c) => c.id === id)?.nombre ?? id;

  async function crear(e) {
    e.preventDefault();
    setError("");
    try {
      await api.crearTraduccion({
        ...f,
        cliente_id: Number(f.cliente_id),
        palabras_totales: Number(f.palabras_totales),
        palabras_repetidas: Number(f.palabras_repetidas),
        descripcion: f.descripcion || null,
      });
      trads.recargar();
      setF({ ...f, palabras_totales: "", palabras_repetidas: 0, descripcion: "" });
    } catch (err) { setError(err.message); }
  }

  return (
    <>
      <form className="card fila" onSubmit={crear}>
        <select value={f.cliente_id} onChange={(e) => setF({ ...f, cliente_id: e.target.value })} required>
          <option value="">Cliente (solo por palabra)…</option>
          {porPalabra.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
        <input type="date" value={f.fecha} onChange={(e) => setF({ ...f, fecha: e.target.value })} required />
        <input type="number" min="1" placeholder="Palabras totales" value={f.palabras_totales} onChange={(e) => setF({ ...f, palabras_totales: e.target.value })} required />
        <input type="number" min="0" placeholder="Palabras repetidas" value={f.palabras_repetidas} onChange={(e) => setF({ ...f, palabras_repetidas: e.target.value })} />
        <input placeholder="Descripción (opcional)" value={f.descripcion} onChange={(e) => setF({ ...f, descripcion: e.target.value })} />
        <button>Registrar traducción</button>
      </form>
      {(error || trads.error) && <p className="error">{error || trads.error}</p>}
      {trads.datos.length === 0 ? (
        <div className="card vacio"><b>Sin traducciones registradas</b>Registra tu primera traducción arriba.</div>
      ) : (
        <table>
          <thead><tr><th>Fecha</th><th>Cliente</th><th>Palabras totales</th><th>Palabras repetidas</th><th>Descripción</th><th>Acciones</th></tr></thead>
          <tbody>
            {trads.datos.map((t) => (
              <tr key={t.id}>
                <td>{t.fecha}</td><td><b>{nombre(t.cliente_id)}</b></td><td>{t.palabras_totales}</td><td>{t.palabras_repetidas}</td><td>{t.descripcion || "—"}</td>
                <td><button className="sec" onClick={async () => { await api.borrarTraduccion(t.id); trads.recargar(); }}>Borrar</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}