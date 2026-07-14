export function initHeaderMenuToggle() {
    const toggleBtn = document.getElementById('toggle-header-menu-btn');
    const headerNav = document.getElementById('header-nav-content');
    if (!toggleBtn || !headerNav) return;

    const iconOpen = toggleBtn.querySelector('.icon-open');
    const iconClose = toggleBtn.querySelector('.icon-close');

    let isExpanded = false;

    headerNav.classList.add('collapsed');
    headerNav.classList.remove('expanded');
    toggleBtn.setAttribute('aria-expanded', 'false');
    if (iconOpen) iconOpen.classList.remove('hidden');
    if (iconClose) iconClose.classList.add('hidden');

    toggleBtn.addEventListener('click', () => {
        isExpanded = !isExpanded;

        if (isExpanded) {
            headerNav.classList.remove('collapsed');
            headerNav.classList.add('expanded');
            toggleBtn.setAttribute('aria-expanded', 'true');
            if (iconOpen) iconOpen.classList.add('hidden');
            if (iconClose) iconClose.classList.remove('hidden');
        } else {
            headerNav.classList.remove('expanded');
            headerNav.classList.add('collapsed');
            toggleBtn.setAttribute('aria-expanded', 'false');
            if (iconOpen) iconOpen.classList.remove('hidden');
            if (iconClose) iconClose.classList.add('hidden');
        }
    });
}
