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
            // Principales villes et installations (rectangles spéciaux)
            {
                id: "military-base",
                title: "Military Base",
                coords: "76,296,247,329",
                description: "Base militaire abandonnée de l'ancienne guerre. Cette installation fortifiée contient encore du matériel militaire et des véhicules blindés, mais est maintenant infestée de créatures mutantes.",
                activities: [
                    "Récupération d'équipement militaire",
                    "Exploration de bunkers souterrains",
                    "Combat contre des mutants",
                    "Recherche d'armes lourdes"
                ]
            },
            {
                id: "tech",
                title: "Tech",
                coords: "611,671,752,699",
                description: "Complexe technologique avancé spécialisé dans la recherche cybernétique. Centre névralgique pour l'upgrade d'implants et la recherche en nanotechnologie.",
                activities: [
                    "Upgrade d'implants cybernétiques",
                    "Recherche technologique",
                    "Commerce d'équipements high-tech",
                    "Laboratoires de nanotechnologie"
                ]
            },
            {
                id: "canyon",
                title: "Canyon",
                coords: "1143,731,1384,761",
                description: "Formation rocheuse naturelle qui offre un passage stratégique à travers les wastelands. Le canyon abrite plusieurs grottes et passages secrets utilisés par les contrebandiers.",
                activities: [
                    "Exploration de grottes",
                    "Routes de contrebande",
                    "Points d'observation stratégiques",
                    "Chasse aux créatures des cavernes"
                ]
            },

            // Polygones complexes avec SVG
            {
                id: "neocron-poly",
                title: "Neocron",
                coords: "592,1139,584,1136,585,1116,596,1103,636,1102,660,1120,711,1124,714,1112,697,1093,694,1075,700,1068,724,1068,751,1096,779,1096,783,1120,806,1147,577,1151",
                type: "polygon",
                description: "La grande mégapole de Neocron, centre de la civilisation post-apocalyptique. Cette vaste cité dome abrite des millions d'habitants et constitue le cœur économique et politique de la région.",
                activities: [
                    "Hub commercial principal",
                    "Quartiers résidentiels",
                    "Centres administratifs",
                    "Points d'accès aux wastelands"
                ]
            },
            {
                id: "york",
                title: "York",
                coords: "896,82,893,134,918,157,959,158,973,171,989,175,989,155,1044,155,1067,131,1106,131,1106,155,1123,169,1135,171,1137,189,1173,155,1211,153,1228,168,1239,168,1242,191,1251,201,1258,195,1256,182,1267,169,1287,171,1301,157,1393,157,1416,178,1423,160,1455,127,1457,85",
                type: "polygon",
                description: "Ancienne ville industrielle transformée en camp militaire. York sert de base d'opérations pour les expéditions dans les territoires les plus dangereux des wastelands.",
                activities: [
                    "Recrutement militaire",
                    "Formation de mercenaires",
                    "Missions d'escorte",
                    "Préparation d'expéditions"
                ]
            },

            
            // Ligne A (A06-A11) - Zones sud autour de Neocron
            {
                id: "A06",
                title: "Zone A06",
                coords: "490,1037,575,1131",
                description: "Zone de wilderness au sud-ouest de Neocron. Terrain accidenté avec des ruines éparses et des créatures mutantes.",
                activities: [
                    "Exploration de ruines",
                    "Chasse aux mutants",
                    "Récupération de matériaux",
                    "Missions de reconnaissance"
                ]
            },
            {
                id: "A07",
                title: "Zone A07",
                coords: "576,1037,666,1129",
                description: "Zone adjacente à Neocron, point de sortie principal vers les wastelands. Zone de transition entre la ville et les terres sauvages.",
                activities: [
                    "Point de sortie de Neocron",
                    "Contrôles de sécurité",
                    "Premières missions dans les wastelands",
                    "Commerce de base"
                ]
            },
            {
                id: "A08",
                title: "Zone A08",
                coords: "664,1038,751,1130",
                description: "Zone incluant une partie de Neocron et ses banlieues industrielles. Mélange d'installations urbaines et de zones abandonnées.",
                activities: [
                    "Banlieues industrielles",
                    "Installations abandonnées",
                    "Commerce périurbain",
                    "Zones résidentielles dégradées"
                ]
            },
            {
                id: "A09",
                title: "Zone A09",
                coords: "751,1038,839,1131",
                description: "Zone est de Neocron avec des installations de recherche et des laboratoires en périphérie de la ville.",
                activities: [
                    "Laboratoires périphériques",
                    "Installations de recherche",
                    "Zones d'expérimentation",
                    "Commerce scientifique"
                ]
            },
            {
                id: "A10",
                title: "Zone A10",
                coords: "840,1037,924,1129",
                description: "Zone de plaines arides à l'est de Neocron. Terrain ouvert avec quelques avant-postes isolés.",
                activities: [
                    "Patrouilles dans les plaines",
                    "Avant-postes isolés",
                    "Surveillance territoriale",
                    "Missions d'escorte"
                ]
            },
            {
                id: "A11",
                title: "Zone A11",
                coords: "926,1036,1015,1128",
                description: "Zone de collines rocheuses avec des mines abandonnées et des grottes naturelles.",
                activities: [
                    "Exploration de mines abandonnées",
                    "Spéléologie",
                    "Extraction de minerais",
                    "Refuge dans les grottes"
                ]
            },

            // Ligne B (B06-B11) - Zones centrales
            {
                id: "B06",
                title: "Zone B06",
                coords: "489,948,575,1036",
                description: "Zone de forêts contaminées au sud de Neocron. Végétation mutante et faune agressive.",
                activities: [
                    "Exploration de forêts mutantes",
                    "Collecte de spécimens biologiques",
                    "Chasse aux créatures des bois",
                    "Recherche botanique"
                ]
            },
            {
                id: "B07",
                title: "Zone B07",
                coords: "575,948,663,1036",
                description: "Zone de transition entre les forêts et les plaines, proche de Neocron. Mélange d'écosystèmes variés.",
                activities: [
                    "Études écologiques",
                    "Missions de transition",
                    "Surveillance environnementale",
                    "Points d'observation"
                ]
            },
            {
                id: "B08",
                title: "Zone B08",
                coords: "664,950,749,1036",
                description: "Zone contenant plusieurs villages et installations civiles. Centre d'activité pour les habitants des wastelands.",
                activities: [
                    "Commerce avec les villages",
                    "Services aux civils",
                    "Missions communautaires",
                    "Centres d'approvisionnement"
                ]
            },
            {
                id: "B09",
                title: "Zone B09",
                coords: "749,950,838,1036",
                description: "Zone industrielle avec plusieurs usines et centres de production. Activité économique importante.",
                activities: [
                    "Production industrielle",
                    "Commerce d'équipements",
                    "Maintenance d'installations",
                    "Transport de marchandises"
                ]
            },
            {
                id: "B10",
                title: "Zone B10",
                coords: "837,950,924,1036",
                description: "Zone de plateaux avec vue panoramique sur les wastelands. Position stratégique pour la surveillance.",
                activities: [
                    "Surveillance stratégique",
                    "Postes d'observation",
                    "Communications longue distance",
                    "Navigation"
                ]
            },
            {
                id: "B11",
                title: "Zone B11",
                coords: "924,949,1012,1036",
                description: "Zone de canyons et de formations rocheuses. Terrain difficile mais riche en ressources minérales.",
                activities: [
                    "Exploration de canyons",
                    "Extraction minière",
                    "Escalade et alpinisme",
                    "Géologie appliquée"
                ]
            },

            // Ligne C (C06-C12) - Zones commerciales et énergétiques
            {
                id: "C06",
                title: "Zone C06",
                coords: "489,862,577,947",
                description: "Zone de marécages toxiques avec une faune aquatique mutante. Environnement dangereux mais riche en ressources rares.",
                activities: [
                    "Exploration de marécages",
                    "Pêche en eaux contaminées",
                    "Collecte de plantes aquatiques",
                    "Recherche en biotoxicologie"
                ]
            },
            {
                id: "C07",
                title: "Zone C07",
                coords: "577,861,661,947",
                description: "Zone agricole expérimentale où les survivants tentent de cultiver dans un environnement post-apocalyptique.",
                activities: [
                    "Agriculture expérimentale",
                    "Recherche agronomique",
                    "Production alimentaire",
                    "Innovation agricole"
                ]
            },
            {
                id: "C08",
                title: "Zone C08",
                coords: "661,862,749,948",
                description: "Zone centrale de commerce et d'échange entre les différentes communautés des wastelands.",
                activities: [
                    "Marché central des wastelands",
                    "Échanges commerciaux",
                    "Négociations entre factions",
                    "Centre de commerce"
                ]
            },
            {
                id: "C09",
                title: "Zone C09",
                coords: "749,861,837,948",
                description: "Zone de production énergétique avec des installations solaires et éoliennes. Source d'énergie pour les wastelands.",
                activities: [
                    "Production d'énergie renouvelable",
                    "Maintenance énergétique",
                    "Distribution électrique",
                    "Innovation énergétique"
                ]
            },
            {
                id: "C10",
                title: "Zone C10",
                coords: "837,862,923,948",
                description: "Zone de stockage et de logistique pour l'approvisionnement des communautés isolées.",
                activities: [
                    "Stockage de marchandises",
                    "Logistique d'approvisionnement",
                    "Transport de fret",
                    "Gestion des inventaires"
                ]
            },
            {
                id: "C11",
                title: "Zone C11",
                coords: "924,862,1012,948",
                description: "Zone de formation et d'entraînement pour les explorateurs et mercenaires des wastelands.",
                activities: [
                    "Centre d'entraînement",
                    "Formation aux wastelands",
                    "École de survie",
                    "Préparation d'expéditions"
                ]
            },
            {
                id: "C12",
                title: "Zone C12",
                coords: "1012,861,1105,948",
                description: "Zone de recherche minière avec plusieurs puits d'extraction et installations de traitement.",
                activities: [
                    "Recherche géologique",
                    "Extraction minière",
                    "Traitement de minerais",
                    "Prospection"
                ]
            },

