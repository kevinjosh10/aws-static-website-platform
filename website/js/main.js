// Add dynamic glass effect to navbar on scroll
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.glass-nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(15, 23, 42, 0.9)';
        nav.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.5)';
    } else {
        nav.style.background = 'rgba(15, 23, 42, 0.7)';
        nav.style.boxShadow = 'none';
    }
});

console.log("AWS Static Website Platform loaded successfully!");
