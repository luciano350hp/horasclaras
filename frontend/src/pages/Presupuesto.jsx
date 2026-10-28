import { useState } from "react";
import { api } from "../api.js";
import { useLista } from "../hooks.js";
import { dinero } from "../hooks.js";

const contar = (t) => (t.match(/[\p{L}\p{N}]+(?:['’][\p{L}\p{N}]+)*/gu) || []).length;

export default function Presupuesto() {
  const clientes = useLista(api.clientes);
  const [clienteId, setClienteId] = useState("");
  const [texto, setTexto] = useState("");
  const [r, setR] = useState(null);
  const [error, setError] = useState("");
  const porPalabra = clientes.datos.filter((c) => c.tipo === "palabra");

  async function calcular(e) {
    e.preventDefault();
    setError("");
    setR(null);
    try {
      setR(await api.presupuesto({ texto, cliente_id: Number(clienteId) }));
    } catch (err) { setError(err.message); }
  }

  return (
    <>
      <form className="card" onSubmit={calcular}>
        <div className="fila">
          <select value={clienteId} onChange={(e) => setClienteId(e.target.value)} required>
            <option value="">Cliente (solo por palabra)…</option>
            {porPalabra.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
          </select>
          <span className="nota">{contar(texto)} palabras</span>
        </div>
        <textarea
          rows="8"
          placeholder="Pegá acá el texto a traducir…"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          required
        />
        <button disabled={!texto.trim() || !clienteId}>Calcular presupuesto</button>
      </form>
      {error && <p className="error">{error}</p>}
      {porPalabra.length === 0 && clientes.datos.length >= 0 && (
        <div className="card vacio"><b>No hay clientes por palabra</b>Creá uno en la pestaña Clientes para poder presupuestar.</div>
      )}
      {r && (
        <div className="card resultado">
          <h3>Presupuesto para {r.cliente}</h3>
          <div className="kpis">
            <div className="kpi"><small>Palabras totales</small><b>{r.palabras_totales}</b></div>
            <div className="kpi"><small>Palabras repetidas</small><b>{r.palabras_repetidas}</b></div>
            <div className="kpi"><small>Tarifa por palabra</small><b>{dinero(r.tarifa)}</b></div>
            <div className="kpi"><small>Descuento en repetidas</small><b>{Number(r.descuento_repeticion)} %</b></div>
          </div>
          <p className="nota">Sin descuento: {dinero(r.monto_sin_descuento)}</p>
          <p className="total">Precio: {dinero(r.monto)}</p>
          {r.segmentos_repetidos.length > 0 && (
            <>
              <h3>Frases repetidas detectadas</h3>
              <ul>{r.segmentos_repetidos.map((s, i) => <li key={i}>{s}</li>)}</ul>
            </>
          )}
        </div>
      )}
    </>
  );
}
