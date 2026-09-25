// Bump this whenever any cached file changes, so old caches get cleared
// and the "Update available" banner shows up for people with it installed.
var CACHE_NAME = "meditation-timer-v1";

var ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./icons/apple-touch-icon.png"
  // If you add real recordings later (see the plan's audio/ folder),
  // list them here too so they're precached for offline use:
  // "./audio/chime.mp3",
  // "./audio/chime-soft.mp3"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(ASSETS);
    })
  );
  // Deliberately no self.skipWaiting() here: a new version waits until the
  // person taps the "Update available" banner in index.html, so an update
  // never lands mid-session.
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (key) { return key !== CACHE_NAME; })
            .map(function (key) { return caches.delete(key); })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener("fetch", function (event) {
  event.respondWith(
    caches.match(event.request).then(function (cached) {
      return cached || fetch(event.request);
    })
  );
});

self.addEventListener("message", function (event) {
  if (event.data === "SKIP_WAITING") {
    self.skipWaiting();
  }
});
