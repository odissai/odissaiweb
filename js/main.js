document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu functionality
    const mobileMenuButton = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuButton && navLinks) {
        mobileMenuButton.addEventListener('click', () => {
            // Toggle mobile menu
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            
            // Animate hamburger to X
            mobileMenuButton.classList.toggle('active');
            
            // Add mobile-specific styles when menu is open
            if (navLinks.style.display === 'flex') {
                navLinks.style.position = 'absolute';
                navLinks.style.top = '80px'; // header height
                navLinks.style.left = '0';
                navLinks.style.right = '0';
                navLinks.style.backgroundColor = 'var(--background-color)';
                navLinks.style.flexDirection = 'column';
                navLinks.style.padding = '1rem';
                navLinks.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
            }
        });

        // Close mobile menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navLinks.style.display = 'none';
                    mobileMenuButton.classList.remove('active');
                }
            });
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                navLinks.style.display = 'flex';
                navLinks.style.position = 'static';
                navLinks.style.padding = '0';
                navLinks.style.boxShadow = 'none';
                navLinks.style.flexDirection = 'row';
            } else {
                navLinks.style.display = 'none';
                mobileMenuButton.classList.remove('active');
            }
        });
    }

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll animation for solution cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.solution-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});
