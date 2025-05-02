import { openViewMediaModal } from './main.js';

export function addAd(adContainer, adTemplate) {
    const adCount = adContainer.children.length;

    if (adCount < 6) { // Limitar a 6 anúncios por campanha
        if (!adTemplate) {
            console.error('O template de anúncio (adTemplate) não foi encontrado.');
            return;
        }
        const adClone = adTemplate.content.cloneNode(true);

        // Adicionar botão "Visualizar" ao anúncio
        const previewButton = document.createElement('button');
        previewButton.className = 'previewAd';
        previewButton.textContent = 'Visualizar';
        previewButton.style.marginTop = '10px';
        previewButton.addEventListener('click', function () {
            const mediaFiles = Array.from(previewButton.closest('.ad').querySelectorAll('select'))
                .map(select => select.value)
                .filter(value => value);

            if (mediaFiles.length > 0) {
                openViewMediaModal(mediaFiles); // Exibir o modal com as mídias selecionadas
            } else {
                alert('Nenhuma mídia selecionada para este anúncio.');
            }
        });
        adClone.querySelector('.ad').appendChild(previewButton);

        adContainer.appendChild(adClone);
    } else {
        alert('Máximo de 6 anúncios por campanha atingido.');
    }
}