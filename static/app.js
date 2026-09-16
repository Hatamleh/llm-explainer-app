const chat = document.getElementById('chat');
const welcome = document.getElementById('welcome');
const form = document.getElementById('composer');
const input = document.getElementById('topic');
const sendBtn = document.getElementById('send');

// Chat history sent back to the server so follow-up questions have context.
let history = [];

function renderMarkdown(text) {
	return DOMPurify.sanitize(marked.parse(text));
}

function addMessage(role, content, { error = false } = {}) {
	welcome.hidden = true;
	const msg = document.createElement('div');
	msg.className = `msg ${role}${error ? ' error' : ''}`;
	msg.dataset.testid = `${role}-message`;

	const bubble = document.createElement('div');
	bubble.className = 'bubble';
	if (role === 'assistant' && !error) {
		bubble.classList.add('md');
		bubble.innerHTML = renderMarkdown(content);
	} else {
		bubble.textContent = content;
	}

	msg.appendChild(bubble);
	chat.appendChild(msg);
	chat.scrollTop = chat.scrollHeight;
	return msg;
}

function addTyping() {
	welcome.hidden = true;
	const msg = document.createElement('div');
	msg.className = 'msg assistant';
	msg.dataset.testid = 'typing-indicator';
	msg.innerHTML = '<div class="bubble"><div class="typing"><span></span><span></span><span></span></div></div>';
	chat.appendChild(msg);
	chat.scrollTop = chat.scrollHeight;
	return msg;
}

async function send(topic) {
	topic = topic.trim();
	if (!topic) return;

	addMessage('user', topic);
	input.value = '';
	autoGrow();
	sendBtn.disabled = true;
	const typing = addTyping();

	try {
		const res = await fetch('/api/explain', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ topic, history })
		});
		const data = await res.json();
		if (!res.ok) throw new Error(data.detail || 'Request failed');

		typing.remove();
		addMessage('assistant', data.answer);
		history.push({ role: 'user', content: topic }, { role: 'assistant', content: data.answer });
	} catch (err) {
		typing.remove();
		addMessage('assistant', 'عذراً، صار في مشكلة وما قدرت أجيب الشرح. جرّب مرة ثانية.', { error: true });
		console.error(err);
	} finally {
		sendBtn.disabled = false;
		input.focus();
	}
}

function autoGrow() {
	input.style.height = 'auto';
	input.style.height = `${input.scrollHeight}px`;
}

form.addEventListener('submit', (e) => {
	e.preventDefault();
	send(input.value);
});

// Enter sends, Shift+Enter adds a new line.
input.addEventListener('keydown', (e) => {
	if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
		e.preventDefault();
		if (!sendBtn.disabled) form.requestSubmit();
	}
});
input.addEventListener('input', autoGrow);

document.querySelectorAll('.suggestions .chip').forEach((chip) => {
	chip.addEventListener('click', () => send(chip.textContent));
});

document.getElementById('new-chat').addEventListener('click', () => {
	history = [];
	chat.querySelectorAll('.msg').forEach((m) => m.remove());
	welcome.hidden = false;
	input.focus();
});

input.focus();
