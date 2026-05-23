// Simple interactivity (Tương tác đơn giản)
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DevOps Portfolio loaded!');
    
    // Add animation on scroll (Thêm hiệu ứng khi cuộn)
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});