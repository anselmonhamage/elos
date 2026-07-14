import { soundFx, triggerConfetti } from './sound.js';
import { getCsrfToken } from './utils.js';

export function initTerminal() {
    const input = document.getElementById('terminal-input');
    const output = document.getElementById('terminal-output');
    if (!input || !output) return;

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const cmd = input.value.trim();
            if (!cmd) return;

            soundFx.playBeep();

            const userLine = document.createElement('div');
            userLine.className = 'terminal-log-line user-cmd';
            userLine.textContent = `dev@birthday:~$ ${cmd}`;
            output.appendChild(userLine);

            fetch('/api/terminal', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ command: cmd })
            })
            .then(res => res.json())
            .then(data => {
                if (data.clear) {
                    output.innerHTML = '';
                } else {
                    const outLine = document.createElement('div');
                    outLine.className = 'terminal-log-line out-cmd';
                    outLine.textContent = data.response;
                    output.appendChild(outLine);

                    if (cmd.toLowerCase() === 'secret') {
                        triggerConfetti();
                    }
                }
                output.scrollTop = output.scrollHeight;
            });

            input.value = '';
        }
    });
}
