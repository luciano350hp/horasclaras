// Cliente HTTP minimo hacia el backend FastAPI.
export const BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function pedir(ruta, opciones = {}) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) };
  const r = await fetch(BASE + ruta, { headers, ...opciones });
  if (r.status === 204) return null;
  const cuerpo = await r.json().catch(() => ({}));
  if (!r.ok) {
    const d = cuerpo.detail;
    throw new Error(typeof d === "string" ? d : Array.isArray(d) ? d.map((e) => e.msg).join(", ") : "Error " + r.status);
  }
  return cuerpo;
}

const post = (ruta, datos) => pedir(ruta, { method: "POST", body: JSON.stringify(datos) });

export const api = {
  registro: (d) => post("/api/auth/registro", d),
  login: (d) => post("/api/auth/login", d),
  me: () => pedir("/api/auth/me"),
  clientes: () => pedir("/api/clientes/"),
  crearCliente: (d) => post("/api/clientes/", d),
  borrarCliente: (id) => pedir(`/api/clientes/${id}`, { method: "DELETE" }),
  horas: () => pedir("/api/horas/"),
  crearHora: (d) => post("/api/horas/", d),
  borrarHora: (id) => pedir(`/api/horas/${id}`, { method: "DELETE" }),
  traducciones: () => pedir("/api/traducciones/"),
  crearTraduccion: (d) => post("/api/traducciones/", d),
  borrarTraduccion: (id) => pedir(`/api/traducciones/${id}`, { method: "DELETE" }),
  calculo: (mes) => pedir(`/api/calculos/${mes}`),
  dashboard: (mes) => pedir(`/api/dashboard/${mes}`),
  chat: (mensaje, conversation_id) => post("/api/chat", { mensaje, conversation_id }),
  waitlist: (email) => post("/api/waitlist", { email }),
  urlPdf: (nombre) => `${BASE}/api/tarifario/pdf?profesional=${encodeURIComponent(nombre || "")}`,
};
