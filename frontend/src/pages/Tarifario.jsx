import { useState } from "react";
import { api } from "../api.js";

export default function Tarifario() {
  const [nombre, setNombre] = useState("");
  return (
    <div className="card">
      <h3>Tarifario en PDF</h3>
      <p>Genera un PDF con tus clientes y tarifas para enviarlo. No se guarda en el servidor.</p>
      <div className="fila">
        <input placeholder="Tu nombre (opcional)" value={nombre} onChange={(e) => setNombre(e.target.value)} />
        <a className="boton" href={api.urlPdf(nombre)} target="_blank" rel="noreferrer">Descargar PDF</a>
      </div>
    </div>
  );
}
