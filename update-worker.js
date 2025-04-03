// Service Worker for Notes Repository Auto-Update

const CACHE_NAME = 'notes-repo-cache-v1';

// Install event - initialize the cache
self.addEventListener('install', event => {
    console.log('Service worker installed');
    self.skipWaiting(); // Ensure activation happens immediately
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service worker activated');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        console.log('Clearing old cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    return self.clients.claim(); // Take control of all clients
});

// Fetch event - serve from cache if available, otherwise fetch from network
self.addEventListener('fetch', event => {
    // Only handle GET requests
    if (event.request.method !== 'GET') return;

    // Only handle markdown and other document files
    const url = new URL(event.request.url);
    if (!url.pathname.endsWith('.md') &&
        !url.pathname.endsWith('.js') &&
        !url.pathname.endsWith('.html')) {
        return;
    }

    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            // Return cached response if available
            if (cachedResponse) {
                return cachedResponse;
            }

            // Otherwise fetch from network and cache the response
            return fetch(event.request).then(response => {
                // Check if we received a valid response
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }

                // Clone the response as it can only be consumed once
                const responseToCache = response.clone();

                caches.open(CACHE_NAME).then(cache => {
                    cache.put(event.request, responseToCache);
                });

                return response;
            });
        })
    );
});

// Message event - handle update requests
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'UPDATE_FILES') {
        console.log('Received update request for files:', event.data.files);
        updateFiles(event.data.files, event.data.repoUrl);
    }
});

// Function to update specific files from the repository
async function updateFiles(files, repoUrl) {
    try {
        // Open the cache
        const cache = await caches.open(CACHE_NAME);

        // Process each file
        for (const file of files) {
            // GitHub raw content URL format
            const rawUrl = `${repoUrl.replace('github.com', 'raw.githubusercontent.com')}/main/${file}`;

            try {
                // Fetch the latest version of the file
                const response = await fetch(rawUrl, {
                    cache: 'no-store', // Bypass the browser cache
                    headers: { 'Cache-Control': 'no-cache' }
                });

                if (!response.ok) {
                    console.error(`Failed to fetch ${file}: ${response.status}`);
                    continue;
                }

                // Cache the updated file
                await cache.put(new Request(`/${file}`), response);
                console.log(`Updated and cached: ${file}`);
            } catch (fileError) {
                console.error(`Error updating file ${file}:`, fileError);
            }
        }

        // Notify all clients that the update is complete
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'UPDATE_COMPLETE'
            });
        });
    } catch (error) {
        console.error('Error updating files:', error);
    }
}