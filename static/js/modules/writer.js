import { soundFx, triggerConfetti } from './sound.js';
import { getCsrfToken, showToast, escapeHtml } from './utils.js';

export function initWriterSectionEditors() {
    const editWelcomeForm = document.getElementById('edit-welcome-form');
    if (editWelcomeForm) {
        editWelcomeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(editWelcomeForm);

            fetch('/writer/update-welcome', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    soundFx.playChime();
                    showToast(data.message);

                    const titleEl = document.getElementById('welcome-title-display');
                    const contentEl = document.getElementById('welcome-content-display');
                    const imgEl = document.getElementById('hero-img-display');

                    if (titleEl) titleEl.textContent = data.title;
                    if (contentEl) contentEl.textContent = data.content;

                    const track = document.getElementById('welcome-carousel-track');
                    const emptyGallery = document.getElementById('welcome-empty-gallery');
                    const counterBadge = document.getElementById('welcome-counter-badge');
                    const totalIdx = document.getElementById('welcome-total-idx');
                    const currIdx = document.getElementById('welcome-curr-idx');
                    const prevBtn = document.getElementById('welcome-prev-arrow');
                    const nextBtn = document.getElementById('welcome-next-arrow');

                    if (data.images_urls && data.images_urls.length > 0) {
                        if (emptyGallery) emptyGallery.classList.add('hidden');
                        if (counterBadge) counterBadge.classList.remove('hidden');
                        if (track) {
                            track.classList.remove('hidden');
                            track.innerHTML = data.images_urls.map(url => `
                                <div class="insta-carousel-slide">
                                    <img src="${url}" alt="Foto de Boas-vindas" class="hero-mockup-img welcome-slide-img" style="object-fit: ${data.image_fit || 'contain'};">
                                </div>
                            `).join('');
                        }

                        if (totalIdx) totalIdx.textContent = data.images_urls.length;
                        if (currIdx) currIdx.textContent = '1';

                        const manageGrid = document.getElementById('welcome-images-manage-grid');
                        if (manageGrid) {
                            manageGrid.innerHTML = data.images_urls.map(url => `
                                <div class="manage-image-card" data-img-url="${url}">
                                    <img src="${url}" alt="Thumbnail" class="manage-image-thumb" onclick="previewWelcomeImage(this.src)">
                                    <button type="button" class="btn-delete-img" onclick="deleteWelcomeImage(event, '${url}')" title="Excluir Imagem">&times;</button>
                                </div>
                            `).join('');
                        }

                        if (prevBtn) prevBtn.style.display = data.images_urls.length > 1 ? 'flex' : 'none';
                        if (nextBtn) nextBtn.style.display = data.images_urls.length > 1 ? 'flex' : 'none';
                    } else {
                        if (track) track.classList.add('hidden');
                        if (counterBadge) counterBadge.classList.add('hidden');
                        if (emptyGallery) emptyGallery.classList.remove('hidden');
                        if (prevBtn) prevBtn.style.display = 'none';
                        if (nextBtn) nextBtn.style.display = 'none';
                    }

                    const editWelcomeModal = document.getElementById('edit-welcome-modal');
                    if (editWelcomeModal) editWelcomeModal.classList.remove('open');
                } else {
                    showToast(data.error || 'Erro ao atualizar a seção de boas-vindas.');
                }
            });
        });
    }

    const editSpecialMsgForm = document.getElementById('edit-special-msg-form');
    if (editSpecialMsgForm) {
        editSpecialMsgForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(editSpecialMsgForm);

            fetch('/writer/update-special-message', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    soundFx.playChime();
                    showToast(data.message);

                    const titleEl = document.getElementById('special-title-display');
                    const contentEl = document.getElementById('special-content-display');

                    if (titleEl) titleEl.textContent = data.title;
                    if (contentEl) {
                        const paragraphs = data.content.split('\n\n');
                        contentEl.innerHTML = paragraphs.map((p, idx) => {
                            return idx === 0 ? `<p class="lead-text">${escapeHtml(p)}</p>` : `<p>${escapeHtml(p)}</p>`;
                        }).join('');
                    }

                    const editSpecialMsgModal = document.getElementById('edit-special-msg-modal');
                    if (editSpecialMsgModal) editSpecialMsgModal.classList.remove('open');
                } else {
                    showToast(data.error || 'Erro ao atualizar a mensagem especial.');
                }
            });
        });
    }
}

export function initWriterForm() {
    const writerForm = document.getElementById('writer-wish-form');
    if (writerForm) {
        writerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(writerForm);

            fetch('/writer/wish', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCsrfToken() },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    soundFx.playChime();
                    triggerConfetti();
                    showToast('Mensagem publicada no mural com sucesso!');
                    prependWishHorizontal(data.wish);
                    writerForm.reset();
                } else {
                    showToast(data.error || 'Erro ao publicar mensagem');
                }
            });
        });
    }
}

