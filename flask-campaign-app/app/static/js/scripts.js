document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const uploadForm = document.getElementById('uploadForm');
    const campaignForm = document.getElementById('campaignForm');
    const adTemplate = document.getElementById('adTemplate');
    const campaignsDiv = document.getElementById('campaigns');

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            // Add form validation logic here
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            if (!username || !password) {
                event.preventDefault();
                alert('Please fill in both fields.');
            }
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener('submit', function (event) {
            // Add media upload handling logic here
            const mediaFiles = document.getElementById('mediaFiles').files;
            if (mediaFiles.length === 0) {
                event.preventDefault();
                alert('Please select at least one media file to upload.');
            }
        });
    }

    if (campaignForm) {
        campaignForm.addEventListener('submit', function (event) {
            // Add campaign configuration validation logic here
            const campaignName = document.getElementById('campaignName').value;
            if (!campaignName) {
                event.preventDefault();
                alert('Please enter a campaign name.');
            }
        });
        document.addEventListener('DOMContentLoaded', function () {
            // Verifica se os elementos "addCampaign" e "addMachinesForm" existem no DOM
            const addCampaignButton = document.getElementById('addCampaign');
            const addMachinesForm = document.getElementById('addMachinesForm');

            if (addCampaignButton) {
                console.log('Botão "Adicionar Campanha" encontrado.');
                addCampaignButton.addEventListener('click', function () {
                    console.log('Botão "Adicionar Campanha" clicado!');
                });
            } else {
                console.error('Elemento com ID "addCampaign" não encontrado no DOM.');
            }

            if (addMachinesForm) {
                console.log('Formulário "Adicionar Máquinas" encontrado.');
                addMachinesForm.addEventListener('submit', function (event) {
                    event.preventDefault();
                    console.log('Formulário "Adicionar Máquinas" enviado!');
                });
            } else {
                console.error('Elemento com ID "addMachinesForm" não encontrado no DOM.');
            }
        });

        let addCampaignButton = document.getElementById('addCampaign');

        // Remove any existing event listeners to avoid duplicates
        addCampaignButton.replaceWith(addCampaignButton.cloneNode(true));
        addCampaignButton = document.getElementById('addCampaign'); // Reatribuição permitida com let

        addCampaignButton.addEventListener('click', function () {
            console.log('Botão "Adicionar Campanha" clicado!');
            const campaignsDiv = document.getElementById('campaigns');
            const campaignCount = campaignsDiv.children.length;

            if (campaignCount < 10) { // Permitir até 10 campanhas
                const campaignDiv = createCampaign(campaignCount + 1);
                campaignsDiv.appendChild(campaignDiv);
            } else {
                alert('Máximo de 10 campanhas atingido.');
            }
        });

        campaignForm.addEventListener('change', function (event) {
            if (event.target.classList.contains('media-dropdown')) {
                const selectedFile = event.target.value;
                const previewContainer = event.target.closest('.ad').querySelector('.media-preview');

                // Clear the preview container
                previewContainer.innerHTML = '';

                // Determine if the file is an image or video
                if (selectedFile.endsWith('.mp4')) {
                    const video = document.createElement('video');
                    video.src = `/static/uploads/${selectedFile}`;
                    video.controls = true;
                    previewContainer.appendChild(video);
                } else {
                    const img = document.createElement('img');
                    img.src = `/static/uploads/${selectedFile}`;
                    previewContainer.appendChild(img);
                }
            }
        });
    }

    if (campaignForm) {
        campaignForm.addEventListener('submit', function(event) {
            // Add campaign configuration validation logic here
            const campaignName = document.getElementById('campaignName').value;
            if (!campaignName) {
                event.preventDefault();
                alert('Please enter a campaign name.');
            }
        });

        const addCampaignButton = document.getElementById('addCampaign');

        // Remove any existing event listeners to avoid duplicates
        addCampaignButton.replaceWith(addCampaignButton.cloneNode(true));
        const newAddCampaignButton = document.getElementById('addCampaign');

        newAddCampaignButton.addEventListener('click', function () {
            const campaignsDiv = document.getElementById('campaigns');
            const campaignCount = campaignsDiv.children.length;

            if (campaignCount < 10) { // Allow up to 10 campaigns
                const campaignDiv = document.createElement('div');
                campaignDiv.className = 'campaign';
                campaignDiv.innerHTML = `
                    <h2>Campanha ${campaignCount + 1}</h2>
                    <input type="text" name="campaignName" placeholder="Nome da Campanha" required>
                    <div class="ads">
                        <h3>Anúncios</h3>
                        <div class="button-group">
                            <button type="button" class="addAd">Adicionar Anúncio</button>
                            <button type="button" class="removeCampaign">Remover Campanha</button>
                            <button type="button" class="previewAd" style="display: none;">Visualizar</button>
                        </div>
                        <div class="adContainer"></div>
                    </div>
                `;
                campaignsDiv.appendChild(campaignDiv);

                // Add functionality to the "Adicionar Anúncio" button
                campaignDiv.querySelector('.addAd').addEventListener('click', function () {
                    const adContainer = campaignDiv.querySelector('.adContainer');
                    const adCount = adContainer.children.length;

                    if (adCount < 6) {
                        if (!adTemplate) {
                            console.error('O template de anúncio (adTemplate) não foi encontrado.');
                            return;
                        }
                        const adClone = adTemplate.content.cloneNode(true);
                        adContainer.appendChild(adClone);

                        // Check if there is at least one ad and show the "Visualizar" button
                        const previewButton = campaignDiv.querySelector('.previewAd');
                        previewButton.style.display = 'inline-block';
                    } else {
                        alert('Máximo de 6 anúncios por campanha atingido.');
                    }
                });
            }
        }); // Certifique-se de que este fechamento está correto
    }

    // Corrigir o botão "Fechar" do modal de preview
const closePreviewButton = document.getElementById('closePreview');
const previewContainer = document.getElementById('previewContainer');

if (closePreviewButton) {
    closePreviewButton.addEventListener('click', function () {
        console.log('Botão "Fechar" clicado!');
        previewContainer.style.display = 'none'; // Oculta o modal
    });
} else {
    console.error('Botão "Fechar" do modal de preview não encontrado.');
}

    function createCampaign(campaignNumber) {
        const campaignDiv = document.createElement('div');
        campaignDiv.className = 'campaign';
        campaignDiv.innerHTML = `
            <h2>Campanha ${campaignNumber}</h2>
            <input type="text" name="campaignName" placeholder="Nome da Campanha" required>
            <div class="ads">
                <div class="button-group">
                    <button type="button" class="addAd">Adicionar Anúncio</button>
                    <button type="button" class="removeCampaign">Remover Campanha</button>
                    <button type="button" class="previewAd" style="display: none;">Visualizar</button>
                </div>
                <div class="adContainer"></div>
            </div>
        `;

        return campaignDiv;
    }
});