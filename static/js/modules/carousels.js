export function initInstagramCarousels() {
    initWelcomeCarousel();
    initMuralCarousel();
}

function handleUserActivity(container, timeoutDuration = 2500) {
    if (!container) return;
    let timer = null;

    function activate() {
        container.classList.add('user-active');
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
            container.classList.remove('user-active');
        }, timeoutDuration);
    }

    ['scroll', 'touchstart', 'touchmove', 'mousemove', 'click'].forEach(evt => {
        container.addEventListener(evt, activate, { passive: true });
    });
}

export function initWelcomeCarousel() {
    const track = document.getElementById('welcome-carousel-track');
    const box = document.getElementById('welcome-insta-carousel');
    const currIdxSpan = document.getElementById('welcome-curr-idx');
    const totalIdxSpan = document.getElementById('welcome-total-idx');
    const prevBtn = document.getElementById('welcome-prev-arrow');
    const nextBtn = document.getElementById('welcome-next-arrow');

    if (!track) return;
    if (box) handleUserActivity(box);

    function updateCounter() {
        const slides = track.querySelectorAll('.insta-carousel-slide');
        if (slides.length === 0) return;

        if (totalIdxSpan) totalIdxSpan.textContent = slides.length;

        const slideWidth = slides[0].clientWidth || track.clientWidth;
        const scrollPos = track.scrollLeft;
        const currentIdx = Math.round(scrollPos / slideWidth) + 1;

        if (currIdxSpan) {
            currIdxSpan.textContent = Math.min(Math.max(currentIdx, 1), slides.length);
        }
    }

    track.addEventListener('scroll', updateCounter);

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            const slideWidth = track.clientWidth;
            track.scrollBy({ left: -slideWidth, behavior: 'smooth' });
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            const slideWidth = track.clientWidth;
            track.scrollBy({ left: slideWidth, behavior: 'smooth' });
        });
    }

    updateCounter();
}

export function initMuralCarousel() {
    const list = document.getElementById('wishes-list');
    const container = list ? list.closest('.mural-scroll-container') : null;
    const currIdxSpan = document.getElementById('mural-curr-idx');
    const totalIdxSpan = document.getElementById('mural-total-idx');
    const prevBtn = document.getElementById('mural-prev-arrow');
    const nextBtn = document.getElementById('mural-next-arrow');

    if (!list) return;
    if (container) handleUserActivity(container);

    function updateMuralCounter() {
        const cards = list.querySelectorAll('.wish-scroll-card');
        const total = cards.length;

        if (totalIdxSpan) totalIdxSpan.textContent = total;

        if (total === 0) {
            if (currIdxSpan) currIdxSpan.textContent = 0;
            return;
        }

        const cardWidth = list.clientWidth;
        const scrollPos = list.scrollLeft;
        const currentIdx = Math.round(scrollPos / cardWidth) + 1;

        if (currIdxSpan) {
            currIdxSpan.textContent = Math.min(Math.max(currentIdx, 1), total);
        }
    }

    list.addEventListener('scroll', updateMuralCounter);

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            const step = list.clientWidth;
            list.scrollBy({ left: -step, behavior: 'smooth' });
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            const step = list.clientWidth;
            list.scrollBy({ left: step, behavior: 'smooth' });
        });
    }

    updateMuralCounter();
}

window.updateMuralCounter = function() {
    const list = document.getElementById('wishes-list');
    const totalIdxSpan = document.getElementById('mural-total-idx');
    if (list && totalIdxSpan) {
        const cards = list.querySelectorAll('.wish-scroll-card');
        totalIdxSpan.textContent = cards.length;
    }
};
