window.enableEdit = function(span) {
    const filename = span.closest('.media-filename').dataset.filename;
    const currentName = span.textContent.trim();
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentName.startsWith('tag: ') ? currentName.slice(5) : currentName;
    input.className = 'media-edit-input';
    input.style.width = '80%';
    input.style.fontSize = '14px';
    input.style.margin = '0';

    let blurTimeout = null;
    let replaced = false;

    function cleanup(newNode) {
        if (!replaced && input.parentNode) {
            input.replaceWith(newNode);
            replaced = true;
        }
    }

    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            window.saveTagInline(filename, input.value, input, cleanup);
        } else if (e.key === 'Escape') {
            window.cancelEdit(input, currentName, cleanup);
        }
    });

    input.addEventListener('blur', function() {
        // Pequeno delay para permitir o Enter antes do blur
        blurTimeout = setTimeout(() => {
            window.cancelEdit(input, currentName, cleanup);
        }, 100);
    });

    span.replaceWith(input);
    input.focus();
    input.select();
};

window.saveTagInline = function(filename, tag, input, cleanup) {
    fetch('/gallery/media_tags', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename, tag})
    })
    .then(res => res.json())
    .then(data => {
        const span = document.createElement('span');
        span.className = 'media-name';
        span.ondblclick = function() { window.enableEdit(span); };
        span.textContent = tag ? `tag: ${tag}` : filename;
        if (typeof cleanup === 'function') cleanup(span);
    });
};

window.cancelEdit = function(input, originalName, cleanup) {
    const span = document.createElement('span');
    span.className = 'media-name';
    span.ondblclick = function() { window.enableEdit(span); };
    span.textContent = originalName;
    if (typeof cleanup === 'function') cleanup(span);
};
