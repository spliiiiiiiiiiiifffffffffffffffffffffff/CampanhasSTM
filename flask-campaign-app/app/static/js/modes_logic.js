export function handleModeLogic(mode, mediaFiles) {
    const previewContainer = document.getElementById('mediaPreviewContainer');
    previewContainer.innerHTML = ''; // Limpar o conteúdo anterior

    if (mode === 'inibicao') {
        // Exibir uma mídia por vez no lado esquerdo da tela, com slide automático
        let currentIndex = 0;

        function showNextMedia() {
            previewContainer.innerHTML = ''; // Limpar o conteúdo anterior
            const mediaFile = mediaFiles[currentIndex];
            const mediaElement = createMediaElement(mediaFile);
            mediaElement.style.position = 'absolute';
            mediaElement.style.left = '10px'; // Posicionar no lado esquerdo
            mediaElement.style.maxWidth = '40%';
            mediaElement.style.maxHeight = '80%';
            previewContainer.appendChild(mediaElement);

            currentIndex = (currentIndex + 1) % mediaFiles.length; // Próximo índice
        }

        showNextMedia(); // Mostrar a primeira mídia
        setInterval(showNextMedia, 15000); // Alterar a mídia a cada 15 segundos
    } else if (mode === 'self') {
        // Exibir uma imagem estática, livremente posicionada
        const mediaFile = mediaFiles[0]; // Apenas uma mídia permitida
        const mediaElement = createMediaElement(mediaFile);
        mediaElement.style.position = 'absolute';
        mediaElement.style.cursor = 'move'; // Cursor para arrastar
        mediaElement.style.maxWidth = '50%';
        mediaElement.style.maxHeight = '50%';

        // Permitir que o usuário arraste a imagem
        mediaElement.addEventListener('mousedown', (e) => {
            let offsetX = e.clientX - mediaElement.offsetLeft;
            let offsetY = e.clientY - mediaElement.offsetTop;

            function onMouseMove(event) {
                mediaElement.style.left = `${event.clientX - offsetX}px`;
                mediaElement.style.top = `${event.clientY - offsetY}px`;
            }

            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', () => {
                document.removeEventListener('mousemove', onMouseMove);
            }, { once: true });
        });

        previewContainer.appendChild(mediaElement);
    } else if (mode === 'antena') {
        // Exibir duas mídias simultaneamente em dois monitores
        let currentIndex = 0;

        function showNextMediaPair() {
            previewContainer.innerHTML = ''; // Limpar o conteúdo anterior

            // Criar dois elementos de mídia
            const mediaFile1 = mediaFiles[currentIndex];
            const mediaFile2 = mediaFiles[(currentIndex + 1) % mediaFiles.length];

            const mediaElement1 = createMediaElement(mediaFile1);
            const mediaElement2 = createMediaElement(mediaFile2);

            mediaElement1.style.position = 'absolute';
            mediaElement1.style.left = '10px'; // Monitor 1
            mediaElement1.style.maxWidth = '45%';
            mediaElement1.style.maxHeight = '80%';

            mediaElement2.style.position = 'absolute';
            mediaElement2.style.right = '10px'; // Monitor 2
            mediaElement2.style.maxWidth = '45%';
            mediaElement2.style.maxHeight = '80%';

            previewContainer.appendChild(mediaElement1);
            previewContainer.appendChild(mediaElement2);

            currentIndex = (currentIndex + 2) % mediaFiles.length; // Próximo par de mídias
        }

        showNextMediaPair(); // Mostrar o primeiro par de mídias
        setInterval(showNextMediaPair, 15000); // Alterar as mídias a cada 15 segundos
    }
}

function createMediaElement(mediaFile) {
    const mediaElement = mediaFile.endsWith('.mp4') ? document.createElement('video') : document.createElement('img');
    mediaElement.src = `/static/uploads/${mediaFile}`;
    mediaElement.controls = mediaFile.endsWith('.mp4'); // Adicionar controles para vídeos
    mediaElement.style.maxWidth = '100%';
    mediaElement.style.maxHeight = '100%';
    return mediaElement;
}