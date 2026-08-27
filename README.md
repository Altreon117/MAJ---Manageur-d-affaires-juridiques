# MAJ - Manageur d'Affaires Juridiques

Application de bureau destinée au suivi des affaires judiciaires, de la rédaction des rapports et des paiements. Elle a été développée en Python avec PyQt6 pour l'interface, Pandas/OpenPyXL pour les fichiers Excel et `imap-tools` pour la messagerie IMAP.

L'application gère trois grands types d'affaires judiciaires :

* **OPJ** (Officier de Police Judiciaire)
* **JAF** (Juge aux Affaires Familiales)
* **JI** (Juge d'Instruction)

## Sommaire

- [Prérequis](#prérequis)
- [Arborescence](#arborescence)
- [Installation et Commandes de Développement](#installation-et-commandes-de-développement)
- [Fichiers Excel](#fichiers-excel)
- [Liaison de la Messagerie (Mail)](#liaison-de-la-messagerie-(mail))
- [Guide d'utilisation](#guide-dutilisation)
- [Développement et compilation](#développement-et-compilation)

## Prérequis

Avant l'installation, vérifier que la machine dispose des éléments suivants :

- **Python 3.10 ou supérieur**, ajouté au `PATH` pour pouvoir utiliser les commandes `python` et `pip` ;
- **un compte Google avec une adresse Gmail**, utilisé pour la détection des nouvelles missions par messagerie IMAP ;
- **la validation en deux étapes activée** sur ce compte Google ;
- **un mot de passe d'application Google** dédié à MAJ. Le mot de passe habituel du compte Google ne doit pas être utilisé dans `.env` ;
- **un fichier maître Excel** nommé `EXPERTISES JUDICIAIRES.xlsx`, placé dans le dossier `assets/`.

Une connexion Internet est nécessaire pour vérifier la boîte Gmail. Les droits d'écriture sont également nécessaires dans le dossier du projet, car l'application crée et actualise les fichiers Excel dérivés et les fichiers de cache.

## Arborescence

```text
MAJ---Manageur-d-affaires-juridiques/
├── assets/
│   ├── EXPERTISES JUDICIAIRES.xlsx          # Fichier maître
│   ├── EXPERTISES JUDICIAIRES- OPJ.xlsx     # Fichier généré pour les OPJ
│   ├── EXPERTISES JUDICIAIRES- JAF.xlsx     # Fichier généré pour les JAF
│   ├── EXPERTISES JUDICIAIRES- JI.xlsx      # Fichier généré pour les JI
│   ├── NOTIFICATIONS_MISSIONS.xlsx          # Cache des missions reçues
│   ├── REFUS_MISSION.xlsx                   # Missions refusées
│   └── *.png                                # Icônes de l'application
├── src/
│   ├── backend/
│   │   ├── excel_manager.py                 # Lecture, écriture et synchronisation Excel
│   │   └── mail_connector.py                # Connexion à Gmail en IMAP
│   └── ui/
│       ├── add_affaire_dialog.py            # Formulaire de création d'une affaire
│       ├── card_dashboard_component.py      # Carte d'un indicateur du dashboard
│       ├── card_jaf_component.py            # Carte d'une affaire JAF
│       ├── card_ji_component.py             # Carte d'une affaire JI
│       ├── card_mission_component.py        # Carte d'une mission reçue par mail
│       ├── card_opj_component.py            # Carte d'une affaire OPJ
│       ├── customize_pins_dialog.py         # Personnalisation des indicateurs
│       ├── edit_affaire_dialog.py           # Formulaire de modification d'une affaire
│       ├── main_window.py                   # Fenêtre principale et navigation
│       ├── notification_menu.py             # Menu des notifications de missions
│       ├── view_dashboard.py                # Accueil et indicateurs
│       ├── view_jaf.py                      # Vue de gestion des affaires JAF
│       ├── view_ji.py                       # Vue de gestion des affaires JI
│       ├── view_opj.py                      # Vue de gestion des affaires OPJ
├── .env                                     # Identifiants locaux, à ne pas versionner
├── .gitignore                               # Rends certains fichiers et dossiers invisibles à github lors du push
├── config.py                                # Chemins, colonnes, choix et styles
├── main.py                                  # Point d'entrée
└── requirements.txt                         # Dépendances Python
```

Les fichiers Excel OPJ/JAF/JI sont des fichiers dérivés : ils sont recréés depuis le fichier maître lorsque celui-ci est plus récent ou lorsqu'un fichier dérivé manque. Il faut donc modifier les données depuis l'application ou depuis le fichier maître, puis relancer l'application.

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

Au premier lancement, le fichier maître doit déjà être présent dans `assets/`. Les fichiers dérivés et les caches sont créés ou actualisés automatiquement.

## Fichiers Excel

### Fichier maître

Le fichier `assets/EXPERTISES JUDICIAIRES.xlsx` peut contenir un ou plusieurs onglets. Ils sont fusionnés, dédoublonnés, puis répartis selon `REF AFFAIRE`.

| Colonne | Obligatoire | Rôle et valeur attendue |
| --- | --- | --- |
| `REF AFFAIRE` | Oui | Type d'affaire : `OPJ`, `JAF` ou `JI`. Les espaces et la casse sont normalisés lors du découpage. |
| `NOM` | Oui pour identifier une affaire | Nom de l'affaire. Sert de clé de secours pour les mises à jour et au dédoublonnage. |
| `CHORUS PRO` | Oui pour OPJ/JI et le rapprochement des paiements | Référence de facturation, par exemple `MJ12345`. Elle doit correspondre aux références du relevé bancaire. |

`REF AFFAIRE` est indispensable au découpage. `NOM` et `CHORUS PRO` sont les clés utilisées par le logiciel lorsqu'elles existent ; il est recommandé de les renseigner sur chaque ligne.

### Colonnes attendues par type

Les noms doivent être repris exactement, y compris les accents, les espaces et la casse. `montant` doit être convertible en nombre. Les dates peuvent être des dates Excel reconnues par Pandas ou du texte cohérent.

| Type | Colonnes backend définies dans `config.py` |
| --- | --- |
| **OPJ** | `NOM`, `Planification`, `Column 13`, `Propriétaire`, `CHORUS PRO`, `periode`, `montant`, `État`, `État 2` |
| **JAF** | `NOM`, `Planification`, `DATE`, `date de redaction du rapport`, `DATE REMISE DES RAPPORT`, `periode`, `État`, `État 2`, `montant` |
| **JI** | `NOM`, `periode`, `Planification`, `CHORUS PRO`, `État`, `État 2`, `montant` |

Les colonnes affichées sont configurées dans `OPJ_FRONT_COLUMNS`, `JAF_FRONT_COLUMNS` et `JI_FRONT_COLUMNS`. La vue JAF peut afficher `Propriétaire` s'il est présent, même si cette colonne ne figure pas dans `JAF_BACK_COLUMNS`.

Les valeurs proposées lors de la modification sont :

- `État` : `A faire`, `Terminé`, `Pas commencé`, `En cours` ;
- `État 2` : `payé`, `En attente`, `Non payé`, `N/A` ;
- `Planification` : `VU`, `ATTENTE DATES`, `A CONVOQUER`, `N/A`.

### Fichiers de cache

- `NOTIFICATIONS_MISSIONS.xlsx` contient `sujet`, `date` et `uid`.
- `REFUS_MISSION.xlsx` contient `Sujet` et `Date`.

Ces deux fichiers sont gérés automatiquement par l'application.

## Liaison de la Messagerie (Mail)

Le logiciel scanne automatiquement la boîte mail Google en arrière-plan pour détecter les nouvelles missions entrantes, une fois lors du lancement du logiciel, puis toutes les 30 minutes. Pour des raisons de sécurité, l'accès se fait obligatoirement via un mot de passe d'application.

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

Le menu de notification permet de consulter les missions détectées, de les accepter ou de les refuser. Une mission refusée est conservée dans `REFUS_MISSION.xlsx` et ne sera plus proposée.

## Guide d'utilisation

### 1. Accueil et navigation

Le bandeau supérieur donne accès aux pages **Accueil**, **OPJ**, **JAF** et **JI**. L'accueil affiche six indicateurs par défaut : totaux OPJ/JAF/JI, dossiers en attente de paiement, montant total facturé et rapports à faire. Les indicateurs disponibles peuvent être personnalisés dans l'application ; ils incluent aussi les affaires terminées et les dossiers sans référence Chorus Pro.

### 2. Rechercher, filtrer et trier

Dans une page OPJ, JAF ou JI :

1. Utiliser la barre de recherche pour filtrer instantanément les cartes selon leur contenu.
2. Utiliser les listes à gauche pour croiser les critères disponibles. OPJ propose aussi le filtre de planification.
3. Cliquer sur un bouton de tri pour trier une colonne. Un second clic désactive le tri et restaure l'ordre initial.

### 3. Ajouter et modifier une affaire

Les boutons d'ajout et de modification ouvrent un formulaire adapté au type d'affaire. Après validation, l'affaire est écrite dans le fichier du service et dans le fichier maître. Lors d'un ajout, `REF AFFAIRE` est renseigné automatiquement avec `OPJ`, `JAF` ou `JI` dans le fichier maître.

Pour une modification, le logiciel recherche d'abord `CHORUS PRO` lorsqu'il est renseigné, puis utilise `NOM` comme solution de repli, notamment pour les JAF.

### 4. Mettre à jour les paiements

1. Cliquer sur le bouton flottant de paiement en bas à droite.
2. Sélectionner un fichier Excel de relevé bancaire.
3. Vérifier qu'il contient une colonne nommée exactement `Référence`.

Le logiciel extrait dans cette colonne les motifs `MJ` suivis de chiffres, les compare à `CHORUS PRO`, puis remplace `État 2` par `payé` dans le fichier maître et dans les fichiers OPJ/JAF/JI concernés.

### 5. Notifications de missions

La cloche signale les missions reçues depuis la dernière date enregistrée. Ouvrir le menu pour traiter chaque mission. L'acceptation retire la notification du cache ; le refus la retire également et l'ajoute à la liste des missions refusées.

## Compilation

Créer un exécutable Windows avec PyInstaller :

```bash
pyinstaller --noconsole --name "MAJ" --icon="assets/app_icon.png" --add-data "assets;assets" --add-data ".env;." main.py
```

A la fin de la compilation, si cette dernière c'est bien passé, vous devrez pourvoir lire similaire à `47836 INFO: Build complete! The results are available in: C:\Emplacement\Du\Dossier\Dans\Votre\Machine\MAJ---Manageur-d-affaires-juridiques\dist`

La compilation crée les éléments suivants à la racine du projet :

- `/dist` : contient le résultat distribuable de la compilation. Avec cette commande, il contient le dossier `MAJ - Manageur d'affaires juridiques` et l'exécutable Windows ;
- `/build` : contient les fichiers temporaires utilisés par PyInstaller pendant la construction. Il peut être supprimé après une compilation réussie ;
- `MAJ - Manageur d'affaires juridiques.spec` : fichier de configuration généré par PyInstaller. Il peut être réutilisé pour relancer ou personnaliser une compilation.

Vous trouverez dans le dossier `dist/MAJ - Manageur d'affaires juridiques` le logiciel **MAJ - Manageur d'affaires juridiques.exe**, ainsi que les ressources nécessaires à son fonctionnement, notamment le dossier `_internal` et une copie de `assets` intégrée par l'option `--add-data`.

Pour distribuer l'application, transmettre le dossier complet présent dans `dist`, et non le seul fichier `.exe` : l'exécutable dépend des fichiers et bibliothèques qui l'accompagnent.

Ne jamais publier `.env` ni les fichiers Excel contenant des données réelles. Avant toute modification manuelle du fichier maître, effectuer une copie de sauvegarde.