export function prependWishHorizontal(wish) {
    const list = document.getElementById('wishes-list');
    if (!list) return;

    const noMsg = document.getElementById('no-wishes-msg');
    if (noMsg) noMsg.remove();

    const isLiked = wish.is_liked || false;
    const div = document.createElement('div');
    div.className = 'wish-scroll-card';
    div.setAttribute('data-id', wish.id);
    div.innerHTML = `
        <div class="wish-item-header">
            <strong>${escapeHtml(wish.author)}</strong>
            <span class="wish-role">(${escapeHtml(wish.role)})</span>
            <span class="wish-time">${escapeHtml(wish.timestamp)}</span>
        </div>
        <p class="wish-text">${escapeHtml(wish.message)}</p>
        <div class="wish-card-footer">
            <button class="btn-like-heart ${isLiked ? 'liked' : ''}" id="btn-like-${wish.id}" onclick="likeWish(${wish.id}, this)" title="Curtir Homenagem">
                <svg class="heart-icon" width="18" height="18" viewBox="0 0 24 24" fill="${isLiked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
                </svg>
                <span id="like-num-${wish.id}" class="like-count">${wish.likes}</span>
            </button>
            <button class="btn-delete-wish" onclick="deleteWish(${wish.id}, this)" title="Excluir Recado">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"/>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                    <line x1="10" x2="10" y1="11" y2="17"/>
                    <line x1="14" x2="14" y1="11" y2="17"/>
                </svg>
                <span>Excluir</span>
            </button>
        </div>
    `;
    list.prepend(div);
    list.scrollLeft = 0;
    if (typeof window.updateMuralCounter === 'function') {
        window.updateMuralCounter();
    }
}

export function likeWish(wishId, btnEl) {
    const btn = btnEl || document.getElementById(`btn-like-${wishId}`);
    
    fetch(`/api/wishes/like/${wishId}`, { 
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            soundFx.playBeep();
            showToast('Obrigado pelo carinho! Curtida registrada.');

            const numEl = document.getElementById(`like-num-${wishId}`);
            if (numEl) numEl.textContent = data.likes;

            if (btn) {
                btn.classList.add('liked');
                const svg = btn.querySelector('.heart-icon');
                if (svg) svg.setAttribute('fill', 'currentColor');
            }
        } else {
            showToast(data.error || 'Você já curtiu esta homenagem!');
            if (btn && data.already_liked) {
                btn.classList.add('liked');
                const svg = btn.querySelector('.heart-icon');
                if (svg) svg.setAttribute('fill', 'currentColor');
            }
        }
    });
}

export function deleteWish(wishId, btnEl) {
    if (!confirm('Tem certeza de que deseja excluir este recado do mural?')) {
        return;
    }

    fetch(`/writer/wish/delete/${wishId}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            soundFx.playBeep();
            showToast(data.message || 'Recado excluído com sucesso!');

            const card = btnEl ? btnEl.closest('.wish-scroll-card') : document.querySelector(`.wish-scroll-card[data-id="${wishId}"]`);
            if (card) {
                card.remove();
            }

            const list = document.getElementById('wishes-list');
            if (list && list.querySelectorAll('.wish-scroll-card').length === 0) {
                list.innerHTML = '<p id="no-wishes-msg" class="empty-state">Nenhum recado cadastrado ainda. Seja o primeiro a enviar!</p>';
            }

            if (typeof window.updateMuralCounter === 'function') {
                window.updateMuralCounter();
            }
        } else {
            showToast(data.error || 'Erro ao excluir o recado.');
        }
    })
    .catch(() => {
        showToast('Erro de conexão ao tentar excluir o recado.');
    });
}

window.likeWish = likeWish;
window.deleteWish = deleteWish;

window.deleteWelcomeImage = function(event, imageUrl) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    if (!confirm("Deseja realmente excluir esta imagem do carrossel?")) return;
    
    fetch('/writer/delete-welcome-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ image_url: imageUrl })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showToast('Imagem excluída do carrossel!');
            
            // Remove thumbnail card from the modal view
            const cards = document.querySelectorAll('.manage-image-card');
            for (let card of cards) {
                if (card.getAttribute('data-img-url') === imageUrl) {
                    card.remove();
                    break;
                }
            }
            
            // Update the main page carousels automatically
            const track = document.getElementById('welcome-carousel-track');
            const emptyGallery = document.getElementById('welcome-empty-gallery');
            const counterBadge = document.getElementById('welcome-counter-badge');
            const totalIdx = document.getElementById('welcome-total-idx');
            const currIdx = document.getElementById('welcome-curr-idx');
            const prevBtn = document.getElementById('welcome-prev-arrow');
            const nextBtn = document.getElementById('welcome-next-arrow');

            if (data.images_urls && data.images_urls.length > 0) {
                if (emptyGallery) emptyGallery.classList.add('hidden');
                if (counterBadge) counterBadge.classList.remove('hidden');
                if (track) {
                    track.classList.remove('hidden');
                    track.innerHTML = data.images_urls.map(url => `
                        <div class="insta-carousel-slide">
                            <img src="${url}" alt="Foto de Boas-vindas" class="hero-mockup-img welcome-slide-img" style="object-fit: contain;">
                        </div>
                    `).join('');
                }

                if (totalIdx) totalIdx.textContent = data.images_urls.length;
                if (currIdx) currIdx.textContent = '1';

                if (prevBtn) prevBtn.style.display = data.images_urls.length > 1 ? 'flex' : 'none';
                if (nextBtn) nextBtn.style.display = data.images_urls.length > 1 ? 'flex' : 'none';
            } else {
                if (track) track.classList.add('hidden');
                if (counterBadge) counterBadge.classList.add('hidden');
                if (emptyGallery) emptyGallery.classList.remove('hidden');
                if (prevBtn) prevBtn.style.display = 'none';
                if (nextBtn) nextBtn.style.display = 'none';
            }
        } else {
            showToast(data.error || 'Erro ao excluir imagem.');
        }
    })
    .catch(err => {
        console.error(err);
        showToast('Erro de rede ao excluir imagem.');
    });
};

window.previewWelcomeImage = function(src) {
    const overlay = document.getElementById('image-preview-overlay');
    const content = document.getElementById('image-preview-content');
    if (overlay && content) {
        content.src = src;
        overlay.classList.add('open');
    }
};

window.closeImagePreview = function() {
    const overlay = document.getElementById('image-preview-overlay');
    if (overlay) {
        overlay.classList.remove('open');
    }
};
