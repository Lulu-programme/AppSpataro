const App = {
    // Gestion des tableaux dynamiques
    initializeTabs: function () {
        const buttons = document.querySelectorAll('.btn-main');
        const contents = document.querySelectorAll('.main-content');

        if (buttons.length === 0 || contents.length === 0) {
            console.warn("Aucun tableau ou bouton à gérer sur cette page.");
            return;
        }

        console.log("Boutons et tableaux trouvés :", buttons);

        buttons.forEach((button, index) => {
            button.addEventListener('click', () => {
                // Masquer tous les contenus
                contents.forEach(content => {
                    content.style.display = 'none';
                });

                // Désactiver tous les boutons
                buttons.forEach(btn => {
                    btn.classList.remove('active');
                });

                // Afficher le contenu correspondant et activer le bouton
                contents[index].style.display = 'flex';
                button.classList.add('active');
            });
        });
    },

    // Gestion des groupes dynamiques
    initializeDynamicGroups: function (buttonClass, containerClass, products) {
        const buttons = document.querySelectorAll(`.${buttonClass}`);
        const containers = document.querySelectorAll(`.${containerClass}`);

        if (buttons.length === 0 || containers.length === 0) {
            console.warn("Aucun bouton ou conteneur pour les groupes dynamiques sur cette page.");
            return;
        }

        let groupIndex = document.querySelectorAll(`.${containerClass} .group`).length; // Compte les groupes existants

        buttons.forEach((button, containerIndex) => {
            button.addEventListener('click', () => {
                console.log("Ajout d'un groupe dans le conteneur :", containerIndex);

                // Crée un nouvel élément HTML pour le groupe
                const newGroup = document.createElement('div');
                newGroup.classList.add('group');
                newGroup.classList.add('add');

                // Génère le contenu HTML du groupe
                let groupContent = `
                    <label for="cmr">Numéro de CMR :</label>
                    <input type="text" name="cmr[${groupIndex}][number]">

                    <label for="command">Numéro de Commande :</label>
                    <input type="text" name="cmr[${groupIndex}][command]">

                    <label for="product">Produits :</label>
                `;

                // Ajoute dynamiquement les produits ADR
                groupContent += products.map(product => `
                    <div>
                        <input type="checkbox" id="product-${groupIndex}-${product.id}" name="cmr[${groupIndex}][product]" value="${product.id}">
                        <label for="product-${groupIndex}-${product.id}">${product.name}</label>
                    </div>
                `).join('');

                // Ajoute le champ pour le poids
                groupContent += `
                    <label for="weight">Poids :</label>
                    <input type="number" name="cmr[${groupIndex}][weight]">
                `;

                // Insère le contenu dans le nouvel élément
                newGroup.innerHTML = groupContent;

                // Ajoute le nouveau groupe dans le conteneur correspondant
                containers[containerIndex].appendChild(newGroup);

                // Incrémente l'index pour le prochain groupe
                groupIndex++;
            });
        });
    }
};