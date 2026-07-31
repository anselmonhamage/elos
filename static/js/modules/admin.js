import { soundFx } from './sound.js';
import { getCsrfToken, showToast, escapeHtml } from './utils.js';

export function bindUserRoleButtons(container = document) {
    container.querySelectorAll('.toggle-role-btn').forEach(btn => {
        if (btn.dataset.bound) return;
        btn.dataset.bound = 'true';
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
}

export function loadUsersTable() {
    const tbody = document.getElementById('admin-users-table-body');
    if (!tbody) return;

    fetch('/admin/users')
    .then(res => res.json())
    .then(data => {
        if (!data.success || !data.users) return;

        if (data.users.length === 0) {
            tbody.innerHTML = `
                <tr id="no-users-row">
                    <td colspan="4" style="text-align: center; color: var(--text-secondary); padding: 20px;">
                        Nenhum usuário cadastrado.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = data.users.map(u => {
            let roleBadge = '';
            if (u.is_admin) {
                roleBadge = `<span class="role-pill role-admin">Admin</span>`;
            } else if (u.is_writer) {
                roleBadge = `<span class="role-pill role-writer" id="user-role-badge-${u.id}">Escritor</span>`;
            } else {
                roleBadge = `<span class="role-pill role-user" id="user-role-badge-${u.id}">Leitor</span>`;
            }

            let actionCol = '';
            if (!u.is_admin) {
                const btnText = u.is_writer ? 'Revogar Escritor' : 'Tornar Escritor';
                actionCol = `
                    <button class="btn btn-sm btn-outline toggle-role-btn" 
                            data-user-id="${u.id}" 
                            id="toggle-btn-${u.id}">
                        ${btnText}
                    </button>
                `;
            } else {
                actionCol = `<span class="text-muted">Master Admin</span>`;
            }

            return `
                <tr class="user-row" data-user-name="${escapeHtml(u.name.toLowerCase())}" data-user-email="${escapeHtml(u.email.toLowerCase())}">
                    <td><strong>${escapeHtml(u.name)}</strong></td>
                    <td>${escapeHtml(u.email)}</td>
                    <td>${roleBadge}</td>
                    <td>${actionCol}</td>
                </tr>
            `;
        }).join('');

        bindUserRoleButtons(tbody);

        const searchInput = document.getElementById('user-search-input');
        if (searchInput && searchInput.value) {
            searchInput.dispatchEvent(new Event('input'));
        }
    })
    .catch(err => console.error('Erro ao carregar lista de usuários:', err));
}

export function initAdminActions() {
    bindUserRoleButtons();

    // User search input live filtering
    const searchInput = document.getElementById('user-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const userRows = document.querySelectorAll('#admin-users-table-body .user-row');
            let visibleCount = 0;

            userRows.forEach(row => {
                const name = row.getAttribute('data-user-name') || '';
                const email = row.getAttribute('data-user-email') || '';
                if (name.includes(query) || email.includes(query)) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            const noUsersRow = document.getElementById('no-users-row');
            if (noUsersRow) {
                noUsersRow.style.display = (visibleCount === 0) ? '' : 'none';
            }
        });
    }

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

    // Terminal Command Customizer Panel
    const cmdForm = document.getElementById('terminal-cmd-form');
    const nameInput = document.getElementById('cmd-name-input');
    const respInput = document.getElementById('cmd-resp-input');
    const saveBtn = document.getElementById('save-cmd-btn');
    const tbody = document.getElementById('terminal-cmds-table-body');

    let currentEditMode = 'add'; // 'add' or 'edit'

    function setFormMode(mode) {
        currentEditMode = mode;
        if (mode === 'edit') {
            nameInput.setAttribute('readonly', 'true');
            nameInput.style.backgroundColor = '#f1f5f9';
            if (saveBtn) saveBtn.textContent = 'Atualizar Comando';
        } else {
            nameInput.removeAttribute('readonly');
            nameInput.style.backgroundColor = '';
            if (saveBtn) saveBtn.textContent = 'Salvar Comando';
            if (cmdForm) cmdForm.reset();
        }
    }

    function bindRowEvents(rowEl) {
        const editBtn = rowEl.querySelector('.edit-cmd-btn');
        const deleteBtn = rowEl.querySelector('.delete-cmd-btn');

        if (editBtn) {
            editBtn.addEventListener('click', () => {
                const name = editBtn.getAttribute('data-cmd-name');
                const content = editBtn.getAttribute('data-cmd-content');
                
                nameInput.value = name;
                respInput.value = content;
                setFormMode('edit');
                respInput.focus();
            });
        }

        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => {
                const name = deleteBtn.getAttribute('data-cmd-name');
                if (confirm(`Deseja realmente deletar o comando "${name}"?`)) {
                    fetch('/api/terminal', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken()
                        },
                        body: JSON.stringify({ command: `delete ${name}` })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success && !data.response.toLowerCase().startsWith('erro')) {
                            soundFx.playBeep();
                            showToast(data.response);
                            const row = document.getElementById(`cmd-row-${name}`);
                            if (row) row.remove();
                            if (nameInput.value === name) {
                                setFormMode('add');
                            }
                        } else {
                            showToast(data.response || 'Erro ao deletar comando.');
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        showToast('Erro de rede ao deletar comando.');
                    });
                }
            });
        }
    }

    if (tbody) {
        tbody.querySelectorAll('tr').forEach(row => {
            bindRowEvents(row);
        });
    }

    if (cmdForm) {
        cmdForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = nameInput.value.trim().toLowerCase();
            const responseText = respInput.value.trim();

            if (!name || !responseText) return;

            const commandStr = `${currentEditMode} ${name} ${responseText}`;

            fetch('/api/terminal', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ command: commandStr })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && !data.response.toLowerCase().startsWith('erro')) {
                    soundFx.playBeep();
                    showToast(data.response);
                    
                    if (currentEditMode === 'add') {
                        const tr = document.createElement('tr');
                        tr.id = `cmd-row-${name}`;
                        tr.innerHTML = `
                            <td><code>${name}</code></td>
                            <td><span class="cmd-content-text" id="cmd-text-${name}">${escapeHtml(responseText)}</span></td>
                            <td>
                                <div class="table-actions-group">
                                    <button class="btn btn-outline edit-cmd-btn" 
                                            data-cmd-name="${name}" 
                                            data-cmd-content="${escapeHtml(responseText)}"
                                            id="edit-cmd-${name}">
                                        Editar
                                    </button>
                                    <button class="btn btn-danger delete-cmd-btn" 
                                            data-cmd-name="${name}"
                                            id="delete-cmd-${name}">
                                        Deletar
                                    </button>
                                </div>
                            </td>
                        `;
                        if (tbody) tbody.appendChild(tr);
                        bindRowEvents(tr);
                    } else {
                        const textSpan = document.getElementById(`cmd-text-${name}`);
                        if (textSpan) textSpan.textContent = responseText;
                        const editBtn = document.getElementById(`edit-cmd-${name}`);
                        if (editBtn) editBtn.setAttribute('data-cmd-content', responseText);
                    }

                    setFormMode('add');
                } else {
                    showToast(data.response || 'Erro ao salvar comando.');
                }
            })
            .catch(err => {
                console.error(err);
                showToast('Erro ao salvar comando.');
            });
        });
    }
}
