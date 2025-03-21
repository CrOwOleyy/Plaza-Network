        // Définition des zones pour chaque carte
        const caligaZones = [
            {   
                id: "O1",
                title: "Outzone 1",
                coords: "1024,256,776,1",
                description: "Une zone frontalière du nord-est de Neocron, Outzone 1 est connue pour ses grands espaces ouverts et ses routes commerciales. C'est une région relativement sûre comparée aux autres Outzones.",
                activities: [
                    "Missions de reconnaissance pour le CopCorps",
                    "Chasse aux mutants de faible niveau",
                    "Commerce avec les avant-postes",
                    "Exploration des bunkers abandonnés"
                ]
            },
            {
                id: "O2",
                title: "Outzone 2",
                coords: "510,254,776,1",
                description: "Située au nord de la ville, Outzone 2 est une zone intermédiaire comportant des installations militaires et des sites d'extraction de ressources abandonnés. La contamination y est plus élevée que dans O1.",
                activities: [
                    "Récupération de technologies anciennes",
                    "Affrontements avec des groupes de bandits",
                    "Missions d'exploration pour les Runners",
                    "Collecte de ressources rares"
                ]
            },
            {
                id: "O3",
                title: "Outzone 3",
                coords: "254,767,510,1026",
                description: "Une région dangereuse au sud-ouest, Outzone 3 abrite des ruines irradiées et des groupes de mutants hostiles. Peu de gens s'y aventurent sans protection adéquate.",
                activities: [
                    "Missions à haut risque pour les mercenaires",
                    "Chasse aux créatures mutantes puissantes",
                    "Recherche de matériaux radioactifs",
                    "Exploration des complexes souterrains"
                ]
            },
            {
                id: "O4",
                title: "Outzone 4",
                coords: "510,255,256,0",
                description: "Zone nord-ouest, Outzone 4 est réputée pour ses anciens laboratoires et centres de recherche datant d'avant la guerre. La zone attire scientifiques et pilleurs de l'ère technologique.",
                activities: [
                    "Récupération de données scientifiques",
                    "Neutralisation de systèmes de défense autonomes",
                    "Expéditions pour les Éclaireurs de Terra",
                    "Affrontements avec des groupes rivaux"
                ]
            },
            {
                id: "O5",
                title: "Outzone 5",
                coords: "254,258,0,0",
                description: "La zone la plus occidentale et l'une des plus isolées, Outzone 5 est connue pour ses conditions climatiques extrêmes et ses terrains difficiles. Peu de structures y subsistent.",
                activities: [
                    "Tests de survie en environnement hostile",
                    "Chasse de créatures rares",
                    "Extraction de minéraux précieux",
                    "Études des anomalies atmosphériques"
                ]
            },
            {
                id: "O6",
                title: "Outzone 6",
                coords: "256,255,510,513",
                description: "Une région de transition entre plusieurs zones, Outzone 6 est caractérisée par ses larges canyons et ses formations rocheuses. Des groupes nomades y ont établi des campements temporaires.",
                activities: [
                    "Négociations avec les tribus nomades",
                    "Protection des caravanes commerciales",
                    "Prospection de ressources naturelles",
                    "Reconnaissance pour les factions de la ville"
                ]
            },
            {
                id: "O7",
                title: "Outzone 7",
                coords: "510,767,256,512",
                description: "Au centre-ouest de la carte, Outzone 7 abrite d'anciennes installations civiles et des quartiers résidentiels en ruines. La zone est disputée entre plusieurs factions.",
                activities: [
                    "Récupération d'objets personnels d'avant-guerre",
                    "Médiation entre groupes rivaux",
                    "Missions de sabotage",
                    "Exploration urbaine des ruines"
                ]
            },
            {
                id: "O8",
                title: "Outzone 8",
                coords: "1535,514,1280,767",
                description: "À l'est de Neocron, Outzone 8 est une région montagneuse avec des vallées encaissées. D'anciennes installations minières y sont encore partiellement fonctionnelles.",
                activities: [
                    "Exploitation des ressources minières",
                    "Confrontations avec les systèmes de sécurité automatisés",
                    "Missions de sabotage industriel",
                    "Recherche d'anciennes technologies d'extraction"
                ]
            },
            {
                id: "O9",
                title: "Outzone 9",
                coords: "766,513,1021,769",
                description: "Zone centrale proche de la ville, Outzone 9 est relativement sécurisée et sert de point de transit pour les voyageurs. On y trouve quelques installations commerciales.",
                activities: [
                    "Échanges commerciaux sécurisés",
                    "Recrutement de mercenaires",
                    "Missions de livraison",
                    "Surveillance des activités suspectes"
                ]
            },
            {
                id: "S1",
                title: "Secret Passage 1",
                coords: "1026,512,1279,768",
                description: "Premier secteur de la ville de Neocron, S1 est un quartier résidentiel de classe moyenne avec des infrastructures bien entretenues. La sécurité y est assurée par le CopCorps.",
                activities: [
                    "Missions pour les corporations locales",
                    "Transactions légales sur le marché",
                    "Rencontres avec des informateurs",
                    "Participation aux événements sociaux"
                ]
            },
            {
                id: "S2",
                title: "Secret Passage 2",
                coords: "1280,766,1535,1026",
                description: "Deuxième secteur urbain, S2 est connu pour ses établissements de divertissement et ses zones commerciales animées. C'est un centre culturel important de Neocron.",
                activities: [
                    "Participation aux tournois virtuels",
                    "Négociations avec les guildes marchandes",
                    "Collecte d'informations dans les bars",
                    "Achat d'équipements de qualité"
                ]
            },
            {
                id: "I1",
                title: "Industrial Sector 1",
                coords: "765,770,1021,1023",
                description: "Première zone de la ville intérieure, I1 abrite des bâtiments gouvernementaux et des sièges de corporations. L'architecture y est imposante et la sécurité renforcée.",
                activities: [
                    "Missions diplomatiques",
                    "Espionnage corporatif",
                    "Réunions avec des officiels",
                    "Participation aux enchères de technologie"
                ]
            },
            {
                id: "I2",
                title: "Industial Sector 2",
                coords: "510,767,765,1023",
                description: "Deuxième zone de la ville intérieure, I2 est le centre technologique de Neocron avec ses laboratoires et centres de recherche avancés. L'accès y est strictement contrôlé.",
                activities: [
                    "Collaboration sur des projets scientifiques",
                    "Vol de prototypes expérimentaux",
                    "Recrutement de spécialistes",
                    "Tests de nouvelles technologies"
                ]
            },
            {
                id: "Pepper Park 1",
                title: "Plaza 1",
                coords: "766,1279,1023,1537",
                description: "Première section de la Plaza, PP1 est une zone commerciale animée avec de nombreuses boutiques et services. C'est un point de rencontre populaire pour les habitants.",
                activities: [
                    "Shopping de haute technologie",
                    "Échanges sur le marché noir",
                    "Recrutement pour missions privées",
                    "Participation aux événements publics"
                ]
            },
            {
                id: "PP2",
                title: "Pepper Park 2",
                coords: "766,1024,1021,1279",
                description: "Deuxième section de la Plaza, PP2 est connue pour ses centres médicaux et ses installations de modification corporelle. Les meilleurs médecins de la ville y exercent.",
                activities: [
                    "Achat d'implants cybernétiques",
                    "Missions pour les corporations médicales",
                    "Transactions de substances contrôlées",
                    "Recherche de traitements expérimentaux"
                ]
            },
            {
                id: "PP3",
                title: "Pepper Park 3",
                coords: "1277,1025,1021,1281",
                description: "Troisième section de la Plaza, PP3 abrite le quartier des divertissements avec ses bars, clubs et casinos. L'atmosphère y est électrique, surtout la nuit.",
                activities: [
                    "Jeux d'argent dans les casinos",
                    "Rencontres avec des fixers",
                    "Écoute des rumeurs locales",
                    "Participation aux compétitions clandestines"
                ]
            },
            {
                id: "P1",
                title: "Plaza 1",
                coords: "1532,1378,1790,1633",
                description: "Première section de Pepper Park, quartier rouge de Neocron, P1 est réputée pour ses établissements de plaisir et son ambiance sulfureuse. La criminalité y est élevée.",
                activities: [
                    "Négociations avec les syndicats criminels",
                    "Protection des établissements",
                    "Collecte de dettes impayées",
                    "Recherche de personnes disparues"
                ]
            },
            {
                id: "P2",
                title: "Plaza 2",
                coords: "1279,1379,1532,1633",
                description: "Deuxième section de Pepper Park, P2 est une zone où se mêlent petits commerces et activités illégales. C'est un territoire disputé entre plusieurs gangs.",
                activities: [
                    "Arbitrage de conflits territoriaux",
                    "Achat d'informations sensibles",
                    "Missions d'infiltration",
                    "Récupération d'objets volés"
                ]
            },
            {
                id: "P3",
                title: "Plaza 3",
                coords: "1021,1379,1277,1633",
                description: "Troisième section de Pepper Park, P3 est moins développée que les autres zones du quartier. On y trouve des entrepôts et des logements précaires.",
                activities: [
                    "Stockage de marchandises illicites",
                    "Recrutement de main-d'œuvre",
                    "Missions de contrebande",
                    "Recherche d'abris temporaires"
                ]
            },
            {
                id: "P4",
                title: "Plaza 4",
                coords: "1535,1665,1790,1919",
                description: "Quatrième section de Pepper Park, P4 est la zone la plus dangereuse du quartier avec une forte présence criminelle. Seuls les plus téméraires s'y aventurent la nuit.",
                activities: [
                    "Affrontements avec les gangs locaux",
                    "Récupération d'objets de valeur",
                    "Sauvetage d'otages",
                    "Sabotage des opérations rivales"
                ]
            },
            {
                id: "V1",
                title: "Via Rosso 1",
                coords: "1279,1920,1535,2176",
                description: "Première section de Via Rosso, V1 est un quartier industriel avec de nombreuses usines et centres de production. L'air y est pollué mais les opportunités nombreuses.",
                activities: [
                    "Sabotage industriel",
                    "Missions syndicales",
                    "Détournement de ressources",
                    "Infiltration des systèmes de sécurité"
                ]
            },
            {
                id: "V2",
                title: "Via Rosso 2",
                coords: "1279,1665,1535,1919",
                description: "Deuxième section de Via Rosso, V2 abrite des installations de recyclage et des centres de traitement des déchets. Les conditions de vie y sont difficiles.",
                activities: [
                    "Récupération de matériaux dangereux",
                    "Missions environnementales",
                    "Recherche de technologies abandonnées",
                    "Organisation de la résistance ouvrière"
                ]
            },
            {
                id: "V3",
                title: "Via Rosso 3",
                coords: "1021,1921,1279,2176",
                description: "Troisième section de Via Rosso, V3 est la zone la plus pauvre de Neocron. Ses habitants luttent quotidiennement pour survivre dans cet environnement hostile.",
                activities: [
                    "Distribution d'aide humanitaire",
                    "Protection des communautés locales",
                    "Chasse aux trafiquants d'organes",
                    "Organisation de réseaux d'entraide"
                ]
            }
        ];

        const yorkZones = [
            {
                id: "Y1",
                title: "Secteur Principal",
                coords: "300,300,500,500",
                description: "Le cœur du Dôme de York, ce secteur abrite les principales installations administratives et le centre de contrôle environnemental qui maintient l'habitabilité du dôme.",
                activities: [
                    "Missions diplomatiques pour les factions",
                    "Maintenance des systèmes de survie",
                    "Négociations commerciales",
                    "Collecte de données historiques"
                ]
            },
            {
                id: "Y2",
                title: "Quartier Résidentiel",
                coords: "510,300,700,500",
                description: "Zone d'habitation principale du Dôme de York, ce quartier est organisé en grands complexes d'appartements avec des espaces communs aménagés.",
                activities: [
                    "Résolution de conflits entre résidents",
                    "Réparation des systèmes de vie",
                    "Organisation d'événements communautaires",
                    "Surveillance des activités suspectes"
                ]
            },
            {
                id: "Y3",
                title: "Centre Scientifique",
                coords: "300,510,500,700",
                description: "Complexe de recherche avancée où sont menées des études sur l'adaptation humaine et la terraformation. Plusieurs laboratoires secrets y sont dissimulés.",
                activities: [
                    "Participation aux expériences scientifiques",
                    "Vol de données de recherche",
                    "Sabotage de projets controversés",
                    "Recrutement de cerveaux brillants"
                ]
            },
            {
                id: "Y4",
                title: "Jardin Hydroponique",
                coords: "510,510,700,700",
                description: "Vaste complexe agricole utilisant des technologies hydroponiques avancées pour nourrir la population du dôme. Une merveille de biotechnologie.",
                activities: [
                    "Maintenance des systèmes d'irrigation",
                    "Protection contre les saboteurs",
                    "Développement de nouvelles cultures",
                    "Distribution de nourriture"
                ]
            }
        ];

        const wastelandsZones = [
            {
                id: "W1",
                title: "Terres Désolées du Nord",
                coords: "300,100,700,300",
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
                coords: "500,300,900,500",
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
    const yorkMap = document.getElementById('york-map');
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
        if (zone.id.startsWith("O")) pageLink = "outzone.html";
        else if (zone.id.startsWith("V")) pageLink = "viarosso.html";
        else if (zone.id.startsWith("PP")) pageLink = "pepperpark.html";
        else if (zone.id.startsWith("P")) pageLink = "plaza.html";
    
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
        yorkMap.style.display = 'none';
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
    createMapAreas(yorkMap, yorkZones);
    createMapAreas(wastelandsMap, wastelandsZones);
    
    // Correction des positions des zones pour les adapter à la taille réelle des images
    function adjustAreaPositions() {
        const maps = [
            { container: caligaMap, originalWidth: 1790, originalHeight: 2200 },
            { container: yorkMap, originalWidth: 1024, originalHeight: 1024 },
            { container: wastelandsMap, originalWidth: 1024, originalHeight: 1024 }
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