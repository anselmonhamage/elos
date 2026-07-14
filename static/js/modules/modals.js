export function initModals() {
    const loginModal = document.getElementById('login-modal');
    const registerModal = document.getElementById('register-modal');
    const adminModal = document.getElementById('admin-modal');
    const editWelcomeModal = document.getElementById('edit-welcome-modal');
    const editSpecialMsgModal = document.getElementById('edit-special-msg-modal');
    const termsModal = document.getElementById('terms-modal');
    const privacyModal = document.getElementById('privacy-modal');
    const supportModal = document.getElementById('support-modal');
    const faqModal = document.getElementById('faq-modal');

    const openLoginBtn = document.getElementById('open-login-btn');
    const openRegisterBtn = document.getElementById('open-register-btn');
    const openAdminBtn = document.getElementById('open-admin-btn');
    const openEditWelcomeBtn = document.getElementById('open-edit-welcome-btn');
    const openEditSpecialMsgBtn = document.getElementById('open-edit-special-msg-btn');
    const openTermsBtn = document.getElementById('open-terms-btn');
    const openPrivacyBtn = document.getElementById('open-privacy-btn');
    const openSupportBtn = document.getElementById('open-support-btn');
    const openFaqBtn = document.getElementById('open-faq-btn');

    const closeLoginBtn = document.getElementById('close-login-btn');
    const closeRegisterBtn = document.getElementById('close-register-btn');
    const closeAdminBtn = document.getElementById('close-admin-btn');
    const closeEditWelcomeBtn = document.getElementById('close-edit-welcome-btn');
    const closeEditSpecialMsgBtn = document.getElementById('close-edit-special-msg-btn');
    const closeTermsBtn = document.getElementById('close-terms-btn');
    const closePrivacyBtn = document.getElementById('close-privacy-btn');
    const closeSupportBtn = document.getElementById('close-support-btn');
    const closeFaqBtn = document.getElementById('close-faq-btn');

    const switchToRegister = document.getElementById('switch-to-register');
    const switchToLogin = document.getElementById('switch-to-login');

    document.querySelectorAll('.open-login-trigger').forEach(el => {
        el.addEventListener('click', () => {
            if (loginModal) loginModal.classList.add('open');
        });
    });

    document.querySelectorAll('.open-welcome-modal-btn').forEach(el => {
        el.addEventListener('click', () => {
            if (editWelcomeModal) editWelcomeModal.classList.add('open');
        });
    });

    if (openLoginBtn && loginModal) openLoginBtn.addEventListener('click', () => loginModal.classList.add('open'));
    if (openRegisterBtn && registerModal) openRegisterBtn.addEventListener('click', () => registerModal.classList.add('open'));
    if (openAdminBtn && adminModal) openAdminBtn.addEventListener('click', () => adminModal.classList.add('open'));
    if (openEditWelcomeBtn && editWelcomeModal) openEditWelcomeBtn.addEventListener('click', () => editWelcomeModal.classList.add('open'));
    if (openEditSpecialMsgBtn && editSpecialMsgModal) openEditSpecialMsgBtn.addEventListener('click', () => editSpecialMsgModal.classList.add('open'));
    if (openTermsBtn && termsModal) openTermsBtn.addEventListener('click', () => termsModal.classList.add('open'));
    if (openPrivacyBtn && privacyModal) openPrivacyBtn.addEventListener('click', () => privacyModal.classList.add('open'));
    if (openSupportBtn && supportModal) openSupportBtn.addEventListener('click', () => supportModal.classList.add('open'));
    if (openFaqBtn && faqModal) openFaqBtn.addEventListener('click', () => faqModal.classList.add('open'));

    if (closeLoginBtn && loginModal) closeLoginBtn.addEventListener('click', () => loginModal.classList.remove('open'));
    if (closeRegisterBtn && registerModal) closeRegisterBtn.addEventListener('click', () => registerModal.classList.remove('open'));
    if (closeAdminBtn && adminModal) closeAdminBtn.addEventListener('click', () => adminModal.classList.remove('open'));
    if (closeEditWelcomeBtn && editWelcomeModal) closeEditWelcomeBtn.addEventListener('click', () => editWelcomeModal.classList.remove('open'));
    if (closeEditSpecialMsgBtn && editSpecialMsgModal) closeEditSpecialMsgBtn.addEventListener('click', () => editSpecialMsgModal.classList.remove('open'));
    if (closeTermsBtn && termsModal) closeTermsBtn.addEventListener('click', () => termsModal.classList.remove('open'));
    if (closePrivacyBtn && privacyModal) closePrivacyBtn.addEventListener('click', () => privacyModal.classList.remove('open'));
    if (closeSupportBtn && supportModal) closeSupportBtn.addEventListener('click', () => supportModal.classList.remove('open'));
    if (closeFaqBtn && faqModal) closeFaqBtn.addEventListener('click', () => faqModal.classList.remove('open'));

    if (switchToRegister && loginModal && registerModal) {
        switchToRegister.addEventListener('click', () => {
            loginModal.classList.remove('open');
            registerModal.classList.add('open');
        });
    }

    if (switchToLogin && loginModal && registerModal) {
        switchToLogin.addEventListener('click', () => {
            registerModal.classList.remove('open');
            loginModal.classList.add('open');
        });
    }

    const profileModal = document.getElementById('profile-modal');
    const openProfileBtn = document.getElementById('open-profile-btn');
    const closeProfileBtn = document.getElementById('close-profile-btn');

    if (openProfileBtn && profileModal) openProfileBtn.addEventListener('click', () => profileModal.classList.add('open'));
    if (closeProfileBtn && profileModal) closeProfileBtn.addEventListener('click', () => profileModal.classList.remove('open'));

    window.addEventListener('click', (e) => {
        if (e.target === loginModal) loginModal.classList.remove('open');
        if (e.target === registerModal) registerModal.classList.remove('open');
        if (e.target === profileModal) profileModal.classList.remove('open');
        if (e.target === adminModal) adminModal.classList.remove('open');
        if (e.target === editWelcomeModal) editWelcomeModal.classList.remove('open');
        if (e.target === editSpecialMsgModal) editSpecialMsgModal.classList.remove('open');
        if (e.target === termsModal) termsModal.classList.remove('open');
        if (e.target === privacyModal) privacyModal.classList.remove('open');
        if (e.target === supportModal) supportModal.classList.remove('open');
        if (e.target === faqModal) faqModal.classList.remove('open');
    });
}
