export function addCampaign(campaignsDiv, campaignCount) {
    const campaignDiv = document.createElement('div');
    campaignDiv.className = 'campaign';
    campaignDiv.innerHTML = `
        <h2>Campanha ${campaignCount + 1}</h2>
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

    // Funcionalidade para o botão "Salvar Campanha"
    campaignDiv.querySelector('.saveCampaign').addEventListener('click', function () {
        const campaignName = campaignDiv.querySelector('input[name="campaignName"]').value;
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