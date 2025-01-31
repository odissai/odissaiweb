// Navigation and floating navigation functionality
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu functionality
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenu && navLinks) {
        mobileMenu.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !navLinks.contains(e.target)) {
                mobileMenu.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }

    // Handle navigation clicks
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
                
                // Close mobile menu if open
                mobileMenu?.classList.remove('active');
                navLinks?.classList.remove('active');
            }
        });
    });

    const floatNavItems = document.querySelectorAll('.float-nav-item');
    const solutionPanels = document.querySelectorAll('.solution-panel');
    
    const observerOptions = {
        root: null,
        rootMargin: '-50% 0px',
        threshold: 0
    };

    const observerCallback = (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Remove active class from all nav items
                floatNavItems.forEach(item => item.classList.remove('active'));
                
                // Add active class to corresponding nav item
                const activeNav = document.querySelector(`.float-nav-item[data-panel="${entry.target.id}"]`);
                if (activeNav) {
                    activeNav.classList.add('active');
                }
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    solutionPanels.forEach(panel => observer.observe(panel));

    // Contact form handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = {
                name: this.name.value,
                email: this.email.value,
                message: this.message.value
            };
            
            // For now, just show a success message
            alert('Message envoyé ! Nous vous contacterons bientôt.');
            this.reset();
        });
    }
});
