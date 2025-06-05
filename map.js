        // Définition des zones pour chaque carte
        const caligaZones = [
            {   
                id: "O1",
                title: "Outzone 1",
                coords: "1024,256,776,1",
                description: "Première zone de Neocron. Aussi un marché.",
                activities: [
                    "Marché d'Outzone"
                ]
            },
            {
                id: "O2",
                title: "Outzone 2",
                coords: "510,254,776,1",
                description: "Deuxième zone de Neocron. Possède la même carte que le tutoriel du jeu.",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "O3",
                title: "Outzone 3",
                coords: "254,767,510,1026",
                description: "Troisème zone d'Outzone",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "O4",
                title: "Outzone 4",
                coords: "510,255,256,0",
                description: "Quatrième zone d'Outzone",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "O5",
                title: "Outzone 5",
                coords: "254,258,0,0",
                description: "Cinquième zone d'Outzone",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "O6",
                title: "Outzone 6",
                coords: "256,255,510,513",
                description: "Sixième zone d'Outzone",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "O7",
                title: "Outzone 7",
                coords: "510,767,256,512",
                description: "Septième zone d'Outzone",
                activities: [
                    "Bâtiment vide"
                ]
            },
            {
                id: "O8",
                title: "Outzone 8",
                coords: "1535,514,1280,767",
                description: "Huitième Secteur d'Outzone",
                activities: [
                    "Prison de Neocron (Zone extrêmement dangeureuse)"
                ]
            },
            {
                id: "O9",
                title: "Outzone 9",
                coords: "766,513,1021,769",
                description: "Neuvième Zone d'Outzone.",
                activities: [
                    "Bâtiment secret de Brotherhood Of Crahn",
                    "Sortie sur A-07 et A-06"
                ]
            },
            {
                id: "S1",
                title: "Secret Passage 1",
                coords: "1026,512,1279,768",
                description: "Premier passage secret, elle est utile pour certaines missions Epic",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "S2",
                title: "Secret Passage 2",
                coords: "1280,766,1535,1026",
                description: "Deuxième passage secret, elle est utile pour certaines missions Epic",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "I1",
                title: "Industrial Sector 1",
                coords: "765,770,1021,1023",
                description: "Première zone du Secteur Industriel.",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "I2",
                title: "Industial Sector 2",
                coords: "510,767,765,1023",
                description: "Deuxième zone du Secteur Industriel.",
                activities: [
                    "Aucune activités significatives"
                ]
            },
            {
                id: "Pepper Park 1",
                title: "Pepper Park 1",
                coords: "766,1279,1023,1537",
                description: "Première section de la Plaza, Pepper Park Sec-1 est une zone commerciale animée avec de nombreuses boutiques et services. C'est un point de rencontre populaire pour les habitants.",
                activities: [
                    "NeoFrag1",
                    "Club Veronique",
                    "Tsunami Syndicate HQ"
                ]
            },
            {
                id: "PP2",
                title: "Pepper Park 2",
                coords: "766,1024,1021,1279",
                description: "Deuxième section de Pepper Park, Pepper Park Sec-2 abrite le plus de divertissements avec ses bars, clubs et casinos.",
                activities: [
                    "NeoFrag2",
                    "Black Dragon HQ",
                    "Tiki Tornado Club",
                    "The mysterious Maze"
                ]
            },
            {
                id: "PP3",
                title: "Pepper Park Sec-3",
                coords: "1277,1025,1021,1281",
                description: "Troisième section de Pepper Park, Pepper Park Sec-3 est connue pour ses secrets.",
                activities: [
                    "Brotherhood Of Crahn HQ",
                    "Bump Asylum",
                    "Smugglers Cave",
                    "Vendeurs peu cher"
                ]
            },
            {
                id: "P1",
                title: "Plaza 1",
                coords: "1532,1378,1790,1633",
                description: "Première section de Plaza, elle est la zone la mieux peuplée de toutes les zones. Vous y trouverez le lobby où tous les joueurs se regroupent",
                activities: [
                    "Typherra Memorial",
                    "Con Center",
                    "Vendeurs divers",
                    "City Administration HQ",
                    "Agence immoblières Diamond"
                ]
            },
            {
                id: "P2",
                title: "Plaza 2",
                coords: "1279,1379,1532,1633",
                description: "Deuxième section de Plaza, c'est une zone où se mêlent petits commerces et activités de travail.",
                activities: [
                    "Job Center",
                    "Protopharm Laboratory",
                    "Missions d'infiltration"
                ]
            },
            {
                id: "P3",
                title: "Plaza 3",
                coords: "1021,1379,1277,1633",
                description: "Troisième section de Plaza, moins développée que les autres zones du quartier. On y trouve des entrepôts et des logements.",
                activities: [
                    "Diamond Real Estate HQ",
                    "ASG (Vendeur de véhicue)",
                    "Vendeurs divers"
                ]
            },
            {
                id: "P4",
                title: "Plaza 4",
                coords: "1535,1665,1790,1919",
                description: "Quatrième section de Plaza, elle est la moins peuplée des 4 secteurs de Plaza.",
                activities: [
                    "NEXT HQ",
                    "ASG (Vendeur de véhicule)",
                    "Vendeurs divers"
                ]
            },
            {
                id: "V1",
                title: "Via Rosso 1",
                coords: "1279,1920,1535,2176",
                description: "Première section de Via Rosso, Via Rosso Sec-1 est un quartier industriel avec de nombreuses usines et centres de production.",
                activities: [
                    "Zoo de Neocron",
                    "Vendeurs de décorations",
                    "Biotech Systems HQ",
                    "Archer & Wesson"
                ]
            },
            {
                id: "V2",
                title: "Via Rosso 2",
                coords: "1279,1665,1535,1919",
                description: "Deuxième section de Via Rosso, Via Rosso Sec-2 abrite des installations de recyclage et des centres de traitement des déchets.",
                activities: [
                    "Tangent Technologies",
                    "Vendeurs divers"
                ]
            },
            {
                id: "V3",
                title: "Via Rosso 3",
                coords: "1021,1921,1279,2176",
                description: "Troisième section de Via Rosso, Via Rosso est la zone avec les meilleurs vendeurs.",
                activities: [
                    "NeoKea",
                    "NCPD Police Departement",
                    "ASG (Vendeurs de véhicules)"
                ]
            }
        ];

        const wastelandsZones = [
            {
                id: "NC",
                title: "Neocron",
                coords: "592,1139,584,1136,585,1116,596,1103,636,1102,660,1120,711,1124,714,1112,697,1093,694,1075,700,1068,724,1068,751,1096,779,1096,783,1120,806,1147,577,1151",
                description: "Vaste région aride et balayée par des vents radioactifs. Des caravanes de nomades y circulent entre les rares points d'eau et abris.",
                activities: [
                    "Survie en environnement hostile",
                    "Chasse aux créatures mutantes",
                    "Exploration des bunkers abandonnés",
                    "Escorte de caravanes"
                ]
            },
            {
                id: "W2",
                title: "Ruines de l'Ancienne Mégapole",
                coords: "490,1037,575,1131",
                description: "Les vestiges d'une immense ville d'avant-guerre. Ces ruines urbaines sont désormais le territoire de bandes organisées et de créatures mutantes.",
                activities: [
                    "Récupération de technologies anciennes",
                    "Affrontements avec des gangs rivaux",
                    "Exploration urbaine dangereuse",
                    "Recherche de bunkers cachés"
                ]
            },
            {
                id: "W3",
                title: "Zone de Cratères",
                coords: "300,500,700,700",
                description: "Région ravagée par d'intenses bombardements lors de la grande guerre. Les cratères sont maintenant des lacs toxiques et des gouffres sans fond.",
                activities: [
                    "Extraction de minéraux rares",
                    "Étude des anomalies radioactives",
                    "Chasse aux créatures abyssales",
                    "Récupération d'équipements militaires"
                ]
            },
            {
                id: "W4",
                title: "Forêt Pétrifiée",
                coords: "100,300,300,700",
                description: "Ancienne zone boisée transformée par les radiations. Les arbres pétrifiés abritent désormais des formes de vie mutantes et des phénomènes inexpliqués.",
                activities: [
                    "Collecte de spécimens biologiques",
                    "Cartographie des zones inexploitées",
                    "Études des phénomènes paranormaux",
                    "Recherche de technologies pré-apocalyptiques"
                ]
            }
        ];
                    document.addEventListener('DOMContentLoaded', function() {
    // Référence aux conteneurs de cartes
    const caligaMap = document.getElementById('caliga-map');
    const wastelandsMap = document.getElementById('wastelands-map');
    const zoneInfo = document.getElementById('zone-info');
    
    // Référence aux boutons de sélection de carte
    const mapButtons = document.querySelectorAll('.map-button');
    
    // Fonction pour créer les zones cliquables sur une carte
    function createMapAreas(mapContainer, zones) {
        // Récupérer les dimensions de l'image de la carte
        const mapImage = mapContainer.querySelector('.map-image');
        
        // Créer les zones cliquables
        zones.forEach(zone => {
            const [x1, y1, x2, y2] = zone.coords.split(',').map(Number);
            
            const area = document.createElement('div');
            area.className = 'map-area';
            area.setAttribute('data-id', zone.id);
            area.setAttribute('data-title', zone.title);
            area.style.left = Math.min(x1, x2) + 'px';
            area.style.top = Math.min(y1, y2) + 'px';
            area.style.width = Math.abs(x2 - x1) + 'px';
            area.style.height = Math.abs(y2 - y1) + 'px';
            
            // Ajouter les événements de survol et de clic
            area.addEventListener('click', function() {
                // Retirer la classe active de toutes les zones
                document.querySelectorAll('.map-area').forEach(a => a.classList.remove('active'));
                
                // Ajouter la classe active à la zone cliquée
                this.classList.add('active');
                
                // Afficher les informations de la zone
                displayZoneInfo(zone);
            });
            
            mapContainer.appendChild(area);
        });
    }
    
    // Fonction pour afficher les informations d'une zone
    function displayZoneInfo(zone) {
        // Associer chaque type de zone à une page spécifique
        let pageLink = "";
        if (zone.id.startsWith("O")) pageLink = "outzone_fr.html";
        else if (zone.id.startsWith("V")) pageLink = "viarosso_fr.html";
        else if (zone.id.startsWith("PP")) pageLink = "pepperpark_fr.html";
        else if (zone.id.startsWith("P")) pageLink = "plaza_fr.html";
    
        // Vérifier si la zone doit avoir un lien
        const isLinked = pageLink !== "";
    
        zoneInfo.innerHTML = `
            <span class="close-btn" id="close-info">&times;</span>
            <h3 class="zone-title">
                ${isLinked ? `<a href="${pageLink}" target="_blank">${zone.title}</a>` : zone.title}
            </h3>
            <p class="zone-description">${zone.description}</p>
            <h4 class="activities-title">Activités disponibles</h4>
            <ul class="activities-list">
                ${zone.activities.map(activity => `<li>${activity}</li>`).join('')}
            </ul>
        `;
    
        // Réattacher l'event listener après mise à jour du HTML
        document.getElementById('close-info').addEventListener('click', function() {
            zoneInfo.style.display = 'none';
        });
    
        // Afficher la boîte d'infos
        zoneInfo.style.display = 'block';
    }
    
    
    
    // Fonction pour changer de carte
    function switchMap(mapId) {
        // Cacher toutes les cartes
        caligaMap.style.display = 'none';
        wastelandsMap.style.display = 'none';
        
        // Afficher la carte sélectionnée
        document.getElementById(mapId + '-map').style.display = 'block';
        
        // Réinitialiser les informations de zone
        zoneInfo.innerHTML = `
            <h3 class="zone-title">Sélectionnez une zone</h3>
            <p class="zone-description">Cliquez sur une zone de la carte pour afficher ses informations.</p>
        `;
        
        // Mettre à jour les boutons
        mapButtons.forEach(button => {
            button.classList.remove('active');
            if (button.dataset.map === mapId) {
                button.classList.add('active');
            }
        });
    }
    
    // Ajouter les événements aux boutons de sélection de carte
    mapButtons.forEach(button => {
        button.addEventListener('click', function() {
            switchMap(this.dataset.map);
        });
    });
    
    // Créer les zones cliquables pour chaque carte
    createMapAreas(caligaMap, caligaZones);
    createMapAreas(wastelandsMap, wastelandsZones);
    
    // Correction des positions des zones pour les adapter à la taille réelle des images
    function adjustAreaPositions() {
        const maps = [
            { container: caligaMap, originalWidth: 1790, originalHeight: 2200 },
            { container: wastelandsMap, originalWidth: 1620, originalHeight: 1200 }
        ];
        
        maps.forEach(map => {
            const mapImage = map.container.querySelector('.map-image');
            const mapAreas = map.container.querySelectorAll('.map-area');
            
            // Obtenir les dimensions actuelles de l'image
            const actualWidth = mapImage.clientWidth;
            const actualHeight = mapImage.clientHeight;
            
            // Calculer les ratios d'échelle
            const widthRatio = actualWidth / map.originalWidth;
            const heightRatio = actualHeight / map.originalHeight;
            
            // Ajuster les positions et dimensions des zones
            mapAreas.forEach(area => {
                const originalLeft = parseInt(area.style.left);
                const originalTop = parseInt(area.style.top);
                const originalWidth = parseInt(area.style.width);
                const originalHeight = parseInt(area.style.height);
                
                area.style.left = (originalLeft * widthRatio) + 'px';
                area.style.top = (originalTop * heightRatio) + 'px';
                area.style.width = (originalWidth * widthRatio) + 'px';
                area.style.height = (originalHeight * heightRatio) + 'px';
            });
        });
    }
    
    // Ajuster les positions lors du chargement et du redimensionnement
    window.addEventListener('load', adjustAreaPositions);
    window.addEventListener('resize', adjustAreaPositions);
    
    // Afficher la carte de Caliga par défaut
    switchMap('caliga');
});
document.addEventListener('DOMContentLoaded', function() {
    const closeButton = document.getElementById('close-info');
    const zoneInfo = document.getElementById('zone-info');

    // Fermer la boîte d'information au clic sur la croix
    closeButton.addEventListener('click', function() {
        zoneInfo.style.display = 'none';
    });

    // Réafficher la boîte quand une zone est cliquée
    function displayZoneInfo(zone) {
        zoneInfo.innerHTML = `
            <span class="close-btn" id="close-info">&times;</span>
            <h3 class="zone-title">${zone.title}</h3>
            <p class="zone-description">${zone.description}</p>
            <h4 class="activities-title">Lieux notables</h4>
            <ul class="activities-list">
                ${zone.activities.map(activity => `<li>${activity}</li>`).join('')}
            </ul>
        `;
        
        // Réattacher l'event listener après mise à jour du HTML
        document.getElementById('close-info').addEventListener('click', function() {
            zoneInfo.style.display = 'none';
        });

        // Afficher la boîte d'infos
        zoneInfo.style.display = 'block';
    }
});