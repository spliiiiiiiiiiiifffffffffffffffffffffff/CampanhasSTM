import { addCampaign } from './campaigns.js';
import { addAd } from './ads.js';
import { openModal, closeModal } from './modals.js';

document.addEventListener('DOMContentLoaded', function () {
    const campaignsDiv = document.getElementById('campaigns');
    const addCampaignButton = document.getElementById('addCampaign');
    const adTemplate = document.getElementById('adTemplate');

    // Configurar evento para o botão "Adicionar Campanha"
    if (addCampaignButton) {
        addCampaignButton.addEventListener('click', function () {
            const campaignCount = campaignsDiv.children.length;
            const campaignDiv = addCampaign(campaignsDiv, campaignCount);

            // Adicionar funcionalidade ao botão "Adicionar Anúncio"
            campaignDiv.querySelector('.addAd').addEventListener('click', function () {
                const adContainer = campaignDiv.querySelector('.adContainer');
                addAd(adContainer, adTemplate);
            });

            // Adicionar funcionalidade ao botão "Remover Campanha"
            campaignDiv.querySelector('.removeCampaign').addEventListener('click', function () {
                removeCampaign(campaignDiv);
            });
        });
    }
});

export function openViewMediaModal(mediaFiles) {
    const modal = document.getElementById('viewMediaModal');
    const mediaPreviewContainer = document.getElementById('mediaPreviewContainer');

    // Limpar o conteúdo anterior
    mediaPreviewContainer.innerHTML = '';

    // Adicionar as mídias ao modal
    mediaFiles.forEach(media => {
        const mediaElement = document.createElement(media.endsWith('.mp4') ? 'video' : 'img');
        mediaElement.src = `/static/uploads/${media}`;
        mediaElement.style.maxWidth = '100%';
        mediaElement.style.maxHeight = '400px';
        if (media.endsWith('.mp4')) {
            mediaElement.controls = true;
        }
        mediaPreviewContainer.appendChild(mediaElement);
    });

    // Exibir o modal
    modal.style.display = 'block';
}

export function closeViewMediaModal() {
    const modal = document.getElementById('viewMediaModal');
    modal.style.display = 'none';
}

// Tornar a função acessível globalmente
window.closeViewMediaModal = closeViewMediaModal;

