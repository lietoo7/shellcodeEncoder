# Cahier des Charges pour le Projet Stéganographie HTML

## 1. Introduction
### 1.1 Objectifs du Projet
L'objectif principal du projet est de développer un script Python (`Encoder.py`) capable d'encoder une chaîne de caractères secrète (le *payload*) et de la cacher à l'intérieur d'un fichier HTML hôte existant (`mapage.html`), en utilisant des éléments HTML structurellement insignifiants (comme des commentaires ou des variables JavaScript/CSS) pour masquer l'information. Le fichier résultant (`jesuiscacher.html`) doit être **visuellement et fonctionnellement identique** au fichier source, rendant la présence de l'information cachée difficile à détecter sans une analyse approfondie.

### 1.2 Contexte du Projet
Ce projet s'inscrit dans le cadre d'un challenge informatique (probablement un CTF ou une épreuve de sécurité) visant à explorer les techniques de **stéganographie**, où l'on cache l'existence d'un message dans un support d'apparence inoffensive. L'idée est de prouver qu'une information peut être transmise sans altérer la perception visuelle du document par l'utilisateur final.

---

## 2. Analyse des Besoins
### 2.1 Besoins Fonctionnels

| ID | Description du Besoin |
| :--- | :--- |
| **BF001** | Le système doit accepter un fichier HTML source (`mapage.html`) et une chaîne de caractères à cacher (`HelloWorld`) en entrée. |
| **BF002** | Le système doit encoder la chaîne de caractères en **Base64** (e.g., `HelloWorld` $\rightarrow$ `SGVsbG9Xb3JsZA==`). |
| **BF003** | Le système doit créer une copie de travail du fichier HTML source (`jesuiscacher.html`). |
| **BF004** | Le système doit insérer séquentiellement chaque caractère du *payload* Base64 dans le fichier HTML de manière cachée. |
| **BF005** | Le système doit utiliser une stratégie de placement aléatoire ou semi-aléatoire des caractères pour compliquer la détection. |
| **BF006** | Le système doit implémenter une fonction `creer_fauxcommentaire(caractere)` pour encapsuler un caractère dans un commentaire HTML (``). |
| **BF007** | Le système doit implémenter une fonction `creer_faussevariable(caractere)` pour encapsuler un caractère dans une fausse variable (e.g., JS ou CSS). |
| **BF008** | Le fichier de sortie (`jesuiscacher.html`) doit être un document HTML valide et fonctionnellement équivalent au document source. |

### 2.2 Besoins Non Fonctionnels
* **Facilité d'utilisation :** Le script doit être exécutable en ligne de commande avec des arguments clairs.
* **Fiabilité :** Le processus d'encodage doit garantir que tous les caractères du *payload* Base64 sont insérés.
* **Maintenabilité :** Le code Python doit être clair, modulaire et documenté (docstrings).
* **Discrétion :** L'altération du fichier HTML doit être minimale et ne pas affecter le rendu visuel.

---

## 3. Spécifications Fonctionnelles
### 3.1 Fonctionnalités Principales

#### 3.1.1 Script Principal (`Encoder.py`)
Le script sera exécuté comme suit :
`python Encoder.py <fichier_html_source> <chaine_a_cacher>`

1.  **Lecture et Initialisation :** Lire le contenu du `<fichier_html_source>`.
2.  **Encodage du Payload :** Appliquer l'encodage Base64 à la `<chaine_a_cacher>`.
3.  **Itération et Placement :** Parcourir le contenu du fichier HTML, caractère par caractère ou ligne par ligne. À des points d'insertion déterminés, insérer le caractère Base64 suivant, en alternant entre les deux méthodes d'encapsulation.

#### 3.1.2 Fonction `creer_fauxcommentaire(caractere)` (BF006)
* **Entrée :** `caractere` (un caractère du *payload* Base64).
* **Sortie :** Une chaîne de caractères représentant un commentaire HTML contenant le caractère.
* **Exemple de structure :** ``
    * *Note :* L'ajout de caractères de *padding* aléatoires ou de texte factice dans le commentaire peut augmenter la discrétion.

#### 3.1.3 Fonction `creer_faussevariable(caractere)` (BF007)
* **Entrée :** `caractere` (un caractère du *payload* Base64).
* **Sortie :** Une chaîne de caractères représentant une instruction de variable factice, souvent dans un bloc `<script>` ou `<style>`.
* **Exemple de structure :**
    * **JS :** `<script>var _${random_id} = '${caractere}';</script>`
    * **CSS :** `<style> :root {--${random_name}: '${caractere}';} </style>`
    * *Note :* L'utilisation de variables non utilisées et de noms aléatoires renforce la dissimulation.

### 3.2 Cas d'Utilisation

| ID | Cas d'Utilisation | Description | Acteur Principal |
| :--- | :--- | :--- | :--- |
| **UC001** | Exécuter le Script d'Encodage | L'utilisateur lance le script avec les deux arguments requis. | Utilisateur |
| **UC002** | Encodage Base64 | Le script encode la chaîne en Base64. | Système |
| **UC003** | Injection d'un Caractère (Commentaire) | Le script appelle `creer_fauxcommentaire()` et insère le résultat à une position valide (e.g., après une balise fermante). | Système |
| **UC004** | Injection d'un Caractère (Variable) | Le script appelle `creer_faussevariable()` et insère le résultat dans la section `<head>` ou `<body>`. | Système |
| **UC005** | Vérification Visuelle | L'utilisateur ouvre `mapage.html` et `jesuiscacher.html` pour confirmer l'identité visuelle. | Utilisateur |

### 3.3 Interfaces Utilisateur
L'interface utilisateur sera uniquement en **ligne de commande (CLI)**, utilisant les arguments de `sys.argv` ou le module `argparse` de Python.

---

## 4. Spécifications Non Fonctionnelles
### 4.1 Performance
Le script doit pouvoir traiter des fichiers HTML de taille moyenne (jusqu'à 1 Mo) en quelques secondes. Étant donné la longueur relativement courte du *payload* Base64 (128 caractères max, par exemple), la performance ne devrait pas être un facteur limitant.

### 4.2 Sécurité
* **Intégrité des données :** Le script doit s'assurer que le *payload* est inséré sans aucune erreur de caractère.
* **Discrétion :** L'objectif est d'assurer la **stéganographie**. Les injections ne doivent pas provoquer d'erreurs d'affichage ou de scripts dans le navigateur. Une attention particulière sera portée à la non-interruption du flux de balises (par exemple, ne pas insérer de commentaire au milieu d'un attribut de balise).

### 4.3 Scalabilité
Le script est conçu pour être un outil ponctuel. La gestion d'un très grand nombre de caractères ou de très gros fichiers HTML n'est pas une priorité immédiate, mais la logique d'itération et d'insertion devrait pouvoir gérer des *payloads* plus longs sans refonte majeure.

### 4.4 Disponibilité
Le script doit être disponible pour exécution immédiate après son développement. Il ne nécessite pas de base de données ni de service externe. Il dépend uniquement de l'environnement d'exécution **Python 3** et de ses librairies standard (`base64`, `os`, `sys` ou `argparse`).
