import axios from "axios";

// Change this if your API runs elsewhere:
const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function optimizeFlight({ origin, destinations, currency = "USD" }) {
  const res = await axios.post(`${API_BASE}/optimize`, {
    origin,
    destinations,
    currency,
  });
  return res.data;
}
