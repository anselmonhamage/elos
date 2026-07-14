import { soundFx } from './sound.js';
import { getCsrfToken, showToast } from './utils.js';

export function initAdminActions() {
    document.querySelectorAll('.toggle-role-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const userId = btn.getAttribute('data-user-id');
            fetch(`/admin/toggle-role/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    soundFx.playBeep();
                    showToast(data.message);
                    
                    const badge = document.getElementById(`user-role-badge-${userId}`);
                    if (data.is_writer) {
                        btn.textContent = 'Revogar Escritor';
                        if (badge) {
                            badge.className = 'role-pill role-writer';
                            badge.textContent = 'Escritor';
                        }
                    } else {
                        btn.textContent = 'Tornar Escritor';
                        if (badge) {
                            badge.className = 'role-pill role-user';
                            badge.textContent = 'Leitor';
                        }
                    }
                } else {
                    showToast(data.error || 'Erro ao alterar permissão.');
                }
            });
        });
    });

    const toggleTerminalBtn = document.getElementById('toggle-terminal-btn');
    if (toggleTerminalBtn) {
        toggleTerminalBtn.addEventListener('click', () => {
            fetch('/admin/toggle-terminal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    soundFx.playBeep();
                    showToast(data.message);
                    
                    document.body.setAttribute('data-terminal-enabled', data.terminal_enabled ? 'true' : 'false');
                    
                    const labelSpan = document.getElementById('terminal-toggle-label');

                    if (data.terminal_enabled) {
                        toggleTerminalBtn.className = 'btn btn-sm btn-primary';
                        if (labelSpan) labelSpan.textContent = 'Terminal: Visível';
                    } else {
                        toggleTerminalBtn.className = 'btn btn-sm btn-outline';
                        if (labelSpan) labelSpan.textContent = 'Terminal: Oculto';
                    }

                    if (typeof window.globalUpdateStep === 'function') {
                        window.globalUpdateStep(window.globalCurrentStep || 1);
                    }
                } else {
                    showToast(data.error || 'Erro ao alterar configuração do terminal.');
                }
            });
        });
    }
}
