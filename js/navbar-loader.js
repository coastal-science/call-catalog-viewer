/**
 * Navbar Loader
 * Dynamically loads the navbar.html file and inserts it into the page
 * 
 * Designed for a flat directory structure where all HTML pages are in the project root.
 * All navbar links use simple filenames (e.g., "home.html", "faq.html").
 */
(function() {
    // Function to load navbar
    function loadNavbar() {
        const navbarContainer = document.getElementById('navbar-container');
        if (!navbarContainer) {
            console.warn('Navbar container not found. Make sure you have <div id="navbar-container"></div> in your HTML.');
            return;
        }

        // Flat structure: navbar.html is in the same directory as all pages
        const navbarPath = 'navbar.html?v=random';
        
        fetch(navbarPath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load navbar');
                }
                return response.text();
            })
            .then(html => {
                navbarContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading navbar:', error);
                // Fallback: show a message or basic navbar
                navbarContainer.innerHTML = '<div style="padding: 10px; background: #f0f0f0; color: #333;">Navbar could not be loaded. Please refresh the page.</div>';
            });
    }

    // Load navbar when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadNavbar);
    } else {
        // DOM is already ready
        loadNavbar();
    }
})();

