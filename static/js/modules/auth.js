import { getCsrfToken, showToast } from './utils.js';

export function initAuthForms() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);

            fetch('/login', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message || 'Login realizado com sucesso!');
                    setTimeout(() => window.location.reload(), 600);
                } else {
                    showToast(data.error || 'Erro ao realizar login');
                }
            });
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);

            fetch('/register', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message || 'Conta criada com sucesso!');
                    setTimeout(() => window.location.reload(), 600);
                } else {
                    showToast(data.error || 'Erro ao criar conta');
                }
            });
        });
    }

    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(profileForm);

            fetch('/profile/update', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message || 'Perfil atualizado com sucesso!');
                    
                    const nameHeader = document.getElementById('header-user-name');
                    if (nameHeader) nameHeader.textContent = data.name;

                    if (data.profile_image) {
                        const avatarHeader = document.getElementById('header-user-avatar');
                        if (avatarHeader) {
                            if (avatarHeader.tagName === 'IMG') {
                                avatarHeader.src = data.profile_image;
                            } else {
                                const newImg = document.createElement('img');
                                newImg.src = data.profile_image;
                                newImg.alt = 'Foto de Perfil';
                                newImg.className = 'user-avatar-sm';
                                newImg.id = 'header-user-avatar';
                                avatarHeader.replaceWith(newImg);
                            }
                        }

                        const avatarPreview = document.getElementById('profile-avatar-preview');
                        if (avatarPreview) {
                            if (avatarPreview.tagName === 'IMG') {
                                avatarPreview.src = data.profile_image;
                            } else {
                                const newImg = document.createElement('img');
                                newImg.src = data.profile_image;
                                newImg.alt = 'Foto de Perfil';
                                newImg.className = 'profile-avatar-lg';
                                newImg.id = 'profile-avatar-preview';
                                avatarPreview.replaceWith(newImg);
                            }
                        }
                    }

                    const profileModal = document.getElementById('profile-modal');
                    if (profileModal) profileModal.classList.remove('open');
                } else {
                    showToast(data.error || 'Erro ao atualizar perfil.');
                }
            });
        });
    }

    const deleteAccountBtn = document.getElementById('delete-account-btn');
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', () => {
            if (confirm('Tem certeza absoluta de que deseja eliminar sua conta? Esta ação é irreversível.')) {
                fetch('/profile/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message);
                        setTimeout(() => window.location.href = '/', 800);
                    } else {
                        showToast(data.error || 'Erro ao eliminar conta.');
                    }
                });
            }
        });
    }
}
