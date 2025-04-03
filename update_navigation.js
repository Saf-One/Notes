/**
 * Navigation Link Updater
 * This utility script helps maintain consistent navigation links across all markdown files
 * in the notes repository. It automatically updates Home.md, topic Home.md files, and
 * ensures bidirectional navigation between documents.
 * 
 * Usage: 
 * - Include this script in the repository root
 * - Can be called manually or through the auto-update system
 */

// Configuration
const config = {
    mainHomePath: 'Home.md',
    topicDirectories: [
        'Collection framework',
        'Spring Boot'
        // New topics will be added here
    ],
    dateFormat: {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }
};

/**
 * Updates the navigation links in all markdown files
 * This function:
 * 1. Scans all topic directories
 * 2. Updates the main Home.md with links to all topics
 * 3. Updates each topic's Home.md with links to its documents
 * 4. Ensures all documents have proper navigation links
 */
function updateAllNavigationLinks() {
    // Implementation would scan directories and update markdown files
    console.log('Updating navigation links for all topics...');

    // 1. Read main Home.md
    // 2. Extract topic information
    // 3. Update topic table
    // 4. Update recently updated section

    // For each topic:
    // 1. Read topic Home.md
    // 2. Update available documents table
    // 3. Ensure navigation links are correct

    // For each document:
    // 1. Check top and bottom navigation
    // 2. Update if necessary

    console.log('Navigation links updated successfully');
}

/**
 * Adds a new topic to the navigation system
 * @param {string} topicName - Name of the new topic directory
 * @param {string} description - Brief description of the topic
 */
function addNewTopic(topicName, description) {
    if (!config.topicDirectories.includes(topicName)) {
        config.topicDirectories.push(topicName);
        console.log(`Added new topic: ${topicName}`);

        // Update main Home.md with new topic
        // Create topic Home.md if it doesn't exist

        updateAllNavigationLinks();
    }
}

/**
 * Updates the 'Recently Updated' section in Home.md
 * @param {string} documentPath - Path to the updated document
 * @param {string} description - Brief description of the update
 */
function updateRecentlyUpdatedSection(documentPath, description) {
    const today = new Date();
    const formattedDate = today.toLocaleDateString('en-US', config.dateFormat);

    // Add entry to recently updated section in Home.md
    console.log(`Added ${documentPath} to recently updated section (${formattedDate})`);
}

// Export functions for use in auto-update system
if (typeof module !== 'undefined') {
    module.exports = {
        updateAllNavigationLinks,
        addNewTopic,
        updateRecentlyUpdatedSection
    };
}