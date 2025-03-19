document.addEventListener('DOMContentLoaded', function() {
    const mapContainer = document.getElementById('neocronMap');
    const zoneInfo = document.getElementById('zoneInfo');
    const closeZoneInfo = document.getElementById('closeZoneInfo');
    const filters = document.querySelectorAll('.map-filter');

    const zones = [
        {
            id: 1,
            name: "Plaza",
            type: "city",
            description: "Centre névralgique de Neocron, la Plaza est le quartier central de la ville où se concentrent les commerces et services.",
            info1: "La Plaza est le centre-ville de Neocron, abritant de nombreux magasins, restaurants et services. C'est le principal hub social pour les joueurs.",
            info2: "Les points d'intérêt incluent le Dôme, le siège de CopBot, plusieurs boutiques d'implants et d'armes, ainsi que des clubs populaires.",
            image: "assets/NC2.SCREENSHOTS/PLAZA/NC2.PLAZA.04.JPG",
            tags: ["Centre-ville", "Commerce", "Services"],
            stats: [
            { name: "Niveau recommandé", value: "1-60" },
                { name: "Sécurité", value: "Haute" },
                { name: "Densité PNJ", value: "Très élevée" },
                { name: "Faction", value: "CopBot" }
            ]
        },
        {
            id: 2,
            name: "Via Rosso",
            type: "city",
            description: "Quartier rouge de Neocron, réputé pour ses clubs et ses établissements de divertissement pour adultes.",
            info1: "Via Rosso est le quartier chaud de Neocron, un lieu de divertissement et de plaisirs illicites. L'endroit est caractérisé par son ambiance néon et ses rues sombres.",
            info2: "On y trouve le célèbre Pepper Park, plusieurs clubs de danse et bars, ainsi que de nombreux appartements de joueurs.",
            image: "assets/NC2.SCREENSHOTS/VIA_ROSSO/NC2.VIA_ROSSO.06.JPG",
            tags: ["Divertissement", "Clubs", "Résidentiel"],
            stats: [
                { name: "Niveau recommandé", value: "5-60" },
                { name: "Sécurité", value: "Moyenne" },
                { name: "Densité PNJ", value: "Élevée" },
                { name: "Faction", value: "Indépendant" }
            ]
        },
        {
            id: 3,
            name: "Tech Haven",
            type: "city",
            description: "Quartier technologique de Neocron, siège de nombreuses entreprises high-tech et de recherche.",
            info1: "Tech Haven est le centre d'innovation de Neocron, abritant les sièges sociaux des principales corporations technologiques.",
            info2: "On y trouve le Dôme de Recherche, plusieurs laboratoires, ainsi que des boutiques d'implants et d'équipements de pointe.",
            image: "assets/NC2.SCREENSHOTS/TECH_HAVEN/NC2.TECH_HAVEN.01.JPG",
            tags: ["Technologie", "Recherche", "Corporatif"],
            stats: [
                { name: "Niveau recommandé", value: "10-60" },
                { name: "Sécurité", value: "Haute" },
                { name: "Densité PNJ", value: "Modérée" },
                { name: "Faction", value: "Diamond Real Estate" }
            ]
        },
        {
            id: 4,
            name: "Wasteland",
            type: "wasteland",
            description: "Terres désolées qui entourent Neocron, résultat de la Grande Guerre Nucléaire.",
            info1: "Le Wasteland est une zone dangereuse, irradiée et inhospitalière. C'est un lieu de PvP et de farming de ressources.",
            info2: "On y trouve des ruines d'anciennes installations, des camps de mutants et des points de forage pour le minage.",
            image: "assets/NC2.WASTELANDS.28.JPG",
            tags: ["PvP", "Ressources", "Danger"],
            stats: [
                { name: "Niveau recommandé", value: "20-60" },
                { name: "Sécurité", value: "Nulle" },
                { name: "Densité PNJ", value: "Faible" },
                { name: "Faction", value: "Aucune" }
            ]
        },
        {
            id: 5,
            name: "Outzone",
            type: "outzone",
            description: "Zone périphérique entre la ville et le Wasteland, partiellement civilisée.",
            info1: "L'Outzone est une zone tampon entre la civilisation de Neocron et les terres désolées. Elle est peuplée de diverses factions indépendantes.",
            info2: "On y trouve des petites communautés, des camps de réfugiés et des installations de traitement des ressources.",
            image: "assets/NC2.OUTZONE.12.JPG",
            tags: ["Périphérie", "Ressources", "Communautés"],
            stats: [
                { name: "Niveau recommandé", value: "15-40" },
                { name: "Sécurité", value: "Basse" },
                { name: "Densité PNJ", value: "Modérée" },
                { name: "Faction", value: "Diverses" }
            ]
        },
        {
            id: 6,
            name: "Dôme de Recherche",
            type: "special",
            description: "Centre de recherche avancée sur les technologies et les implants cybernetiques.",
            info1: "Le Dôme de Recherche est un complexe scientifique ultra-sécurisé où sont développées les technologies les plus avancées de Neocron.",
            info2: "On y trouve des laboratoires de recherche, des salles d'expérimentation et des installations de stockage de données.",
            image: "assets/NC2.CYBERSPACE.03.JPG",
            tags: ["Recherche", "Technologie", "Sécurisé"],
            stats: [
                { name: "Niveau recommandé", value: "30-60" },
                { name: "Sécurité", value: "Très haute" },
                { name: "Densité PNJ", value: "Faible" },
                { name: "Faction", value: "Gouvernement" }
            ]
        }
        // Ajoutez plus de zones selon vos besoins
    ];
    
    // Création de la grille de la carte
    function createMap() {
        // Définir le nombre de cellules (14x14 = 196, proche de 204)
        const gridSize = 14;
        const totalCells = gridSize * gridSize;
        
        // Créer les cellules
        for (let i = 0; i < totalCells; i++) {
            const cell = document.createElement('div');
            cell.className = 'map-cell';
            
            // Assignation aléatoire de zones pour démonstration
            // Dans une version réelle, vous auriez une correspondance précise
            const zoneIndex = i % zones.length;
            const zone = zones[zoneIndex];
            
            cell.dataset.id = zone.id;
            cell.classList.add(zone.type);
            
            // Ajouter le nom de la zone pour les cellules qui ont une zone assignée
            if (i < zones.length * 3) { // Multiplier par 3 pour avoir plus de cellules avec des noms
                const nameSpan = document.createElement('span');
                nameSpan.className = 'map-cell-name';
                nameSpan.textContent = zone.name;
                cell.appendChild(nameSpan);
            }
            
            // Ajouter l'événement de clic
            cell.addEventListener('click', function() {
                showZoneInfo(zone.id);
            });
            
            mapContainer.appendChild(cell);
        }
    }
    
    // Afficher les informations d'une zone
    function showZoneInfo(zoneId) {
        // Trouver la zone par son ID
        const zone = zones.find(z => z.id === zoneId);
        if (!zone) return;
        
        // Mettre à jour les informations de la zone
        document.getElementById('zoneTitle').textContent = zone.name;
        document.getElementById('zoneDescription').textContent = zone.description;
        document.getElementById('zoneInfo1').textContent = zone.info1;
        document.getElementById('zoneInfo2').textContent = zone.info2;
        
        // Mettre à jour l'image
        document.getElementById('zoneImage').style.backgroundImage = `url(${zone.image})`;
        
        // Mettre à jour les tags
        const tagsContainer = document.getElementById('zoneTags');
        tagsContainer.innerHTML = '';
        zone.tags.forEach(tag => {
            const tagElement = document.createElement('div');
            tagElement.className = 'zone-tag';
            tagElement.textContent = tag;
            tagsContainer.appendChild(tagElement);
        });
        
        // Mettre à jour les statistiques
        const statsContainer = document.getElementById('zoneStats');
        statsContainer.innerHTML = '';
        zone.stats.forEach(stat => {
            const statElement = document.createElement('div');
            statElement.className = 'zone-stat';
            statElement.innerHTML = `
                <div class="zone-stat-title">${stat.name}</div>
                <div class="zone-stat-value">${stat.value}</div>
            `;
            statsContainer.appendChild(statElement);
        });
        
        // Afficher le panneau d'information
        zoneInfo.classList.add('active');
        
        // Marquer la cellule active
        const allCells = document.querySelectorAll('.map-cell');
        allCells.forEach(cell => {
            if (parseInt(cell.dataset.id) === zoneId) {
                cell.classList.add('active');
            } else {
                cell.classList.remove('active');
            }
        });
        
        // Faire défiler jusqu'aux informations de la zone
        zoneInfo.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Fermer le panneau d'information
    closeZoneInfo.addEventListener('click', function() {
        zoneInfo.classList.remove('active');
        
        // Retirer la classe active de toutes les cellules
        const allCells = document.querySelectorAll('.map-cell');
        allCells.forEach(cell => cell.classList.remove('active'));
    });
    
    // Filtrer les zones
    filters.forEach(filter => {
        filter.addEventListener('click', function() {
            // Mettre à jour l'état actif du filtre
            filters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
            
            const filterType = this.dataset.filter;
            const cells = document.querySelectorAll('.map-cell');
            
            cells.forEach(cell => {
                if (filterType === 'all' || cell.classList.contains(filterType)) {
                    cell.style.display = 'block';
                } else {
                    cell.style.display = 'none';
                }
            });
        });
    });
    
    // Initialiser la carte
    createMap();
});