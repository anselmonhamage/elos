import { soundFx, triggerConfetti } from './sound.js';
import { showToast } from './utils.js';

export function initInteractions() {
    const confettiBtn = document.getElementById('confetti-btn');
    if (confettiBtn) {
        confettiBtn.addEventListener('click', triggerConfetti);
    }

    const audioToggleBtn = document.getElementById('audio-toggle-btn');
    const soundText = document.getElementById('sound-btn-text');
    const soundIconOn = document.getElementById('sound-icon-on');
    const soundIconOff = document.getElementById('sound-icon-off');

    if (audioToggleBtn) {
        audioToggleBtn.addEventListener('click', () => {
            soundFx.enabled = !soundFx.enabled;
            if (soundText) soundText.textContent = soundFx.enabled ? 'Som: LIGADO' : 'Som: DESLIGADO';
            
            if (soundFx.enabled) {
                if (soundIconOn) soundIconOn.classList.remove('hidden');
                if (soundIconOff) soundIconOff.classList.add('hidden');
            } else {
                if (soundIconOn) soundIconOn.classList.add('hidden');
                if (soundIconOff) soundIconOff.classList.remove('hidden');
            }
        });
    }

    const copyBtn = document.getElementById('copy-text-btn');
    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const poeticContainer = document.getElementById('special-content-display');
            const text = poeticContainer ? poeticContainer.innerText : 'Feliz Aniversário!';
            navigator.clipboard.writeText(text).then(() => {
                showToast('Mensagem copiada para a área de transferência!');
            });
        });
    }

    const hugBtn = document.getElementById('hug-btn');
    if (hugBtn) {
        hugBtn.addEventListener('click', () => {
            triggerConfetti();
            showToast('Abraço virtual enviado!');
        });
    }
}
