import { useState } from "react";
import { api } from "../api.js";
import { useLista } from "../hooks.js";

export default function Traducciones() {
  const clientes = useLista(api.clientes);
  const trads = useLista(api.traducciones);
  const [f, setF] = useState({ cliente_id: "", fecha: new Date().toISOString().slice(0, 10), palabras_totales: "", palabras_repetidas: 0, descripcion: "" });
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
    } catch (err) { setError(err.message); }
  }

  return (
    <>
      <form className="card fila" onSubmit={crear}>
        <select value={f.cliente_id} onChange={(e) => setF({ ...f, cliente_id: e.target.value })} required>
          <option value="">Cliente…</option>
          {porPalabra.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
        </select>
        <input type="date" value={f.fecha} onChange={(e) => setF({ ...f, fecha: e.target.value })} required />
        <input type="number" min="1" placeholder="Palabras totales" value={f.palabras_totales} onChange={(e) => setF({ ...f, palabras_totales: e.target.value })} required />
        <input type="number" min="0" placeholder="Repetidas" value={f.palabras_repetidas} onChange={(e) => setF({ ...f, palabras_repetidas: e.target.value })} />
        <input placeholder="Descripción" value={f.descripcion} onChange={(e) => setF({ ...f, descripcion: e.target.value })} />
        <button>Registrar</button>
      </form>
      {(error || trads.error) && <p className="error">{error || trads.error}</p>}
      <table>
        <thead><tr><th>Fecha</th><th>Cliente</th><th>Totales</th><th>Repetidas</th><th>Descripción</th><th /></tr></thead>
        <tbody>
          {trads.datos.map((t) => (
            <tr key={t.id}>
              <td>{t.fecha}</td><td>{nombre(t.cliente_id)}</td><td>{t.palabras_totales}</td><td>{t.palabras_repetidas}</td><td>{t.descripcion}</td>
              <td><button className="sec" onClick={async () => { await api.borrarTraduccion(t.id); trads.recargar(); }}>Borrar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
