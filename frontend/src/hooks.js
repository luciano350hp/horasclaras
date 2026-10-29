import { useCallback, useEffect, useState } from "react";

// Carga una lista y permite recargarla; expone el error para mostrarlo en pantalla.
export function useLista(cargar) {
  const [datos, setDatos] = useState([]);
  const [error, setError] = useState("");
  const recargar = useCallback(() => cargar().then(setDatos).catch((e) => setError(e.message)), [cargar]);
  useEffect(() => { recargar(); }, [recargar]);
  return { datos, error, setError, recargar };
}

export const fechaLocal = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
export const mesActual = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
};
export const dinero = (v) => `$ ${Number(v).toLocaleString("es-AR", { minimumFractionDigits: 2 })}`;
