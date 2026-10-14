/* Rafiq service worker: works offline after the first visit. Bump VERSION when you publish changes. */
const VERSION = "rafiq-v5";
const QURAN_CACHE = "rafiq-quran-1";   // Quran files never change: kept across app versions
const SHELL = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "icons/apple-touch-icon.png", "icons/favicon-32.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION && k !== "rafiq-fonts" && k !== QURAN_CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
const networkFirst = (req, key) => fetch(req).then(res => { if (res.ok) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(key, copy)); } return res; })
  .catch(() => caches.match(key));
self.addEventListener("fetch", e => {
  const req = e.request; if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (req.mode === "navigate") { e.respondWith(networkFirst(req, "index.html")); return; }   // the app: newest when online
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {   // fonts: cached after first load
    e.respondWith(caches.open("rafiq-fonts").then(c => c.match(req).then(hit => hit || fetch(req).then(res => { c.put(req, res.clone()); return res; }))));
    return;
  }
  if (url.origin !== location.origin) return;
  if (url.pathname.endsWith("/reflections.json")) { e.respondWith(networkFirst(req, "reflections.json")); return; }   // today's reflection
  if (/\/quran\/\d+\.json$/.test(url.pathname)) {                                                                // a surah: once loaded, always offline
    e.respondWith(caches.open(QURAN_CACHE).then(c => c.match(req).then(hit => hit || fetch(req).then(res => { if (res.ok) c.put(req, res.clone()); return res; }))));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});
