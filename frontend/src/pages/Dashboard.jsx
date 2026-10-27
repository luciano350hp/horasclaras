import { useEffect, useState } from "react";
import { api } from "../api.js";
import { dinero, mesActual } from "../hooks.js";

export default function Dashboard() {
  const [mes, setMes] = useState(mesActual());
  const [d, setD] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => { setError(""); api.dashboard(mes).then(setD).catch((e) => setError(e.message)); }, [mes]);
  const max = d ? Math.max(...d.clientes.map((c) => Number(c.monto)), 1) : 1;

  return (
    <>
      <div className="card fila">
        <label>Mes a consultar <input type="month" value={mes} onChange={(e) => setMes(e.target.value)} /></label>
      </div>
      {error && <p className="error">{error}</p>}
      {d && (
        <>
          <div className="kpis">
            <div className="kpi"><small>Total facturado</small><b>{dinero(d.total_facturado)}</b></div>
            <div className="kpi"><small>Horas facturables</small><b>{d.horas_facturables} h</b></div>
            <div className="kpi"><small>Horas no facturables</small><b>{d.horas_no_facturables} h</b></div>
            <div className="kpi"><small>Palabras traducidas</small><b>{d.palabras_traducidas}</b></div>
            <div className="kpi"><small>Mejor cliente</small><b>{d.mejor_cliente ?? "—"}</b></div>
          </div>
          <div className="card">
            <h3>Facturación por cliente</h3>
            {d.clientes.length === 0 ? (
              <div className="vacio"><b>Sin datos</b>No hay actividad registrada para este mes.</div>
            ) : (
              d.clientes.map((c) => (
                <div key={c.cliente_id} className="barra">
                  <span>{c.cliente}</span>
                  <div><i style={{ width: `${(Number(c.monto) / max) * 100}%` }} /></div>
                  <span>{dinero(c.monto)}</span>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </>
  );
}