// Ligne D (D05-D13) - Zones archéologiques et minières
            {
                id: "D05",
                title: "Zone D05",
                coords: "401,773,489,861",
                description: "Zone de recherche archéologique avec des ruines d'une ancienne civilisation. Site de fouilles important.",
                activities: [
                    "Fouilles archéologiques",
                    "Recherche historique",
                    "Récupération d'artéfacts",
                    "Études culturelles"
                ]
            },
            {
                id: "D06",
                title: "Zone D06",
                coords: "489,775,574,864",
                description: "Zone de transition entre les marécages et les plaines, terrain mixte avec végétation diverse.",
                activities: [
                    "Études environnementales",
                    "Cartographie écologique",
                    "Missions d'exploration",
                    "Collecte de données"
                ]
            },
            {
                id: "D07",
                title: "Zone D07",
                coords: "575,772,661,859",
                description: "Zone agricole développée avec des fermes hydroponiques et des centres de production alimentaire.",
                activities: [
                    "Agriculture hydroponique",
                    "Production alimentaire",
                    "Commerce agricole",
                    "Innovation alimentaire"
                ]
            },
            {
                id: "D08",
                title: "Zone D08",
                coords: "660,773,748,861",
                description: "Zone urbaine périphérique avec des quartiers résidentiels et des centres de services.",
                activities: [
                    "Services résidentiels",
                    "Commerce de proximité",
                    "Logements sociaux",
                    "Centres communautaires"
                ]
            },
            {
                id: "D09",
                title: "Zone D09",
                coords: "749,775,833,861",
                description: "Zone industrielle spécialisée dans le traitement des déchets et le recyclage des matériaux.",
                activities: [
                    "Traitement des déchets",
                    "Recyclage de matériaux",
                    "Gestion environnementale",
                    "Innovation verte"
                ]
            },
            {
                id: "D10",
                title: "Zone D10",
                coords: "831,775,923,862",
                description: "Zone de transport et de logistique avec des centres de distribution et des entrepôts.",
                activities: [
                    "Centres de distribution",
                    "Transport de marchandises",
                    "Logistique avancée",
                    "Gestion d'entrepôts"
                ]
            },
            {
                id: "D11",
                title: "Zone D11",
                coords: "924,773,1011,861",
                description: "Zone militaire avec des installations d'entraînement et des casernes pour les forces de sécurité.",
                activities: [
                    "Entraînement militaire",
                    "Casernes de sécurité",
                    "Formation tactique",
                    "Opérations spéciales"
                ]
            },
            {
                id: "D12",
                title: "Zone D12",
                coords: "1012,775,1105,859",
                description: "Zone de recherche géologique avec des laboratoires d'analyse et des centres d'étude des sols.",
                activities: [
                    "Recherche géologique",
                    "Analyse des sols",
                    "Prospection minière",
                    "Études sismiques"
                ]
            },
            {
                id: "D13",
                title: "Zone D13",
                coords: "1107,773,1192,861",
                description: "Zone de haute technologie avec des centres de recherche avancée et des installations expérimentales.",
                activities: [
                    "Recherche avancée",
                    "Technologies expérimentales",
                    "Innovation high-tech",
                    "Projets scientifiques"
                ]
            },

            // Ligne E (E03-E13) - Zones côtières et forestières
            {
                id: "E03",
                title: "Zone E03",
                coords: "226,686,312,773",
                description: "Zone côtière avec des installations portuaires abandonnées. Accès maritime vers d'autres régions.",
                activities: [
                    "Exploration maritime",
                    "Installations portuaires",
                    "Commerce maritime",
                    "Pêche en haute mer"
                ]
            },
            {
                id: "E05",
                title: "Zone E05",
                coords: "401,687,488,772",
                description: "Zone de transition entre la côte et l'intérieur des terres, terrain vallonné avec végétation dense.",
                activities: [
                    "Exploration terrestre",
                    "Cartographie topographique",
                    "Études botaniques",
                    "Missions de reconnaissance"
                ]
            },
            {
                id: "E06",
                title: "Zone E06",
                coords: "486,686,575,773",
                description: "Zone forestière dense avec une biodiversité remarquable et des écosystèmes préservés.",
                activities: [
                    "Conservation forestière",
                    "Recherche biologique",
                    "Écotourisme",
                    "Protection environnementale"
                ]
            },
            {
                id: "E07",
                title: "Zone E07",
                coords: "574,690,659,770",
                description: "Zone de plaines fertiles avec des installations agricoles et des centres de production.",
                activities: [
                    "Agriculture intensive",
                    "Production de masse",
                    "Innovation agricole",
                    "Distribution alimentaire"
                ]
            },
            {
                id: "E08",
                title: "Zone E08",
                coords: "749,773,660,688",
                description: "Zone mixte urbaine-rurale avec des petites villes et des communautés rurales.",
                activities: [
                    "Vie communautaire",
                    "Commerce local",
                    "Services ruraux",
                    "Agriculture familiale"
                ]
            },
            {
                id: "E09",
                title: "Zone E09",
                coords: "838,775,748,686",
                description: "Zone de collines avec des vignobles et des cultures spécialisées, production de produits de luxe.",
                activities: [
                    "Viticulture",
                    "Cultures spécialisées",
                    "Production de luxe",
                    "Commerce haut de gamme"
                ]
            },
            {
                id: "E10",
                title: "Zone E10",
                coords: "925,773,839,685",
                description: "Zone de montagnes basses avec des stations de surveillance et des postes d'observation.",
                activities: [
                    "Surveillance territoriale",
                    "Météorologie",
                    "Communications",
                    "Sécurité frontalière"
                ]
            },
            {
                id: "E11",
                title: "Zone E11",
                coords: "924,686,1015,773",
                description: "Zone de passages montagneux avec des routes commerciales et des centres de transit.",
                activities: [
                    "Routes commerciales",
                    "Transit de marchandises",
                    "Services aux voyageurs",
                    "Péages et contrôles"
                ]
            },
            {
                id: "E12",
                title: "Zone E12",
                coords: "1014,685,1103,774",
                description: "Zone de hauts plateaux avec des installations de recherche atmosphérique et météorologique.",
                activities: [
                    "Recherche atmosphérique",
                    "Stations météo",
                    "Études climatiques",
                    "Prévisions long terme"
                ]
            },
            {
                id: "E13",
                title: "Zone E13",
                coords: "1104,684,1192,772",
                description: "Zone de sommets avec des installations de communication satellite et des antennes relais.",
                activities: [
                    "Communications satellite",
                    "Télécommunications",
                    "Recherche spatiale",
                    "Navigation GPS"
                ]
            },

            // Ligne F (F02-F13) - Zones de forêts et plaines
            {
                id: "F02",
                title: "Zone F02",
                coords: "141,598,229,686",
                description: "Zone de forêts denses avec une biodiversité remarquable malgré la contamination. Refuge pour la faune mutante.",
                activities: [
                    "Observation de la faune",
                    "Collecte de spécimens",
                    "Recherche biologique",
                    "Conservation environnementale"
                ]
            },
            {
                id: "F03",
                title: "Zone F03",
                coords: "228,598,312,686",
                description: "Zone de transition forêt-prairie avec des écosystèmes mixtes et une faune diversifiée.",
                activities: [
                    "Études écologiques",
                    "Gestion des habitats",
                    "Recherche comportementale",
                    "Conservation de la biodiversité"
                ]
            },
            {
                id: "F04",
                title: "Zone F04",
                coords: "312,599,401,688",
                description: "Zone de prairies avec des troupeaux d'animaux domestiques et des fermes d'élevage.",
                activities: [
                    "Élevage d'animaux",
                    "Production laitière",
                    "Agriculture pastorale",
                    "Commerce d'animaux"
                ]
            },
            {
                id: "F05",
                title: "Zone F05",
                coords: "403,599,485,686",
                description: "Zone agricole mixte avec des cultures céréalières et des jardins potagers communautaires.",
                activities: [
                    "Cultures céréalières",
                    "Jardins communautaires",
                    "Production maraîchère",
                    "Coopératives agricoles"
                ]
            },
            {
                id: "F06",
                title: "Zone F06",
                coords: "485,598,577,684",
                description: "Zone de production alimentaire intensive avec des serres et des centres de transformation.",
                activities: [
                    "Production en serres",
                    "Transformation alimentaire",
                    "Conservation des aliments",
                    "Distribution régionale"
                ]
            },
            {
                id: "F07",
                title: "Zone F07",
                coords: "577,599,660,688",
                description: "Zone de petites industries agroalimentaires et de centres de traitement des produits agricoles.",
                activities: [
                    "Industries agroalimentaires",
                    "Traitement des produits",
                    "Conditionnement",
                    "Contrôle qualité"
                ]
            },
            {
                id: "F08",
                title: "Zone F08",
                coords: "663,599,747,680",
                description: "Zone commerciale agricole avec des marchés et des centres de distribution alimentaire.",
                activities: [
                    "Marchés agricoles",
                    "Distribution alimentaire",
                    "Commerce de gros",
                    "Négociation de prix"
                ]
            },
            {
                id: "F09",
                title: "Zone F09",
                coords: "748,598,837,684",
                description: "Zone de services agricoles avec des centres de formation et des instituts de recherche.",
                activities: [
                    "Formation agricole",
                    "Recherche agronomique",
                    "Conseil aux agriculteurs",
                    "Innovation technique"
                ]
            },
            {
                id: "F10",
                title: "Zone F10",
                coords: "835,599,923,684",
                description: "Zone de technologie agricole avec des centres de développement d'équipements agricoles.",
                activities: [
                    "Développement d'équipements",
                    "Technologie agricole",
                    "Mécanisation",
                    "Automatisation"
                ]
            },
            {
                id: "F11",
                title: "Zone F11",
                coords: "924,598,1015,684",
                description: "Zone de recherche biotechnologique appliquée à l'agriculture et à l'amélioration des cultures.",
                activities: [
                    "Recherche biotechnologique",
                    "Amélioration des cultures",
                    "Génétique végétale",
                    "Innovation biologique"
                ]
            },
            {
                id: "F12",
                title: "Zone F12",
                coords: "1013,597,1105,685",
                description: "Zone de centres d'excellence agricole et d'instituts de recherche avancée.",
                activities: [
                    "Centres d'excellence",
                    "Recherche avancée",
                    "Formation supérieure",
                    "Coopération internationale"
                ]
            },
            {
                id: "F13",
                title: "Zone F13",
                coords: "1105,598,1193,684",
                description: "Zone de production de semences et de centres de conservation génétique.",
                activities: [
                    "Production de semences",
                    "Conservation génétique",
                    "Banques de graines",
                    "Préservation de la biodiversité"
                ]
            },

            // Ligne G (G03-G13) - Zones de plaines fertiles
            {
                id: "G03",
                title: "Zone G03",
                coords: "226,512,312,596",
                description: "Zone de plaines fertiles où s'établissent les communautés agricoles. Production alimentaire pour les wastelands.",
                activities: [
                    "Agriculture intensive",
                    "Élevage d'animaux",
                    "Production alimentaire",
                    "Commerce agricole"
                ]
            },
            {
                id: "G04",
                title: "Zone G04",
                coords: "314,512,403,598",
                description: "Zone de fermes familiales avec des cultures traditionnelles et des méthodes de production durables.",
                activities: [
                    "Fermes familiales",
                    "Cultures traditionnelles",
                    "Agriculture durable",
                    "Transmission de savoir-faire"
                ]
            },
            {
                id: "G05",
                title: "Zone G05",
                coords: "401,510,488,599",
                description: "Zone de coopératives agricoles avec des installations communes et des programmes d'entraide.",
                activities: [
                    "Coopératives agricoles",
                    "Installations communes",
                    "Programmes d'entraide",
                    "Solidarité rurale"
                ]
            },
            {
                id: "G06",
                title: "Zone G06",
                coords: "488,510,578,598",
                description: "Zone de recherche agricole avec des stations expérimentales et des centres d'innovation.",
                activities: [
                    "Recherche agricole",
                    "Stations expérimentales",
                    "Innovation agricole",
                    "Tests de nouvelles variétés"
                ]
            },
            {
                id: "G07",
                title: "Zone G07",
                coords: "580,513,661,599",
                description: "Zone de production spécialisée avec des cultures de haute valeur et des produits d'exportation.",
                activities: [
                    "Production spécialisée",
                    "Cultures de haute valeur",
                    "Produits d'exportation",
                    "Commerce international"
                ]
            },
            {
                id: "G08",
                title: "Zone G08",
                coords: "660,513,752,601",
                description: "Zone de transformation agroalimentaire avec des usines de traitement et des centres de conditionnement.",
                activities: [
                    "Transformation agroalimentaire",
                    "Usines de traitement",
                    "Conditionnement",
                    "Chaîne du froid"
                ]
            },
            {
                id: "G09",
                title: "Zone G09",
                coords: "751,510,838,598",
                description: "Zone logistique agricole avec des centres de stockage et des plateformes de distribution.",
                activities: [
                    "Logistique agricole",
                    "Centres de stockage",
                    "Plateformes de distribution",
                    "Transport spécialisé"
                ]
            },
            {
                id: "G10",
                title: "Zone G10",
                coords: "838,510,926,598",
                description: "Zone de commerce agricole avec des bourses de marchandises et des centres de négociation.",
                activities: [
                    "Commerce agricole",
                    "Bourses de marchandises",
                    "Centres de négociation",
                    "Fixation des prix"
                ]
            },
            {
                id: "G11",
                title: "Zone G11",
                coords: "926,510,1016,598",
                description: "Zone de financement agricole avec des banques spécialisées et des organismes de crédit.",
                activities: [
                    "Financement agricole",
                    "Banques spécialisées",
                    "Organismes de crédit",
                    "Assurance agricole"
                ]
            },
            {
                id: "G12",
                title: "Zone G12",
                coords: "1015,510,1104,598",
                description: "Zone de formation agricole avec des écoles et des centres de perfectionnement professionnel.",
                activities: [
                    "Formation agricole",
                    "Écoles spécialisées",
                    "Perfectionnement professionnel",
                    "Certification"
                ]
            },
            {
                id: "G13",
                title: "Zone G13",
                coords: "1104,512,1192,598",
                description: "Zone de politique agricole avec des organismes gouvernementaux et des centres de décision.",
                activities: [
                    "Politique agricole",
                    "Organismes gouvernementaux",
                    "Centres de décision",
                    "Réglementation"
                ]
            },

            // Ligne H (H03-H16) - Zones de recherche et développement
            {
                id: "H03",
                title: "Zone H03",
                coords: "228,424,314,513",
                description: "Zone de recherche fondamentale avec des laboratoires universitaires et des centres de sciences pures.",
                activities: [
                    "Recherche fondamentale",
                    "Laboratoires universitaires",
                    "Sciences pures",
                    "Formation doctorale"
                ]
            },
            {
                id: "H04",
                title: "Zone H04",
                coords: "314,423,403,510",
                description: "Zone de développement technologique avec des incubateurs d'entreprises et des centres d'innovation.",
                activities: [
                    "Développement technologique",
                    "Incubateurs d'entreprises",
                    "Centres d'innovation",
                    "Start-ups technologiques"
                ]
            },
            {
                id: "H05",
                title: "Zone H05",
                coords: "403,424,488,510",
                description: "Zone de recherche appliquée avec des centres de R&D industriels et des laboratoires privés.",
                activities: [
                    "Recherche appliquée",
                    "R&D industriels",
                    "Laboratoires privés",
                    "Innovation produits"
                ]
            },
            {
                id: "H06",
                title: "Zone H06",
                coords: "488,424,577,509",
                description: "Zone de prototypage avec des ateliers de fabrication et des centres d'essais.",
                activities: [
                    "Prototypage",
                    "Ateliers de fabrication",
                    "Centres d'essais",
                    "Validation produits"
                ]
            },
            {
                id: "H07",
                title: "Zone H07",
                coords: "577,423,664,512",
                description: "Zone de production pilote avec des lignes de test et des installations d'évaluation.",
                activities: [
                    "Production pilote",
                    "Lignes de test",
                    "Installations d'évaluation",
                    "Optimisation processus"
                ]
            },
            {
                id: "H08",
                title: "Zone H08",
                coords: "664,423,752,512",
                description: "Zone de transfert technologique avec des centres de liaison université-industrie.",
                activities: [
                    "Transfert technologique",
                    "Liaison université-industrie",
                    "Commercialisation recherche",
                    "Partenariats publics-privés"
                ]
            },
            {
                id: "H09",
                title: "Zone H09",
                coords: "751,421,840,509",
                description: "Zone de propriété intellectuelle avec des offices de brevets et des centres juridiques.",
                activities: [
                    "Propriété intellectuelle",
                    "Offices de brevets",
                    "Centres juridiques",
                    "Protection innovations"
                ]
            },
            {
                id: "H10",
                title: "Zone H10",
                coords: "840,423,924,509",
                description: "Zone de normalisation avec des organismes de certification et des centres de standards.",
                activities: [
                    "Normalisation",
                    "Organismes de certification",
                    "Centres de standards",
                    "Contrôle qualité"
                ]
            },
            {
                id: "H11",
                title: "Zone H11",
                coords: "924,424,1015,509",
                description: "Zone de métrologie avec des laboratoires d'étalonnage et des centres de mesure.",
                activities: [
                    "Métrologie",
                    "Laboratoires d'étalonnage",
                    "Centres de mesure",
                    "Instruments de précision"
                ]
            },
            {
                id: "H12",
                title: "Zone H12",
                coords: "1012,423,1104,510",
                description: "Zone de veille technologique avec des centres d'information et des observatoires innovation.",
                activities: [
                    "Veille technologique",
                    "Centres d'information",
                    "Observatoires innovation",
                    "Prospective technologique"
                ]
            },
            {
                id: "H13",
                title: "Zone H13",
                coords: "1102,421,1190,510",
                description: "Zone de coopération internationale avec des centres de collaboration et des réseaux mondiaux.",
                activities: [
                    "Coopération internationale",
                    "Centres de collaboration",
                    "Réseaux mondiaux",
                    "Échanges scientifiques"
                ]
            },
            {
                id: "H14",
                title: "Zone H14",
                coords: "1190,421,1278,510",
                description: "Zone de prospective avec des centres d'études futures et des think tanks.",
                activities: [
                    "Prospective",
                    "Centres d'études futures",
                    "Think tanks",
                    "Analyse stratégique"
                ]
            },
            {
                id: "H15",
                title: "Zone H15",
                coords: "1276,421,1370,510",
                description: "Zone de politique scientifique avec des organismes gouvernementaux de recherche.",
                activities: [
                    "Politique scientifique",
                    "Organismes gouvernementaux",
                    "Stratégie recherche",
                    "Financement public"
                ]
            },
            {
                id: "H16",
                title: "Zone H16",
                coords: "1370,421,1456,512",
                description: "Zone de relations internationales scientifiques avec des ambassades de la science.",
                activities: [
                    "Relations internationales",
                    "Ambassades de la science",
                    "Diplomatie scientifique",
                    "Accords bilatéraux"
                ]
            },

            // Ligne I (I02-I16) - Zones de services et administration
            {
                id: "I02",
                title: "Zone I02",
                coords: "143,338,226,424",
                description: "Zone administrative locale avec des mairies et des services de proximité.",
                activities: [
                    "Administration locale",
                    "Services de proximité",
                    "État civil",
                    "Affaires locales"
                ]
            },
            {
                id: "I03",
                title: "Zone I03",
                coords: "225,336,314,423",
                description: "Zone de services sociaux avec des centres d'aide et des organismes caritatifs.",
                activities: [
                    "Services sociaux",
                    "Centres d'aide",
                    "Organismes caritatifs",
                    "Assistance sociale"
                ]
            },
            {
                id: "I04",
                title: "Zone I04",
                coords: "312,335,400,421",
                description: "Zone d'éducation avec des écoles et des centres de formation professionnelle.",
                activities: [
                    "Éducation primaire",
                    "Formation professionnelle",
                    "Centres de formation",
                    "Apprentissage"
                ]
            },
            {
                id: "I05",
                title: "Zone I05",
                coords: "401,335,489,423",
                description: "Zone de santé avec des hôpitaux et des centres médicaux spécialisés.",
                activities: [
                    "Soins médicaux",
                    "Hôpitaux",
                    "Centres spécialisés",
                    "Urgences médicales"
                ]
            },
            {
                id: "I06",
                title: "Zone I06",
                coords: "489,338,575,423",
                description: "Zone de justice avec des tribunaux et des centres juridiques.",
                activities: [
                    "Tribunaux",
                    "Centres juridiques",
                    "Services judiciaires",
                    "Médiation"
                ]
            },
            {
                id: "I07",
                title: "Zone I07",
                coords: "577,338,663,421",
                description: "Zone de sécurité avec des commissariats et des centres de surveillance.",
                activities: [
                    "Forces de l'ordre",
                    "Commissariats",
                    "Surveillance",
                    "Sécurité publique"
                ]
            },
            {
                id: "I08",
                title: "Zone I08",
                coords: "663,336,749,421",
                description: "Zone de transport avec des gares et des centres de logistique.",
                activities: [
                    "Transport public",
                    "Gares",
                    "Logistique",
                    "Mobilité urbaine"
                ]
            },
            {
                id: "I09",
                title: "Zone I09",
                coords: "751,338,838,420",
                description: "Zone de communication avec des centres postaux et des télécommunications.",
                activities: [
                    "Services postaux",
                    "Télécommunications",
                    "Communication",
                    "Réseaux"
                ]
            },
            {
                id: "I10",
                title: "Zone I10",
                coords: "840,334,924,421",
                description: "Zone financière avec des banques et des organismes de crédit.",
                activities: [
                    "Services bancaires",
                    "Organismes de crédit",
                    "Finance",
                    "Assurances"
                ]
            },
            {
                id: "I11",
                title: "Zone I11",
                coords: "924,336,1015,423",
                description: "Zone d'emploi avec des centres pour l'emploi et des agences de recrutement.",
                activities: [
                    "Centres pour l'emploi",
                    "Agences de recrutement",
                    "Formation professionnelle",
                    "Insertion professionnelle"
                ]
            },
            {
                id: "I12",
                title: "Zone I12",
                coords: "1013,335,1101,421",
                description: "Zone de culture avec des centres culturels et des bibliothèques.",
                activities: [
                    "Centres culturels",
                    "Bibliothèques",
                    "Activités culturelles",
                    "Patrimoine"
                ]
            },
            {
                id: "I13",
                title: "Zone I13",
                coords: "1102,336,1190,420",
                description: "Zone de sport avec des complexes sportifs et des centres de loisirs.",
                activities: [
                    "Complexes sportifs",
                    "Centres de loisirs",
                    "Sport",
                    "Bien-être"
                ]
            },
            {
                id: "I14",
                title: "Zone I14",
                coords: "1190,335,1278,420",
                description: "Zone de tourisme avec des offices de tourisme et des centres d'accueil.",
                activities: [
                    "Offices de tourisme",
                    "Centres d'accueil",
                    "Promotion touristique",
                    "Information visiteurs"
                ]
            },
            {
                id: "I15",
                title: "Zone I15",
                coords: "1275,335,1370,421",
                description: "Zone de commerce avec des centres commerciaux et des marchés.",
                activities: [
                    "Centres commerciaux",
                    "Marchés",
                    "Commerce de détail",
                    "Distribution"
                ]
            },
            {
                id: "I16",
                title: "Zone I16",
                coords: "1368,335,1454,420",
                description: "Zone d'innovation sociale avec des centres d'entrepreneuriat social.",
                activities: [
                    "Entrepreneuriat social",
                    "Innovation sociale",
                    "Économie solidaire",
                    "Développement durable"
                ]
            },

            // Ligne J (J01-J16) - Zones frontalières
            {
                id: "J01",
                title: "Zone J01",
                coords: "54,249,141,336",
                description: "Zone frontalière ouest des wastelands. Territoire sauvage avec peu d'installations humaines.",
                activities: [
                    "Exploration de territoires vierges",
                    "Missions de reconnaissance",
                    "Établissement d'avant-postes",
                    "Cartographie"
                ]
            },
            {
                id: "J02",
                title: "Zone J02",
                coords: "141,250,226,336",
                description: "Zone de contrôle frontalier avec des postes de douane et des points de passage.",
                activities: [
                    "Contrôle frontalier",
                    "Postes de douane",
                    "Points de passage",
                    "Sécurité des frontières"
                ]
            },
            {
                id: "J03",
                title: "Zone J03",
                coords: "226,249,312,335",
                description: "Zone de commerce transfrontalier avec des marchés et des centres d'échange.",
                activities: [
                    "Commerce transfrontalier",
                    "Marchés internationaux",
                    "Centres d'échange",
                    "Négociation commerciale"
                ]
            },
            {
                id: "J04",
                title: "Zone J04",
                coords: "314,249,400,336",
                description: "Zone de transit avec des centres logistiques et des plateformes de transport.",
                activities: [
                    "Centres logistiques",
                    "Plateformes de transport",
                    "Transit international",
                    "Gestion des flux"
                ]
            },
            {
                id: "J05",
                title: "Zone J05",
                coords: "400,247,488,334",
                description: "Zone de services aux voyageurs avec des hôtels et des centres de repos.",
                activities: [
                    "Services aux voyageurs",
                    "Hôtels",
                    "Centres de repos",
                    "Restauration"
                ]
            },
            {
                id: "J06",
                title: "Zone J06",
                coords: "488,247,577,336",
                description: "Zone de communication internationale avec des centres de liaison.",
                activities: [
                    "Communication internationale",
                    "Centres de liaison",
                    "Diplomatie",
                    "Relations extérieures"
                ]
            },
            {
                id: "J07",
                title: "Zone J07",
                coords: "577,247,663,336",
                description: "Zone de coopération internationale avec des organismes multinationaux.",
                activities: [
                    "Coopération internationale",
                    "Organismes multinationaux",
                    "Projets communs",
                    "Coordination régionale"
                ]
            },
            {
                id: "J08",
                title: "Zone J08",
                coords: "663,247,749,335",
                description: "Zone d'échanges culturels avec des centres culturels internationaux.",
                activities: [
                    "Échanges culturels",
                    "Centres culturels internationaux",
                    "Festivals",
                    "Promotion culturelle"
                ]
            },
            {
                id: "J09",
                title: "Zone J09",
                coords: "751,247,842,338",
                description: "Zone de recherche internationale avec des laboratoires collaboratifs.",
                activities: [
                    "Recherche internationale",
                    "Laboratoires collaboratifs",
                    "Projets scientifiques",
                    "Échanges chercheurs"
                ]
            },
            {
                id: "J10",
                title: "Zone J10",
                coords: "841,247,924,335",
                description: "Zone d'enseignement international avec des universités et des écoles.",
                activities: [
                    "Enseignement international",
                    "Universités",
                    "Écoles internationales",
                    "Mobilité étudiante"
                ]
            },
            {
                id: "J11",
                title: "Zone J11",
                coords: "923,249,1012,335",
                description: "Zone de formation internationale avec des centres de perfectionnement.",
                activities: [
                    "Formation internationale",
                    "Centres de perfectionnement",
                    "Certification internationale",
                    "Échanges professionnels"
                ]
            },
            {
                id: "J12",
                title: "Zone J12",
                coords: "1013,247,1105,334",
                description: "Zone de standards internationaux avec des organismes de normalisation.",
                activities: [
                    "Standards internationaux",
                    "Organismes de normalisation",
                    "Harmonisation",
                    "Certification"
                ]
            },
            {
                id: "J13",
                title: "Zone J13",
                coords: "1104,246,1192,336",
                description: "Zone de régulation internationale avec des autorités de contrôle.",
                activities: [
                    "Régulation internationale",
                    "Autorités de contrôle",
                    "Supervision",
                    "Conformité"
                ]
            },
            {
                id: "J14",
                title: "Zone J14",
                coords: "1193,247,1281,336",
                description: "Zone de médiation internationale avec des centres d'arbitrage.",
                activities: [
                    "Médiation internationale",
                    "Centres d'arbitrage",
                    "Résolution conflits",
                    "Justice internationale"
                ]
            },
            {
                id: "J15",
                title: "Zone J15",
                coords: "1276,247,1367,335",
                description: "Zone de paix et sécurité avec des forces de maintien de la paix.",
                activities: [
                    "Maintien de la paix",
                    "Forces internationales",
                    "Sécurité collective",
                    "Prévention conflits"
                ]
            },
            {
                id: "J16",
                title: "Zone J16",
                coords: "1367,249,1453,335",
                description: "Zone de développement international avec des organismes d'aide.",
                activities: [
                    "Développement international",
                    "Organismes d'aide",
                    "Coopération technique",
                    "Assistance humanitaire"
                ]
            },

            // Ligne K (K01-K16) - Zones nordiques
            {
                id: "K01",
                title: "Zone K01",
                coords: "143,161,55,247",
                description: "Zone arctique extrême avec des conditions climatiques difficiles et des avant-postes isolés.",
                activities: [
                    "Exploration arctique",
                    "Avant-postes isolés",
                    "Survie extrême",
                    "Recherche climatique"
                ]
            },
            {
                id: "K02",
                title: "Zone K02",
                coords: "228,161,141,249",
                description: "Zone de recherche polaire avec des stations scientifiques et des observatoires.",
                activities: [
                    "Recherche polaire",
                    "Stations scientifiques",
                    "Observatoires",
                    "Études glaciaires"
                ]
            },
            {
                id: "K03",
                title: "Zone K03",
                coords: "315,160,229,247",
                description: "Zone de météorologie polaire avec des centres de prévision climatique.",
                activities: [
                    "Météorologie polaire",
                    "Prévision climatique",
                    "Études atmosphériques",
                    "Surveillance climatique"
                ]
            },
            {
                id: "K04",
                title: "Zone K04",
                coords: "401,161,314,247",
                description: "Zone de géologie polaire avec des centres d'étude des formations glaciaires.",
                activities: [
                    "Géologie polaire",
                    "Formations glaciaires",
                    "Études sédimentaires",
                    "Paléoclimatologie"
                ]
            },
            {
                id: "K06",
                title: "Zone K06",
                coords: "577,163,489,246",
                description: "Zone de toundra nordique avec un climat rigoureux. Territoire de créatures adaptées au froid.",
                activities: [
                    "Survie en climat rigoureux",
                    "Chasse aux créatures arctiques",
                    "Exploration polaire",
                    "Recherche climatique"
                ]
            },
            {
                id: "K05",
                title: "Zone K05",
                coords: "489,161,400,246",
                description: "Zone de biologie polaire avec des centres d'étude de la faune arctique.",
                activities: [
                    "Biologie polaire",
                    "Faune arctique",
                    "Adaptation au froid",
                    "Écosystèmes polaires"
                ]
            },
            {
                id: "K07",
                title: "Zone K07",
                coords: "663,161,577,247",
                description: "Zone de passage nordique avec des routes de migration animale et des couloirs de déplacement.",
                activities: [
                    "Routes de migration",
                    "Couloirs de déplacement",
                    "Observation animale",
                    "Guidage territorial"
                ]
            },
            {
                id: "K08",
                title: "Zone K08",
                coords: "752,161,663,246",
                description: "Zone de ressources nordiques avec des gisements de minéraux rares et des sites d'extraction.",
                activities: [
                    "Extraction de minéraux rares",
                    "Prospection nordique",
                    "Exploitation minière",
                    "Commerce de ressources"
                ]
            },
            {
                id: "K09",
                title: "Zone K09",
                coords: "837,161,751,246",
                description: "Zone de communication nordique avec des relais et des stations de transmission longue distance.",
                activities: [
                    "Communications longue distance",
                    "Relais de transmission",
                    "Navigation polaire",
                    "Coordination nordique"
                ]
            },
            {
                id: "K10",
                title: "Zone K10",
                coords: "926,160,840,246",
                description: "Zone de logistique nordique avec des bases d'approvisionnement et des centres de distribution.",
                activities: [
                    "Bases d'approvisionnement",
                    "Distribution nordique",
                    "Logistique polaire",
                    "Ravitaillement"
                ]
            },
            {
                id: "K11",
                title: "Zone K11",
                coords: "1012,160,927,249",
                description: "Zone de défense nordique avec des installations militaires et des postes de surveillance.",
                activities: [
                    "Installations militaires",
                    "Surveillance nordique",
                    "Défense territoriale",
                    "Sécurité polaire"
                ]
            },
            {
                id: "K12",
                title: "Zone K12",
                coords: "1105,161,1011,247",
                description: "Zone de recherche énergétique avec des installations géothermiques et des centres d'énergie.",
                activities: [
                    "Installations géothermiques",
                    "Recherche énergétique",
                    "Énergie polaire",
                    "Sources d'énergie alternatives"
                ]
            },
            {
                id: "K13",
                title: "Zone K13",
                coords: "1193,163,1104,246",
                description: "Zone de technologie nordique avec des centres de développement d'équipements polaires.",
                activities: [
                    "Développement d'équipements polaires",
                    "Technologie nordique",
                    "Innovation polaire",
                    "Matériel spécialisé"
                ]
            },
            {
                id: "K14",
                title: "Zone K14",
                coords: "1279,163,1192,246",
                description: "Zone de coopération polaire avec des centres de coordination internationale.",
                activities: [
                    "Coopération polaire",
                    "Coordination internationale",
                    "Traités polaires",
                    "Gestion commune"
                ]
            },
            {
                id: "K15",
                title: "Zone K15",
                coords: "1364,161,1278,246",
                description: "Zone de préservation polaire avec des réserves naturelles et des zones protégées.",
                activities: [
                    "Réserves naturelles",
                    "Zones protégées",
                    "Conservation polaire",
                    "Protection environnementale"
                ]
            },
            {
                id: "K16",
                title: "Zone K16",
                coords: "1456,161,1363,247",
                description: "Zone d'urgence polaire avec des centres de secours et des équipes de sauvetage.",
                activities: [
                    "Centres de secours",
                    "Équipes de sauvetage",
                    "Urgences polaires",
                    "Assistance d'urgence"
                ]
            },

            // Points d'intérêt spéciaux (cercles) - comme dans le fichier original
            {
                id: "simmons-factory",
                title: "Simmons Factory",
                coords: "519,1088,12",
                description: "Ancienne usine de production d'équipements médicaux. Aujourd'hui partiellement automatisée, elle produit encore des fournitures médicales basiques.",
                activities: [
                    "Production de matériel médical",
                    "Récupération de machines",
                    "Maintenance automatisée",
                    "Commerce d'équipements"
                ]
            },
            {
                id: "point-red",
                title: "Point Red",
                coords: "619,1000,13",
                description: "Point de référence stratégique marqué par une tour de communication rouge. Utilisé pour la navigation et les communications.",
                activities: [
                    "Communications",
                    "Navigation",
                    "Point de rendez-vous",
                    "Surveillance"
                ]
            },
            {
                id: "jeriko-fortress",
                title: "Jeriko Fortress",
                coords: "700,989,15",
                description: "Forteresse militaire gardant les approches sud de Neocron. Base d'opérations pour les patrouilles des wastelands.",
                activities: [
                    "Patrouilles militaires",
                    "Sécurité des routes",
                    "Entraînement de soldats",
                    "Poste de commandement"
                ]
            },
            {
                id: "mutant-trap",
                title: "Mutant Trap",
                coords: "724,1010,13",
                description: "Zone piégée utilisée pour capturer des créatures mutantes vivantes. Installation de recherche biologique clandestine.",
                activities: [
                    "Capture de mutants",
                    "Recherche biologique",
                    "Étude comportementale",
                    "Commerce de spécimens"
                ]
            },
            {
                id: "sherman-bay",
                title: "Sherman Bay",
                coords: "876,1017,11",
                description: "Petite baie naturelle servant de port pour les bateaux de pêche et les navires de transport léger. Point de transit maritime.",
                activities: [
                    "Transport maritime",
                    "Pêche",
                    "Commerce côtier",
                    "Réparation navale"
                ]
            },
            {
                id: "mcpherson-factory",
                title: "McPherson Factory",
                coords: "981,1015,15",
                description: "Complexe industriel spécialisé dans la production de véhicules. L'usine fonctionne encore partiellement grâce à des systèmes automatisés.",
                activities: [
                    "Assemblage de véhicules",
                    "Réparation mécanique",
                    "Commerce de pièces détachées",
                    "Modification de véhicules"
                ]
            },
            {
                id: "tawkeen-village",
                title: "Tawkeen Village",
                coords: "553,902,13",
                description: "Petit village de survivants établi autour d'un puits d'eau pure. Les habitants vivent principalement de l'agriculture et du commerce avec les caravanes.",
                activities: [
                    "Commerce de vivres",
                    "Point de repos pour caravanes",
                    "Agriculture hydroponique",
                    "Marché local"
                ]
            },
            {
                id: "tyron-factory",
                title: "Tyron Factory",
                coords: "601,885,15",
                description: "Usine de production d'armes et d'équipements de combat. Contrôlée par une faction militaire qui en assure la sécurité.",
                activities: [
                    "Production d'armements",
                    "Modification d'armes",
                    "Entraînement au combat",
                    "Commerce militaire"
                ]
            },
            {
                id: "crest-village",
                title: "Crest Village",
                coords: "690,912,13",
                description: "Village fortifié construit sur une colline rocheuse. Réputé pour sa position défensive et ses guetteurs expérimentés.",
                activities: [
                    "Services de reconnaissance",
                    "Formation de scouts",
                    "Commerce d'armes légères",
                    "Point d'observation stratégique"
                ]
            },
            {
                id: "krupp-factory",
                title: "Krupp Factory",
                coords: "798,897,17",
                description: "Massive usine métallurgique qui transforme les minerais extraits des mines environnantes. Point central de l'industrie lourde des wastelands.",
                activities: [
                    "Traitement de minerais",
                    "Production métallurgique",
                    "Commerce de métaux",
                    "Forge avancée"
                ]
            },
            {
                id: "ceres-mine",
                title: "Ceres Mine",
                coords: "1077,894,18",
                description: "Grande mine à ciel ouvert exploitant des minerais rares. L'extraction est automatisée mais nécessite une maintenance constante.",
                activities: [
                    "Extraction de minerais rares",
                    "Maintenance d'équipements miniers",
                    "Commerce de matières premières",
                    "Exploration géologique"
                ]
            },
            {
                id: "gravis-uplink",
                title: "Gravis Uplink",
                coords: "551,840,17",
                description: "Station de communication relais connectant les installations isolées au réseau principal. Point névralgique des communications.",
                activities: [
                    "Communications relais",
                    "Transmission de données",
                    "Maintenance réseau",
                    "Surveillance électronique"
                ]
            },
            {
                id: "redrock-mine",
                title: "Redrock Mine",
                coords: "611,814,15",
                description: "Mine souterraine exploitant un filon de minerai rouge aux propriétés énergétiques uniques. Très recherché pour les technologies avancées.",
                activities: [
                    "Extraction de minerai énergétique",
                    "Exploration souterraine",
                    "Commerce de cristaux",
                    "Recherche énergétique"
                ]
            },
            {
                id: "crest-uplink",
                title: "Crest Uplink",
                coords: "789,832,17",
                description: "Station de communication haute sécurité servant aux transmissions militaires et gouvernementales cryptées.",
                activities: [
                    "Communications sécurisées",
                    "Transmissions militaires",
                    "Cryptage",
                    "Sécurité nationale"
                ]
            },
            {
                id: "calida-village",
                title: "Calida Village",
                coords: "818,849,14",
                description: "Village thermal construit autour de sources chaudes naturelles. Centre de relaxation et de soins pour les voyageurs des wastelands.",
                activities: [
                    "Thermes curatifs",
                    "Soins médicaux",
                    "Repos et récupération",
                    "Commerce de produits médicinaux"
                ]
            },
            {
                id: "foster-uplink",
                title: "Foster Uplink",
                coords: "989,835,16",
                description: "Station de communication commerciale gérée par la famille Foster. Spécialisée dans les communications d'affaires.",
                activities: [
                    "Communications commerciales",
                    "Transactions financières",
                    "Commerce électronique",
                    "Services d'affaires"
                ]
            },
            {
                id: "techhaven",
                title: "Techhaven",
                coords: "625,743,21",
                description: "Principal centre de recherche technologique des wastelands. Ce complexe abrite les laboratoires les plus avancés et les chercheurs les plus brillants.",
                activities: [
                    "Recherche technologique avancée",
                    "Développement d'implants",
                    "Innovation cybernétique",
                    "Formation scientifique"
                ]
            },
            {
                id: "shirkan-fortress",
                title: "Shirkan Fortress",
                coords: "870,714,17",
                description: "Ancienne forteresse reconvertie en centre de formation pour mercenaires. Réputée pour ses instructeurs expérimentés.",
                activities: [
                    "Formation de mercenaires",
                    "Entraînement au combat",
                    "Recrutement militaire",
                    "École de guerre"
                ]
            },
            {
                id: "catlock-bay",
                title: "Catlock Bay",
                coords: "1054,728,15",
                description: "Baie naturelle protégée utilisée comme port sûr pour les navires de commerce. Centre de transit pour les marchandises maritimes.",
                activities: [
                    "Port commercial",
                    "Transit maritime",
                    "Entreposage",
                    "Commerce international"
                ]
            }
        ];

        document.addEventListener('DOMContentLoaded', function() {
    // Ajouter les styles CSS pour les zones
    const style = document.createElement('style');
    style.textContent = `
.map-container {
    position: relative;
    display: inline-block;
}

.map-image {
    max-width: 100%;
    height: auto;
    display: block;
}

.map-area {
    position: absolute;
    border: 2px solid transparent;
    background: transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 10;
}

.map-area.circle {
    z-index: 50 !important;
    border: 3px solid transparent;
    background: transparent;
}

.map-area.rectangle {
    z-index: 10;
}

.map-area:hover {
    border-color: rgba(255, 162, 0, 1);
    background: rgba(255, 255, 0, 0.2);
    box-shadow: 0 0 10px rgba(255, 145, 0, 0.85);
}

.map-area.circle:hover {
    border-color: rgba(255, 153, 0, 1);
    background: rgba(255, 255, 0, 0.3);
    box-shadow: 0 0 15px rgba(255, 153, 0, 1);
    transform: scale(1.05);
}

.map-area.active {
    border-color: rgba(0, 255, 0, 0.9) !important;
    background: rgba(0, 255, 0, 0.3) !important;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.7);
}

.map-area.circle.active {
    border-color: rgba(0, 255, 0, 1) !important;
    background: rgba(0, 255, 0, 0.4) !important;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.9);
    transform: scale(1.1);
}

.map-area[title]:hover::after {
    content: attr(title);
    position: absolute;
    top: -35px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 13px;
    font-weight: bold;
    white-space: nowrap;
    z-index: 1000;
    pointer-events: none;
}

.polygon-area {
    position: absolute;
    z-index: 15;
    cursor: pointer;
}

.polygon-area svg {
    width: 100%;
    height: 100%;
}

.polygon-area polygon {
    fill: transparent;
    stroke: transparent;
    stroke-width: 2;
    transition: all 0.3s ease;
}

.polygon-area:hover polygon {
    fill: rgba(255, 255, 0, 0.2);
    stroke: rgba(255, 166, 0, 0.9);
    filter: drop-shadow(0 0 10px rgba(255, 255, 0, 0.5));
}

.polygon-area.active polygon {
    fill: rgba(0, 255, 0, 0.3) !important;
    stroke: rgba(0, 255, 0, 0.9) !important;
    filter: drop-shadow(0 0 15px rgba(0, 255, 0, 0.7));
}
    `;
    document.head.appendChild(style);
    
    // Référence aux conteneurs de cartes
    const caligaMap = document.getElementById('caliga-map');
    const wastelandsMap = document.getElementById('wastelands-map');
    const zoneInfo = document.getElementById('zone-info');
    
    // Référence aux boutons de sélection de carte
    const mapButtons = document.querySelectorAll('.map-button');
    
    // Fonction pour créer un polygone SVG
    function createPolygonArea(zone, coords) {
        const xCoords = [];
        const yCoords = [];
        
        for (let i = 0; i < coords.length; i += 2) {
            xCoords.push(coords[i]);
            yCoords.push(coords[i + 1]);
        }
        
        const minX = Math.min(...xCoords);
        const maxX = Math.max(...xCoords);
        const minY = Math.min(...yCoords);
        const maxY = Math.max(...yCoords);
        
        const width = maxX - minX;
        const height = maxY - minY;
        
        // Créer les points relatifs pour le SVG
        const points = [];
        for (let i = 0; i < coords.length; i += 2) {
            const x = coords[i] - minX;
            const y = coords[i + 1] - minY;
            points.push(`${x},${y}`);
        }
        
        const area = document.createElement('div');
        area.className = 'polygon-area';
        area.setAttribute('data-id', zone.id);
        area.setAttribute('title', zone.title);
        area.style.left = minX + 'px';
        area.style.top = minY + 'px';
        area.style.width = width + 'px';
        area.style.height = height + 'px';
        
        area.innerHTML = `
            <svg viewBox="0 0 ${width} ${height}">
                <polygon points="${points.join(' ')}" />
            </svg>
        `;
        
        return area;
    }
    
    // Fonction pour créer les zones cliquables sur une carte
    function createMapAreas(mapContainer, zones) {
        // Supprimer les anciennes zones
        mapContainer.querySelectorAll('.map-area, .polygon-area').forEach(area => area.remove());
        
        // Créer les zones cliquables
        zones.forEach(zone => {
            const coords = zone.coords.split(',').map(Number);
            let area;
            
            // Gérer les polygones spécialement
            if (zone.type === 'polygon') {
                area = createPolygonArea(zone, coords);
            } else {
                area = document.createElement('div');
                area.className = 'map-area';
                area.setAttribute('data-id', zone.id);
                area.setAttribute('title', zone.title);
                
                // Détecter le type de zone basé sur le nombre de coordonnées
                if (coords.length === 3) {
                    // Cercle : x, y, radius
                    const [x, y, radius] = coords;
                    area.style.left = (x - radius) + 'px';
                    area.style.top = (y - radius) + 'px';
                    area.style.width = (radius * 2) + 'px';
                    area.style.height = (radius * 2) + 'px';
                    area.style.borderRadius = '50%';
                } else if (coords.length === 4) {
                    // Rectangle : x1, y1, x2, y2
                    const [x1, y1, x2, y2] = coords;
                    area.style.left = Math.min(x1, x2) + 'px';
                    area.style.top = Math.min(y1, y2) + 'px';
                    area.style.width = Math.abs(x2 - x1) + 'px';
                    area.style.height = Math.abs(y2 - y1) + 'px';
                    area.style.borderRadius = '0';
                }
            }
            
            // Ajouter les événements de clic
            area.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Retirer la classe active de toutes les zones
                document.querySelectorAll('.map-area, .polygon-area').forEach(a => a.classList.remove('active'));
                
                // Ajouter la classe active à la zone cliquée
                this.classList.add('active');
                
                // Afficher les informations de la zone
                displayZoneInfo(zone);
            });
            
            mapContainer.appendChild(area);
        });
        
        console.log(`Created ${zones.length} zones for map`);
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
        const closeBtn = document.getElementById('close-info');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                zoneInfo.style.display = 'none';
            });
        }
    
        // Afficher la boîte d'infos
        zoneInfo.style.display = 'block';
    }
    
    // Fonction pour changer de carte
    function switchMap(mapId) {
        console.log('Switching to map:', mapId);
        
        // Cacher toutes les cartes
        caligaMap.style.display = 'none';
        wastelandsMap.style.display = 'none';
        
        // Afficher la carte sélectionnée et créer ses zones
        if (mapId === 'caliga') {
            caligaMap.style.display = 'block';
            setTimeout(() => {
                createMapAreas(caligaMap, caligaZones);
                adjustAreaPositions();
            }, 100);
        } else if (mapId === 'wastelands') {
            wastelandsMap.style.display = 'block';
            setTimeout(() => {
                createMapAreas(wastelandsMap, wastelandsZones);
                adjustAreaPositions();
            }, 100);
        }
        
        // Réinitialiser les informations de zone
        zoneInfo.innerHTML = `
            <h3 class="zone-title">Sélectionnez une zone</h3>
            <p class="zone-description">Cliquez sur une zone de la carte pour afficher ses informations.</p>
        `;
        zoneInfo.style.display = 'none';
        
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
    
    // Correction des positions des zones pour les adapter à la taille réelle des images
    function adjustAreaPositions() {
        const maps = [
            { container: caligaMap, originalWidth: 1790, originalHeight: 2200 },
            { container: wastelandsMap, originalWidth: 1600, originalHeight: 1200 } // Correction des dimensions
        ];
        
        maps.forEach(map => {
            if (map.container.style.display === 'none') return;
            
            const mapImage = map.container.querySelector('.map-image');
            const mapAreas = map.container.querySelectorAll('.map-area, .polygon-area');
            
            if (!mapImage || mapAreas.length === 0) return;
            
            // Attendre que l'image soit chargée
            if (mapImage.naturalWidth === 0) {
                mapImage.onload = function() {
                    adjustSingleMap(map, mapImage, mapAreas);
                };
            } else {
                adjustSingleMap(map, mapImage, mapAreas);
            }
        });
    }
    
    function adjustSingleMap(map, mapImage, mapAreas) {
        // Obtenir les dimensions actuelles de l'image
        const actualWidth = mapImage.clientWidth;
        const actualHeight = mapImage.clientHeight;
        
        if (actualWidth === 0 || actualHeight === 0) return;
        
        // Calculer les ratios d'échelle
        const widthRatio = actualWidth / map.originalWidth;
        const heightRatio = actualHeight / map.originalHeight;
        
        console.log(`Adjusting ${mapAreas.length} areas with ratios: ${widthRatio.toFixed(3)}, ${heightRatio.toFixed(3)}`);
        console.log(`Image dimensions: ${actualWidth}x${actualHeight}, Original: ${map.originalWidth}x${map.originalHeight}`);
        
        // Ajuster les positions et dimensions des zones
        mapAreas.forEach(area => {
            const originalLeft = parseInt(area.style.left);
            const originalTop = parseInt(area.style.top);
            const originalWidth = parseInt(area.style.width);
            const originalHeight = parseInt(area.style.height);
            
            if (!isNaN(originalLeft) && !isNaN(originalTop)) {
                area.style.left = (originalLeft * widthRatio) + 'px';
                area.style.top = (originalTop * heightRatio) + 'px';
                area.style.width = (originalWidth * widthRatio) + 'px';
                area.style.height = (originalHeight * heightRatio) + 'px';
            }
        });
    }
    
    // Ajuster les positions lors du chargement et du redimensionnement
    window.addEventListener('load', adjustAreaPositions);
    window.addEventListener('resize', adjustAreaPositions);
    
    // Afficher la carte de Caliga par défaut
    switchMap('caliga');
});