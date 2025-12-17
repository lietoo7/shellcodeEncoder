  

#README (`Encoder.py`)

Ce projet implémente une méthode de stéganographie visant à dissimuler un contenu secret (le *payload*, généralement du texte ou du code) à l'intérieur d'un fichier HTML hôte. L'information cachée est insérée dans des éléments HTML structurellement insignifiants (commentaires, fausses variables JS/CSS) pour minimiser l'impact visuel et fonctionnel du document.

##1. Objectifs et Fonctionnalités Clés
Le script `Encoder.py` satisfait les besoins fonctionnels suivants :

| ID | Fonctionnalité | Description |
| --- | --- | --- |
| **BF002** | **Encodage Base64** | Le contenu du fichier secret est encodé en Base64 avant l'injection. |
| **BF003** | **Création Hôte Stéganographié** | Génération d'un fichier de sortie (`jesuiscacher.html`) visuellement identique au fichier source. |
| **BF004** | **Ciblage d'Injection Sûr** | L'injection est ciblée **uniquement après** une liste prédéfinie de balises de fermeture sûres (`</div>`, `</p>`, `</body>`, etc.) pour préserver l'intégrité du rendu. |
| **BF005** | **Injection Séquentielle** | Les caractères du payload encodé sont insérés séquentiellement, dans l'ordre du flux Base64. |
| **BF010** | **Auto-Correction de Capacité** | Si le fichier hôte ne contient pas assez d'emplacements sûrs, le script injecte un bloc invisible de balises de fermeture (`</p>`) avant `</body>` pour garantir l'espace nécessaire au payload. |

##2. PrérequisLe projet ne nécessite que l'environnement d'exécution **Python 3** et ses librairies standards.

##3. Utilisation###3.1 ExécutionLe script s'exécute directement en ligne de commande (CLI). Il nécessite **deux arguments de chemin** : le fichier HTML hôte et le fichier source du payload.

**Syntaxe :**

```bash
python Encoder.py <FICHIER_HTML_SOURCE> <FICHIER_PAYLOAD_SOURCE>

```

**Exemple :**

Pour cacher le contenu de `mon_message_secret.txt` dans `mapage.html`, utilisez la commande :

```bash
python encoder.py mapage.html mon_message_secret.txt

```

###3.2 SortieSi l'exécution est réussie, le script génère un nouveau fichier :

* **Fichier de sortie :** `jesuiscacher.html`

Ce fichier contient l'intégralité du contenu de l'hôte augmenté des injections stéganographiques.

##4. Détails Techniques de l'EncodageL'encodage repose sur l'alternance aléatoire de deux méthodes d'injection pour chaque caractère du *payload* Base64 :

###4.1 Injection par Faux Commentaire HTML (BF006)Le caractère est encapsulé dans un commentaire HTML. Un identifiant de stéganographie (`stg_c`) et un *padding* aléatoire sont inclus pour masquer la longueur et la fonction du commentaire.

**Format de l'injection (Exemple pour le caractère 'S') :**

```html

```

###4.2 Injection par Fausse Variable (JS ou CSS) (BF007)Le caractère est caché dans une déclaration de variable inutilisée. Le type (JS ou CSS) et le nom de la variable sont générés aléatoirement pour éviter la détection.

**Exemple d'injection JavaScript (Exemple pour le caractère 'G') :**

```html
<script>var _aB7f45 = 'G';</script>

```

**Exemple d'injection CSS (Exemple pour le caractère 'V') :**

```html
<style> :root {--c2P9j988: 'V';} </style>

```

##5. Robustesse et Résilience (BF010)Si le fichier HTML hôte initial ne contient pas suffisamment de balises de fermeture (comme dans un document très simple), la fonction `auto_patch_html_slots` ajoute un grand nombre de balises `</p>` dans un conteneur invisible (`<div style="display:none;">`) juste avant la balise `</body>`.

Ce mécanisme garantit que l'encodage peut être effectué quel que soit la taille du payload, sans affecter le rendu visuel de la page.

 

