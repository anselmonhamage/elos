import { soundFx } from './sound.js';
import { getCsrfToken } from './utils.js';

export function isTerminalEnabled() {
    const attr = document.body.getAttribute('data-terminal-enabled');
    return attr === 'true';
}

export let globalCurrentStep = 1;
export let globalUpdateStep = null;

export function initStepsWizard() {
    const totalSteps = 4;

    const stepCards = document.querySelectorAll('.step-card');
    const stepItems = document.querySelectorAll('.step-item');
    const progressBar = document.getElementById('steps-progress-bar');

    function getSavedStep() {
        const bodyStep = document.body.getAttribute('data-initial-step');
        if (bodyStep) {
            const parsed = parseInt(bodyStep, 10);
            if (parsed >= 1 && parsed <= totalSteps) return parsed;
        }

        const hashMatch = window.location.hash.match(/#step-(\d+)/);
        if (hashMatch) {
            const hStep = parseInt(hashMatch[1], 10);
            if (hStep >= 1 && hStep <= totalSteps) return hStep;
        }

        const saved = localStorage.getItem('elos_active_step');
        if (saved) {
            const parsed = parseInt(saved, 10);
            if (parsed >= 1 && parsed <= totalSteps) return parsed;
        }

        return 1;
    }

    function updateStep(stepNumber, saveHistory = true) {
        if (stepNumber < 1 || stepNumber > totalSteps) return;

        const terminalOn = isTerminalEnabled();

        if (!terminalOn && stepNumber === 3) {
            stepNumber = 4;
        }

        globalCurrentStep = stepNumber;

        // Persistir no Servidor (Base de dados ou Session)
        fetch('/api/steps/active', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ step: stepNumber })
        }).catch(err => console.error('Erro ao salvar passo ativo no servidor:', err));

        // Persistir no LocalStorage e URL Hash para manter o passo ao recarregar (F5)
        localStorage.setItem('elos_active_step', stepNumber.toString());
        if (saveHistory && window.history && window.history.replaceState) {
            window.history.replaceState(null, '', '#step-' + stepNumber);
        }

        stepCards.forEach(card => {
            const cardStep = parseInt(card.getAttribute('data-step'), 10);
            if (cardStep === globalCurrentStep) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });

        const visibleItems = Array.from(stepItems).filter(item => {
            const itemStep = parseInt(item.getAttribute('data-step-target'), 10);
            return terminalOn || itemStep !== 3;
        });

        const activeVisibleIndex = visibleItems.findIndex(item => {
            return parseInt(item.getAttribute('data-step-target'), 10) === globalCurrentStep;
        });

        const progressPercentage = visibleItems.length > 1
            ? (activeVisibleIndex / (visibleItems.length - 1)) * 100
            : 0;

        if (progressBar) {
            progressBar.style.width = `${progressPercentage}%`;
        }

        stepItems.forEach(item => {
            const itemStep = parseInt(item.getAttribute('data-step-target'), 10);
            const badge = item.querySelector('.step-badge');

            if (!terminalOn && itemStep === 3) {
                item.classList.add('hidden');
                return;
            } else {
                item.classList.remove('hidden');
            }

            const visibleIndex = visibleItems.indexOf(item);
            const displayBadgeNum = visibleIndex + 1;

            item.classList.remove('active', 'completed');

            if (itemStep < globalCurrentStep) {
                item.classList.add('completed');
                if (badge) badge.innerHTML = '&#10003;';
            } else if (itemStep === globalCurrentStep) {
                item.classList.add('active');
                if (badge) badge.textContent = displayBadgeNum;
            } else {
                if (badge) badge.textContent = displayBadgeNum;
            }
        });
    }

    globalUpdateStep = updateStep;

    stepItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetStep = parseInt(item.getAttribute('data-step-target'), 10);
            updateStep(targetStep);
        });
    });

    document.querySelectorAll('[data-jump-step]').forEach(btn => {
        btn.addEventListener('click', () => {
            const step = parseInt(btn.getAttribute('data-jump-step'), 10);
            updateStep(step);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });

    document.querySelectorAll('.btn-next-step').forEach(btn => {
        btn.addEventListener('click', () => {
            soundFx.playBeep();
            let next = globalCurrentStep + 1;
            if (!isTerminalEnabled() && next === 3) {
                next = 4;
            }
            updateStep(next);
        });
    });

    document.querySelectorAll('.btn-prev-step').forEach(btn => {
        btn.addEventListener('click', () => {
            soundFx.playBeep();
            let prev = globalCurrentStep - 1;
            if (!isTerminalEnabled() && prev === 3) {
                prev = 2;
            }
            updateStep(prev);
        });
    });

    window.addEventListener('hashchange', () => {
        const hashStep = getSavedStep();
        updateStep(hashStep, false);
    });

    const initialStep = getSavedStep();
    updateStep(initialStep);
}
