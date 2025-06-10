import { openViewMediaModal } from './main.js';

export function addAd(adContainer, adTemplate, mode) {
    const adCount = adContainer.children.length;

    if (adCount < 6) { // Limitar a 6 anúncios por campanha
        if (!adTemplate) {
            console.error('O template de anúncio (adTemplate) não foi encontrado.');
            return;
        }
        const adClone = adTemplate.content.cloneNode(true);

        // Personalizar o anúncio com base no modo selecionado
        const mediaSelection = adClone.querySelector('.media-selection');
        const adTitle = adClone.querySelector('h4');
        if (mode === 'inibicao') {
            adTitle.textContent = `Anúncio ${adCount + 1} (Modo: Inibição)`;
            mediaSelection.innerHTML = `
                <h5>Selecione 1 mídia para exibição em sequência:</h5>
                <select name="adMedia" class="media-dropdown" required>
                    <option value="">Nenhuma</option>
                   
                </select>
            `;
        } else if (mode === 'self') {
            adTitle.textContent = `Anúncio ${adCount + 1} (Modo: Self)`;
            mediaSelection.innerHTML = `
                <h5>Selecione 1 mídia para exibição estática:</h5>
                <select name="adMedia" class="media-dropdown" required>
                    <option value="">Nenhuma</option>
                </select>
            `;
        } else if (mode === 'antena') {
            adTitle.textContent = `Anúncio ${adCount + 1} (Modo: Antena)`;
            mediaSelection.innerHTML = `
                <h5>Selecione 2 mídias para exibição simultânea:</h5>
                <div style="display: flex; gap: 10px;">
                    <select name="adMedia" class="media-dropdown" required>
                        <option value="">Nenhuma</option>
                        
                    </select>
                    <select name="adMedia" class="media-dropdown" required>
                        <option value="">Nenhuma</option>
                        
                    </select>
                </div>
            `;
        }

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

        // Adicionar botão "Remover" ao anúncio
        const removeButton = document.createElement('button');
        removeButton.className = 'removeAd';
        removeButton.textContent = 'x';
        removeButton.style.position = 'absolute';
        removeButton.style.top = '5px';
        removeButton.style.right = '5px';
        removeButton.style.backgroundColor = 'red';
        removeButton.style.color = 'white';
        removeButton.style.border = 'none';
        removeButton.style.borderRadius = '50%';
        removeButton.style.width = '20px';
        removeButton.style.height = '20px';
        removeButton.style.cursor = 'pointer';
        removeButton.addEventListener('click', function () {
            removeButton.closest('.ad').remove(); // Remove o elemento pai mais próximo com a classe .ad
        });
        adClone.querySelector('.ad').appendChild(removeButton);

        adContainer.appendChild(adClone);

        // Preencher os dropdowns do anúncio com mídias do modo correto
        fillMediaDropdownsByMode(mode, adContainer.lastElementChild);
    } else {
        alert('Máximo de 6 anúncios por campanha atingido.');
    }
}


function fillMediaDropdownsByMode(mode, adCloneElement) {
    fetch(`/campaigns/media_files_by_mode/${mode}`)
        .then(response => response.json())
        .then(data => {
            const mediaFiles = data.media_files || [];
            const dropdowns = adCloneElement.querySelectorAll('.media-dropdown');
            dropdowns.forEach(dropdown => {
                dropdown.innerHTML = '<option value="">Nenhuma</option>';
                mediaFiles.forEach(media => {
                    const filename = media.filename || media;
                    dropdown.innerHTML += `<option value="${filename}">${filename}</option>`;
                });
            });
        });
}
