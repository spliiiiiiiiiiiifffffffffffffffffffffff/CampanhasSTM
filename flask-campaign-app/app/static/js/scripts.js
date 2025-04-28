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
// Função para abrir o modal de adicionar máquinas
function openAddMachinesModal(campaignName) {
    const addMachinesModal = document.getElementById('addMachinesModal');
    const machinesList = document.getElementById('machinesList');

    if (!addMachinesModal || !machinesList) {
        console.error('Modal ou lista de máquinas não encontrado.');
        return;
    }

    // Limpa a lista de máquinas
    machinesList.innerHTML = '';

    // Carregar os IPs de machines.json
    fetch('/static/data/machines.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao carregar máquinas: ${response.statusText}`);
            }
            return response.json();
        })
        .then(machines => {
            // Carregar associações de associations.json
            return fetch('/static/data/associations.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro ao carregar associações: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(associations => {
                    // Processar máquinas e associações
                    machines.forEach(machine => {
                        const isAssociated = associations.find(
                            assoc => assoc.machine_ip === machine
                        );

                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.name = 'machine';
                        checkbox.value = machine;
                        checkbox.id = `machine-${machine}`;
                        checkbox.checked = !!isAssociated; // Marcar como selecionado se estiver associado a qualquer campanha
                        checkbox.disabled = false; // Permitir que o IP seja selecionado/desmarcado

                        const label = document.createElement('label');
                        label.htmlFor = `machine-${machine}`;
                        label.textContent = machine;

                        const listItem = document.createElement('div');
                        listItem.appendChild(checkbox);
                        listItem.appendChild(label);

                        machinesList.appendChild(listItem);
                    });
                });
        })
        .catch(error => {
            console.error('Erro ao carregar máquinas ou associações:', error);
        });

    // Exibe o modal
    addMachinesModal.style.display = 'block';

    // Salvar a campanha associada no modal
    addMachinesModal.dataset.campaignName = campaignName;
}

// Função para fechar o modal de adicionar máquinas
function closeAddMachinesModal() {
    const addMachinesModal = document.getElementById('addMachinesModal');
    if (addMachinesModal) {
        addMachinesModal.style.display = 'none';
    }
}

// Função para salvar as associações
function saveAssociations() {
    const addMachinesModal = document.getElementById('addMachinesModal');
    const machinesList = document.getElementById('machinesList');
    const campaignName = addMachinesModal.dataset.campaignName;

    if (!campaignName) {
        console.error('Nome da campanha não encontrado no modal.');
        return;
    }

    // Obter os IPs selecionados
    const selectedMachines = Array.from(machinesList.querySelectorAll('input[name="machine"]:checked'))
        .map(checkbox => checkbox.value);

    if (selectedMachines.length === 0) {
        alert('Selecione pelo menos um IP.');
        return;
    }

    // Enviar as associações para o servidor
    fetch('/save_association', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            campaign_name: campaignName,
            machines: selectedMachines,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                closeAddMachinesModal();
            } else {
                alert('Erro ao salvar associações: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro ao salvar associações:', error);
        });
}

// Função para abrir o modal de edição de campanha
function openEditModal(campaignName) {
    const editModal = document.getElementById('editModal');
    const editCampaignTitle = document.getElementById('editCampaignTitle');
    const editCampaignContent = document.getElementById('editCampaignContent');

    if (!editModal || !editCampaignTitle || !editCampaignContent) {
        console.error('Modal de edição ou elementos relacionados não encontrados.');
        return;
    }

    // Define o título do modal
    editCampaignTitle.textContent = `Editar Campanha: ${campaignName}`;

    // Limpa o conteúdo anterior do modal
    editCampaignContent.innerHTML = '';

    // Carregar campanhas e exibir os anúncios da campanha selecionada
    fetch('/static/data/campaigns.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao carregar campanhas: ${response.statusText}`);
            }
            return response.json();
        })
        .then(campaigns => {
            // Carregar mídias disponíveis na galeria
            return fetch('/gallery')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro ao carregar mídias: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(mediaFiles => {
                    // Encontrar a campanha selecionada
                    const campaign = campaigns.find(camp => camp.name === campaignName);

                    if (!campaign) {
                        console.error(`Campanha "${campaignName}" não encontrada.`);
                        return;
                    }

                    // Exibir os anúncios da campanha
                    campaign.ads.forEach((ad, index) => {
                        const adDiv = document.createElement('div');
                        adDiv.className = 'ad-edit';
                        adDiv.innerHTML = `
                            <h4>Anúncio ${index + 1}</h4>
                            <div class="media-list">
                                ${ad.media
                                    .map(
                                        (media, mediaIndex) => `
                                        <div>
                                            <label for="media-${index}-${mediaIndex}">Mídia ${mediaIndex + 1}:</label>
                                            <select id="media-${index}-${mediaIndex}" name="media">
                                                ${mediaFiles
                                                    .map(
                                                        file => `
                                                        <option value="${file}" ${
                                                            file === media ? 'selected' : ''
                                                        }>${file}</option>
                                                    `
                                                    )
                                                    .join('')}
                                            </select>
                                        </div>
                                    `
                                    )
                                    .join('')}
                            </div>
                        `;
                        editCampaignContent.appendChild(adDiv);
                    });

                    // Adicionar botão para salvar alterações
                    const saveButton = document.createElement('button');
                    saveButton.textContent = 'Salvar Alterações';
                    saveButton.className = 'save-btn';
                    saveButton.addEventListener('click', () => saveCampaignEdits(campaignName));
                    editCampaignContent.appendChild(saveButton);
                });
        })
        .catch(error => {
            console.error('Erro ao carregar campanhas ou mídias:', error);
        });

    // Exibe o modal
    editModal.style.display = 'block';
}

// Função para salvar as edições da campanha
function saveCampaignEdits(campaignName) {
    const editCampaignContent = document.getElementById('editCampaignContent');
    const ads = Array.from(editCampaignContent.querySelectorAll('.ad-edit')).map(adDiv => {
        const media = Array.from(adDiv.querySelectorAll('select[name="media"]')).map(
            dropdown => dropdown.value
        );
        return { media };
    });

    // Enviar as alterações para o servidor
    fetch('/save_campaign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: campaignName,
            ads,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                closeEditModal();
            } else {
                alert('Erro ao salvar alterações.');
            }
        })
        .catch(error => {
            console.error('Erro ao salvar alterações:', error);
        });
}