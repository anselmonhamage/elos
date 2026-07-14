import { initHeaderMenuToggle } from './modules/header.js';
import { initStepsWizard } from './modules/wizard.js';
import { initInteractions } from './modules/interactions.js';
import { initTerminal } from './modules/terminal.js';
import { initModals } from './modules/modals.js';
import { initAuthForms } from './modules/auth.js';
import { initWriterForm, initWriterSectionEditors } from './modules/writer.js';
import { initAdminActions } from './modules/admin.js';
import { initInstagramCarousels } from './modules/carousels.js';

document.addEventListener('DOMContentLoaded', () => {
    initHeaderMenuToggle();
    initStepsWizard();
    initInteractions();
    initTerminal();
    initModals();
    initAuthForms();
    initWriterForm();
    initWriterSectionEditors();
    initAdminActions();
    initInstagramCarousels();
});
