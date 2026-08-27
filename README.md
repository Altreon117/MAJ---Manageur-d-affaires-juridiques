# MAJ - Manageur d'Affaires Juridiques

Outil de bureau automatisé conçu dans le cadre d'un stage de deuxième année de Bachelor Informatique à Paris Ynov Campus (Nanterre). Développé par Raphaël Phan, ce logiciel est destiné aux professionnels du milieu juridique. Son but principal est d'offrir un gain de temps massif sur le suivi quotidien du travail, en automatisant la gestion des dossiers, la facturation et la synchronisation des données.

L'application gère trois grands types d'affaires judiciaires :

* **OPJ** (Officier de Police Judiciaire)
* **JAF** (Juge aux Affaires Familiales)
* **JI** (Juge d'Instruction)

**Pile Technologique** : Développé en Python 3, l'interface graphique repose sur PyQt6, tandis que la manipulation des données est assurée par Pandas. Les connexions serveur s'effectuent via `imap-tools`.

## Arborescence du Projet et Configuration

Le projet respecte une architecture modulaire stricte séparant le backend de l'interface utilisateur.

```text
MAJ/
├── assets/                 # Dossier critique contenant les bases de données et icônes
│   ├── EXPERTISES JUDICIAIRES.xlsx  # Le fichier maître de la base de données
│   ├── REFUS_MISSION.xlsx           # Fichier de cache des missions refusées
│   ├── NOTIFICATIONS_MISSIONS.xlsx  # Fichier de cache des notifications lues
│   ├── app_icon.png                 # Icône principale de l'application
│   ├── notification_up-icon.png     # Icône de cloche avec alerte rouge
│   ├── notification_down-icon.png   # Icône de cloche standard (sans alerte)
│   └── update_transaction.png       # Icône du bouton flottant des paiements
├── src/
│   ├── backend/            # Logique métier (ExcelManager, MailConnector)
│   └── ui/                 # Vues (Dashboard, JAF, OPJ, JI) et composants (Cartes, Dialogues)
├── .env                    # Fichier caché contenant les identifiants de messagerie
├── config.py               # Fichier centralisant les chemins, dimensions, colonnes et styles QSS
├── main.py                 # Point d'entrée de l'application (initialisation PyQt6 et Windows AppID)
└── requirements.txt        # Liste des dépendances Python

```

## Base de Données Excel

Le système repose sur un fichier maître (`EXPERTISES JUDICIAIRES.xlsx`) qui est automatiquement découpé en sous-fichiers (OPJ, JAF, JI) au lancement pour optimiser les temps de chargement.

### Colonnes obligatoires du Fichier Maître

Pour que le système de découpage et d'anti-doublon fonctionne, le fichier global doit impérativement contenir les colonnes suivantes :

| Nom de la colonne | Type de donnée attendu | Description |
| --- | --- | --- |
| **REF AFFAIRE** | `Texte` (String) | Permet de diviser le fichier (Valeurs : "OPJ", "JAF", "JI")

 |
| **NOM** | `Texte` (String) | Nom du dossier/client (Utilisé pour l'anti-doublon)

 |
| **CHORUS PRO** | `Texte` (String) | Référence de facturation (Utilisé pour l'anti-doublon et les paiements)

 |

### Colonnes par type d'affaire

Chaque onglet de l'application gère des données spécifiques listées dans le fichier de configuration.

| Type | Colonnes lues par le logiciel | Format des données |
| --- | --- | --- |
| **OPJ** | NOM, Planification, Propriétaire, CHORUS PRO, periode, montant, État, État 2

 | `montant` en float64, autres en Texte |
| **JAF** | NOM, Planification, DATE, date de redaction du rapport, DATE REMISE DES RAPPORT, periode, État, État 2, montant

 | Dates gérées par Pandas, `montant` en float64 |
| **JI** | NOM, periode, Planification, CHORUS PRO, État, État 2, montant

 | `montant` en float64, autres en Texte |

## Liaison de la Messagerie (Mail)

Le logiciel scanne automatiquement la boîte mail en arrière-plan pour détecter les nouvelles missions entrantes. Pour des raisons de sécurité, l'accès se fait obligatoirement via un mot de passe d'application.

1. **Configuration du compte Google** :
* Connectez-vous à votre compte Gmail sur un navigateur.
* Accédez à **Gérer votre compte Google** > **Sécurité**.
* Activez impérativement la **Validation en deux étapes**.
* Cherchez **Mots de passe des applications** dans la barre de recherche des paramètres.
* Créez une nouvelle application nommée "MAJ" et copiez le code secret de 16 lettres généré.


2. **Configuration du projet (.env)** :
* À la racine du projet, créez un fichier nommé exactement `.env`.
* Ajoutez vos identifiants selon ce format strict :
```env
EMAIL_COMPTE="votre_adresse@gmail.com"
EMAIL_PASSWORD="les_16_lettres_du_mot_de_passe"

```





## Installation et Commandes de Développement

Pour faire tourner le projet sur une nouvelle machine de développement, suivez ces étapes dans votre terminal :

1. **Installation de Python** : Assurez-vous d'avoir Python 3.10 ou supérieur installé sur le système.
2. **Création de l'environnement virtuel** :
```bash
python -m venv venv

```


3. **Activation de l'environnement** :
* *Windows* : `.\venv\Scripts\activate`
* *Mac/Linux* : `source venv/bin/activate`


4. **Installation des dépendances** :
```bash
pip install -r requirements.txt

```


5. **Mise à jour des dépendances (Freeze)** : Si vous installez de nouveaux imports pendant le développement, mettez à jour le fichier texte avec :
```bash
pip freeze > requirements.txt

```


6. **Lancement de l'application** :
```bash
python main.py

```


7. **Compilation (Création du .exe)** :
```bash
pyinstaller --noconsole --name "MAJ" --icon="assets/app_icon.png" --add-data "assets;assets" --add-data ".env;." main.py

```



## Guide des Fonctionnalités de l'Application

L'interface graphique est conçue de manière ergonomique pour limiter les clics et centraliser les outils.

### 1. Composants Permanents

* **Le Header (En-tête)** : Permet la navigation fluide entre les différents onglets (Accueil, OPJ, JAF, JI). Sur la droite se trouve l'icône de notification. Elle s'affiche avec un point rouge (fichier `notification_up-icon.png`) lorsqu'un nouveau mail dont le sujet commence par "MISSION" est détecté. En cliquant dessus, un menu déroulant permet de consulter, accepter ou refuser ces affaires.


* **Le Bouton de Mise à Jour (Paiements)** : Un bouton flottant circulaire contenant le visuel `update_transaction.png` est situé en bas à droite de l'écran. En cliquant dessus, une boîte de dialogue s'ouvre pour sélectionner un relevé bancaire Excel. Le logiciel croise automatiquement le motif "MJ" suivi de chiffres dans ce relevé avec la colonne "CHORUS PRO" de vos dossiers, et passe le statut "État 2" à "payé".



### 2. Le Dashboard (Accueil)

Vue globale générant des indicateurs de performance en temps réel.

* Affiche 6 cartes personnalisables par défaut au lancement.


* Permet de suivre d'un coup d'œil le total de dossiers par service, les dossiers en attente de paiement, ou la somme totale facturée au cabinet.



### 3. Vues OPJ, JAF et JI

L'interface de gestion de chaque service suit la même structure pour faciliter la prise en main :

* **Filtres (Partie gauche)** : Des listes déroulantes permettent de filtrer finement les dossiers croisés par Période, Planification, Statut du rapport et Statut du paiement.


* **Barre de Recherche** : Saisie libre filtrant instantanément les cartes affichées par n'importe quelle donnée (nom, référence, etc.).


* **Boutons de Tri** : Des boutons "Switch" organisent les données affichées chronologiquement, alphabétiquement ou par montants.


* **Cartes Affaires** : Chaque dossier est encapsulé dans une carte visuelle. Un bouton "Modifier" ouvre une boîte de dialogue permettant de mettre à jour le dossier. La sauvegarde synchronise instantanément le fichier Excel spécifique du service ET le fichier maître global, évitant ainsi toute perte de données.