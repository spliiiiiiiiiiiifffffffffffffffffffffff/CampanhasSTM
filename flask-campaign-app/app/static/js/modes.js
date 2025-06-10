import { handleModeLogic } from './modes_logic.js';

console.log('modes.js carregado');

let selectedMode = null;

function setMode(mode, campaignDiv) {
    selectedMode = mode;
    alert(`Modo "${mode}" configurado para a campanha.`);

    // Atualizar todos os anúncios existentes na campanha
    const adContainer = campaignDiv.querySelector('.adContainer');
    const ads = Array.from(adContainer.children); // Obter todos os anúncios

    ads.forEach(ad => {
        const mediaSelection = ad.querySelector('.media-selection');
        const adTitle = ad.querySelector('h4');

        // Atualizar o título do anúncio
        adTitle.textContent = `Anúncio ${Array.from(adContainer.children).indexOf(ad) + 1} (Modo: ${mode.charAt(0).toUpperCase() + mode.slice(1)})`;

        // Atualizar o conteúdo da seleção de mídia com base no novo modo
        if (mode === 'inibicao') {
            mediaSelection.innerHTML = `
                <h5>Selecione 1 mídia para exibição em sequência:</h5>
                <select name="adMedia" class="media-dropdown" required>
                    <option value="">Nenhuma</option>
                    ${getMediaOptions()}
                </select>
            `;
        } else if (mode === 'self') {
            mediaSelection.innerHTML = `
                <h5>Selecione 1 mídia para exibição estática:</h5>
                <select name="adMedia" class="media-dropdown" required>
                    <option value="">Nenhuma</option>
                    ${getMediaOptions()}
                </select>
            `;
        } else if (mode === 'antena') {
            mediaSelection.innerHTML = `
                <h5>Selecione 2 mídias para exibição simultânea:</h5>
                <div style="display: flex; gap: 10px;">
                    <select name="adMedia" class="media-dropdown" required>
                        <option value="">Nenhuma</option>
                        ${getMediaOptions()}
                    </select>
                    <select name="adMedia" class="media-dropdown" required>
                        <option value="">Nenhuma</option>
                        ${getMediaOptions()}
                    </select>
                </div>
            `;
        }
    });
}

function getMediaOptions() {
    // Exemplo de opções de mídia
    const mediaFiles = [
        'bebe1.gif',
        'FaZe_Brian_-_Family_Guy_Trickshot_Thankyou_PewDiePie.mp4',
        'Logo_Solution_slogan_sem_fundo.png',
        'Logo_STM_sem_fundo.png',
        'paiacada.jpg',
        'POSTGRECAMPANHAS.drawio.png',
        'propaganda.png',
        'skeleton.gif',
        'skeleton3.gif',
        'video1.mp4'
    ];
    return mediaFiles.map(file => `<option value="${file}">${file}</option>`).join('');
}

function handlePreview(mediaFiles) {
    if (!selectedMode) {
        alert('Por favor, selecione um modo antes de visualizar.');
        return;
    }

    handleModeLogic(selectedMode, mediaFiles);
}

// Torna as funções acessíveis globalmente
window.setMode = setMode;
window.handlePreview = handlePreview;

document.addEventListener('DOMContentLoaded', function () {
    const hoverPreview = document.getElementById('hoverPreview');
    const hoverPreviewImage = document.getElementById('hoverPreviewImage');

    console.log('hoverPreview:', hoverPreview);
    console.log('hoverPreviewImage:', hoverPreviewImage);

    if (!hoverPreview || !hoverPreviewImage) {
        console.error('Elementos hoverPreview ou hoverPreviewImage não encontrados no DOM.');
        return;
    }

    // Delegação de eventos para inputs de rádio com valor "antena"
    document.body.addEventListener('mouseenter', function (event) {
        if (event.target.matches('input[type="radio"][value="antena"]')) {
            if (!hoverPreview || !hoverPreviewImage) return; // Verifique se os elementos existem
            hoverPreviewImage.src = '/static/images/Antena.png';
            hoverPreview.style.display = 'block';

            // Calcular a posição inicial
            const previewWidth = hoverPreview.offsetWidth;
            const pageWidth = window.innerWidth;

            let leftPosition = event.pageX + 10; // Posição padrão à direita do mouse
            if (leftPosition + previewWidth > pageWidth) {
                leftPosition = event.pageX - previewWidth - 10; // Ajustar para o lado esquerdo
            }

            hoverPreview.style.left = `${leftPosition}px`;
            hoverPreview.style.top = `${event.pageY + 10}px`;
        } else if (event.target.matches('input[type="radio"][value="inibicao"]')) {
            console.log('Hover iniciado para Inibição'); // Adicione este log para depuração
            hoverPreviewImage.src = '/static/images/Inibicao.png';
            hoverPreview.style.display = 'block';

            // Calcular a posição inicial
            const previewWidth = hoverPreview.offsetWidth;
            const pageWidth = window.innerWidth;

            let leftPosition = event.pageX + 10; // Posição padrão à direita do mouse
            if (leftPosition + previewWidth > pageWidth) {
                leftPosition = event.pageX - previewWidth - 10; // Ajustar para o lado esquerdo
            }

            hoverPreview.style.left = `${leftPosition}px`;
            hoverPreview.style.top = `${event.pageY + 10}px`;
        } else if (event.target.matches('input[type="radio"][value="self"]')) { // Adicionado para "self"
            console.log('Hover iniciado para Self');
            hoverPreviewImage.src = '/static/images/Self.png'; // Caminho para a imagem "Self.png"
            hoverPreview.style.display = 'block';

            const previewWidth = hoverPreview.offsetWidth;
            const pageWidth = window.innerWidth;

            let leftPosition = event.pageX + 10;
            if (leftPosition + previewWidth > pageWidth) {
                leftPosition = event.pageX - previewWidth - 10;
            }

            hoverPreview.style.left = `${leftPosition}px`;
            hoverPreview.style.top = `${event.pageY + 10}px`;
        }
    }, true);

    document.body.addEventListener('mousemove', function (event) {
        if (event.target.matches('input[type="radio"][value="antena"]')) {
            // Calcular a posição dinâmica
            const previewWidth = hoverPreview.offsetWidth;
            const pageWidth = window.innerWidth;

            let leftPosition = event.pageX + 10; // Posição padrão à direita do mouse
            if (leftPosition + previewWidth > pageWidth) {
                leftPosition = event.pageX - previewWidth - 10; // Ajustar para o lado esquerdo
            }

            hoverPreview.style.left = `${leftPosition}px`;
            hoverPreview.style.top = `${event.pageY + 10}px`;
        }
    });

    document.body.addEventListener('mouseleave', function (event) {
        if (
            event.target.matches('input[type="radio"][value="antena"]') ||
            event.target.matches('input[type="radio"][value="inibicao"]') ||
            event.target.matches('input[type="radio"][value="self"]') // Adicionado para "self"
        ) {
            hoverPreview.style.display = 'none';
        }
    }, true);
});