import { useEffect, useState } from "react";
import { api } from "../api.js";
import { dinero, mesActual } from "../hooks.js";

export default function Calculo() {
  const [mes, setMes] = useState(mesActual());
  const [c, setC] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => { api.calculo(mes).then(setC).catch((e) => setError(e.message)); setError(""); }, [mes]);

  return (
    <>
      <div className="card fila">
        <label>Mes <input type="month" value={mes} onChange={(e) => setMes(e.target.value)} /></label>
      </div>
      {error && <p className="error">{error}</p>}
      {c && (
        <>
          <table>
            <thead><tr><th>Cliente</th><th>Detalle</th><th>No facturable</th><th>Monto</th></tr></thead>
            <tbody>
              {c.clientes.map((f) => (
                <tr key={f.cliente_id}>
                  <td>{f.cliente}</td>
                  <td>{f.tipo === "hora" ? `${(f.minutos_facturables / 60).toFixed(2)} h × ${dinero(f.tarifa)}` : `${f.palabras_totales} palabras (${f.palabras_repetidas} repetidas)`}</td>
                  <td>{f.tipo === "hora" ? `${(f.minutos_no_facturables / 60).toFixed(2)} h` : "-"}</td>
                  <td><b>{dinero(f.monto)}</b></td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="total">Total del mes: {dinero(c.total)}</p>
        </>
      )}
    </>
  );
}
