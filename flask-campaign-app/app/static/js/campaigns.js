export function addCampaign(campaignsDiv, campaignCount) {
    const campaignDiv = document.createElement('div');
    campaignDiv.className = 'campaign';
    campaignDiv.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <h2>Campanha ${campaignCount + 1}</h2>
            <div class="mode-buttons">
                <label>
                    <input type="radio" name="mode-${campaignCount}" value="inibicao" onclick="setMode('inibicao', this.closest('.campaign'))"> Inibição
                </label>
                <label>
                    <input type="radio" name="mode-${campaignCount}" value="self" onclick="setMode('self', this.closest('.campaign'))"> Self
                </label>
                <label>
                    <input type="radio" name="mode-${campaignCount}" value="antena" onclick="setMode('antena', this.closest('.campaign'))"> Antena
                </label>
            </div>
        </div>
        <input type="text" name="campaignName" placeholder="Nome da Campanha" required>
        <div class="ads">
            <div class="button-group">
                <button type="button" class="addAd">Adicionar Anúncio</button>
                <button type="button" class="removeCampaign">Remover Campanha</button>
                <button type="button" class="saveCampaign">Salvar Campanha</button>
            </div>
            <div class="adContainer"></div>
        </div>
    `;
    campaignsDiv.appendChild(campaignDiv);

    // Adicionar listener para atualizar dropdowns ao mudar o modo
    const modeRadios = campaignDiv.querySelectorAll('input[name^="mode-"]');
    modeRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            const selectedMode = campaignDiv.querySelector('input[name^="mode-"]:checked').value;
            campaignDiv.querySelectorAll('.ad').forEach(adDiv => {
                fillMediaDropdownsByMode(selectedMode, adDiv);
            });
        });
    });

    // Funcionalidade para o botão "Salvar Campanha"
    campaignDiv.querySelector('.saveCampaign').addEventListener('click', function () {
        const campaignName = campaignDiv.querySelector('input[name="campaignName"]').value;
        const selectedMode = campaignDiv.querySelector('input[name^="mode-"]:checked').value;
        const ads = Array.from(campaignDiv.querySelectorAll('.ad')).map(ad => {
            const media = Array.from(ad.querySelectorAll('select')).map(select => select.value);
            return { media };
        });

        if (!campaignName) {
            alert('Por favor, insira um nome para a campanha.');
            return;
        }

        const campaignData = {
            name: campaignName,
            mode: selectedMode, // <-- Adicione esta linha
            ads: ads
        };

        // Enviar os dados da campanha para o servidor
        fetch('/campaigns/save_campaign', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(campaignData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Erro ao salvar a campanha:', error);
            });
    });

    return campaignDiv;
}
function loadMediaOptions(campaignName) {
    fetch(`/campaigns/media_files/${campaignName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ao carregar mídias: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const mediaFiles = data.media_files;
            const tags = data.tags || {};
            const dropdowns = document.querySelectorAll('.media-dropdown');
            dropdowns.forEach(dropdown => {
                dropdown.innerHTML = '<option value="">Nenhuma</option>';
                mediaFiles.forEach(file => {
                    const displayName = tags[file] ? `tag: ${tags[file]}` : file;
                    const option = document.createElement('option');
                    option.value = file;
                    option.textContent = displayName;
                    dropdown.appendChild(option);
                });
            });
        })
        .catch(error => {
            console.error('Erro ao carregar mídias:', error);
        });
}

// Chamar a função ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    const campaignElem = document.querySelector('.campaign');
    if (campaignElem) {
        const campaignName = campaignElem.dataset.campaignName;
        loadMediaOptions(campaignName);
    }
});

// fetch('/gallery/media_files')
 //   .then(response => response.json())
//  .then(data => {
   //     const mediaFiles = data.media_files; // array
    //    const tags = data.tags || {};
    //    const dropdowns = document.querySelectorAll('.media-dropdown');
     //   dropdowns.forEach(dropdown => {
     //       dropdown.innerHTML = '<option value="">Nenhuma</option>';
      //      mediaFiles.forEach(file => {
      //          const displayName = tags[file] ? `tag: ${tags[file]}` : file;
      //          const option = document.createElement('option');
      //          option.value = file;
      //          option.textContent = displayName;
      //          dropdown.appendChild(option);
      //      });
     //   });
  //  });

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

