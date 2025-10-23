import { useState } from "react";
import { optimizeFlight } from "./api";
import { Spinner } from "./components/Spinner";

export default function App() {
  const [origin, setOrigin] = useState("");
  const [destinations, setDestinations] = useState("");
  const [currency, setCurrency] = useState("USD");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const destList = destinations.split(",").map(s => s.trim()).filter(Boolean);
      const data = await optimizeFlight({ origin, destinations: destList, currency });
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50 text-neutral-900 dark:bg-neutral-900 dark:text-neutral-100">
      <header className="sticky top-0 z-10 border-b border-neutral-200/70 bg-white/70 backdrop-blur dark:border-neutral-800 dark:bg-neutral-900/70">
        <div className="mx-auto max-w-6xl px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold tracking-tight">
              <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                Flight Optimizer
              </span>
            </h1>
            <p className="text-sm text-neutral-500 dark:text-neutral-400">
              Best value by <strong>$ / km</strong>
            </p>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 grid gap-6 lg:grid-cols-2">
        <section className="rounded-2xl border border-neutral-200/70 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <div className="p-6">
            <h2 className="text-lg font-semibold">Search</h2>
            <p className="mt-1 text-sm text-neutral-500 dark:text-neutral-400">
              Enter an origin city and one or more destinations (comma separated).
            </p>

            <form onSubmit={onSubmit} className="mt-6 space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium">From (city)</label>
                <input
                  value={origin}
                  onChange={(e) => setOrigin(e.target.value)}
                  placeholder="e.g., London"
                  required
                  className="w-full rounded-xl border border-neutral-300 bg-white px-3 py-2 outline-none
                             ring-blue-500/0 transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40
                             dark:border-neutral-700 dark:bg-neutral-900"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium">To (cities)</label>
                <input
                  value={destinations}
                  onChange={(e) => setDestinations(e.target.value)}
                  placeholder="e.g., Paris, Berlin, Rome"
                  required
                  className="w-full rounded-xl border border-neutral-300 bg-white px-3 py-2 outline-none
                             ring-blue-500/0 transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40
                             dark:border-neutral-700 dark:bg-neutral-900"
                />
                <p className="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
                  Separate multiple cities with commas.
                </p>
              </div>

              <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                <div className="sm:col-span-2">
                  <label className="mb-1 block text-sm font-medium">Currency</label>
                  <input
                    value={currency}
                    onChange={(e) => setCurrency(e.target.value)}
                    className="w-full rounded-xl border border-neutral-300 bg-white px-3 py-2 outline-none
                               focus:border-blue-500 focus:ring-2 focus:ring-blue-500/40
                               dark:border-neutral-700 dark:bg-neutral-900"
                  />
                </div>

                <div className="flex items-end">
                  <button
                    type="submit"
                    disabled={loading}
                    className="inline-flex w-full items-center justify-center gap-2 rounded-xl
                               bg-blue-600 px-4 py-2.5 font-semibold text-white shadow
                               transition hover:bg-blue-700 disabled:opacity-60"
                  >
                    {loading && <Spinner />}
                    {loading ? "Searching…" : "Find Best $ / km"}
                  </button>
                </div>
              </div>
            </form>

            {error && (
              <div className="mt-4 rounded-xl border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-700
                              dark:border-red-800/60 dark:bg-red-900/30 dark:text-red-200">
                {error}
              </div>
            )}
          </div>
        </section>

        <section className="rounded-2xl border border-neutral-200/70 bg-white shadow-sm dark:border-neutral-800 dark:bg-neutral-950">
          <div className="p-6">
            <h2 className="text-lg font-semibold">Results</h2>

            {!result && !loading && (
              <p className="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
                Submit a search to see the best destination.
              </p>
            )}

            {loading && (
              <div className="mt-4 flex items-center gap-2 text-neutral-500 dark:text-neutral-400">
                <Spinner />
                <span>Crunching numbers…</span>
              </div>
            )}

            {result && (
              <>
                <div className="mt-4 flex flex-wrap items-center gap-3">
                  <span className="inline-flex items-center gap-2 rounded-full bg-green-600/10 px-3 py-1
                                   text-sm font-medium text-green-700 ring-1 ring-inset ring-green-600/20
                                   dark:text-green-300">
                    Best: <span className="font-semibold">{result.best_destination}</span>
                  </span>
                  <span className="inline-flex items-center rounded-full bg-blue-600/10 px-3 py-1
                                   text-sm font-medium text-blue-700 ring-1 ring-inset ring-blue-600/20
                                   dark:text-blue-300">
                    ${result.price_per_km.toFixed(4)}/km
                  </span>
                </div>

                <div className="mt-4 overflow-x-auto">
                  <table className="min-w-full border-separate border-spacing-y-2">
                    <thead>
                      <tr className="text-left text-sm text-neutral-500 dark:text-neutral-400">
                        <th className="px-3 py-2">City</th>
                        <th className="px-3 py-2">Code</th>
                        <th className="px-3 py-2">Price</th>
                        <th className="px-3 py-2">Distance</th>
                        <th className="px-3 py-2">$ / km</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.details
                        .slice()
                        .sort((a, b) => a.price_per_km - b.price_per_km)
                        .map((r) => (
                          <tr key={r.code} className="rounded-xl">
                            <td className="px-3 py-2">
                              <div className="font-medium">{r.destination}</div>
                            </td>
                            <td className="px-3 py-2">
                              <span className="rounded-md bg-neutral-100 px-2 py-1 text-xs font-mono
                                               dark:bg-neutral-800">
                                {r.code}
                              </span>
                            </td>
                            <td className="px-3 py-2">${r.price.toFixed(2)}</td>
                            <td className="px-3 py-2">{Math.round(r.distance_km)} km</td>
                            <td className="px-3 py-2 font-semibold">
                              ${r.price_per_km.toFixed(4)}
                            </td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </div>
        </section>
      </main>

      <footer className="py-8 text-center text-xs text-neutral-500 dark:text-neutral-400">
        Built for the B12 Flight Optimization take-home.
      </footer>
    </div>
  );
}
