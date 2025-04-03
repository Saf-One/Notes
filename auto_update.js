// Notes Repository Auto-Update System

/**
 * This script checks for updates in the Notes repository when the Home page is accessed.
 * It compares the local version with the remote version and pulls updates if needed.
 */

(function() {
    // Configuration
    const REPO_URL = 'https://github.com/Saf-One/Notes';
    const REPO_API_URL = 'https://api.github.com/repos/Saf-One/Notes';
    const VERSION_STORAGE_KEY = 'notes_repo_version';
    const LAST_CHECK_KEY = 'notes_repo_last_check';
    const CHECK_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

    // Check if we're running in a browser environment
    if (typeof window === 'undefined' || !window.localStorage) {
        console.log('Auto-update can only run in a browser environment');
        return;
    }

    // Main function to check for updates
    async function checkForUpdates() {
        try {
            // Don't check too frequently
            const lastCheck = parseInt(localStorage.getItem(LAST_CHECK_KEY) || '0');
            const now = Date.now();

            if (now - lastCheck < CHECK_INTERVAL) {
                console.log('Last update check was recent, skipping');
                return;
            }

            localStorage.setItem(LAST_CHECK_KEY, now.toString());

            // Get current commits info
            const response = await fetch(`${REPO_API_URL}/commits`);

            if (!response.ok) {
                throw new Error(`Failed to fetch commits: ${response.status}`);
            }

            const commits = await response.json();

            if (!commits || !commits.length) {
                throw new Error('No commits found');
            }

            const latestCommitSha = commits[0].sha;
            const storedVersion = localStorage.getItem(VERSION_STORAGE_KEY);

            // If no stored version or versions differ, we need to update
            if (!storedVersion || storedVersion !== latestCommitSha) {
                const shouldUpdate = confirm(
                    'There are updates available for the Notes repository. Would you like to update now?'
                );

                if (shouldUpdate) {
                    await updateRepository(latestCommitSha);
                }
            } else {
                console.log('Repository is up to date');
            }
        } catch (error) {
            console.error('Error checking for updates:', error);
        }
    }

    // Function to update the repository
    async function updateRepository(newVersion) {
        try {
            // Show update notification
            const updateNotice = document.createElement('div');
            updateNotice.style.position = 'fixed';
            updateNotice.style.top = '0';
            updateNotice.style.left = '0';
            updateNotice.style.right = '0';
            updateNotice.style.backgroundColor = '#4CAF50';
            updateNotice.style.color = 'white';
            updateNotice.style.padding = '10px';
            updateNotice.style.textAlign = 'center';
            updateNotice.style.zIndex = '1000';
            updateNotice.innerHTML = 'Updating repository, please wait...';

            document.body.appendChild(updateNotice);

            // Fetch the updated pages
            const pagesToUpdate = [
                'Home.md',
                'README.md',
                'note_processor_rules.md',
                'Collection framework/Home.md',
                'Collection framework/Java_Collections_Framework.md',
                'Collection framework/Java_Cursors.md'
            ];

            // We'll use a service worker or similar approach to cache the files
            if ('serviceWorker' in navigator) {
                const registration = await navigator.serviceWorker.register('update-worker.js');

                // Send message to service worker to update files
                const updateMessage = {
                    type: 'UPDATE_FILES',
                    files: pagesToUpdate,
                    repoUrl: REPO_URL
                };

                registration.active.postMessage(updateMessage);

                // Save the new version
                localStorage.setItem(VERSION_STORAGE_KEY, newVersion);

                // Update the notification
                updateNotice.innerHTML = 'Update complete! Reloading page...';

                // Reload the page after a brief delay
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                updateNotice.innerHTML = 'Your browser does not support automatic updates.';
                setTimeout(() => {
                    updateNotice.style.display = 'none';
                }, 3000);
            }
        } catch (error) {
            console.error('Error updating repository:', error);

            const updateNotice = document.querySelector('[style*="position: fixed"]');
            if (updateNotice) {
                updateNotice.style.backgroundColor = '#F44336';
                updateNotice.innerHTML = 'Update failed. Please try again later.';

                setTimeout(() => {
                    updateNotice.style.display = 'none';
                }, 3000);
            }
        }
    }

    // Run the update check when the page loads
    window.addEventListener('load', checkForUpdates);
})();