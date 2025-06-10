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
                const mode = campaignDiv.querySelector('input[name^="mode-"]:checked');
                if (!mode) {
                    alert('Por favor, selecione um modo para a campanha antes de adicionar anúncios.');
                    return;
                }

                const adContainer = campaignDiv.querySelector('.adContainer');
                addAd(adContainer, adTemplate, mode.value);
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
    modal.style.display = 'block';

    // Chamar a lógica de preview com base no modo selecionado
    handlePreview(mediaFiles);
}

export function closeViewMediaModal() {
    const modal = document.getElementById('viewMediaModal');
    modal.style.display = 'none';
}

// Tornar a função acessível globalmente
window.closeViewMediaModal = closeViewMediaModal;

