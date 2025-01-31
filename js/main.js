document.addEventListener('DOMContentLoaded', () => {
    // Handle smooth scroll for all navigation links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Handle scroll indicator
    document.querySelector('.scroll-indicator').addEventListener('click', (e) => {
        e.preventDefault();
        const solutions = document.querySelector('#solutions');
        if (solutions) {
            solutions.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
