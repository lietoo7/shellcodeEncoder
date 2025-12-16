# README Stéganographie HTML (`Encoder.py`)

Ce projet implémente une méthode de stéganographie visant à dissimuler une chaîne de caractères secrète (le *payload*) à l'intérieur d'un fichier HTML hôte. L'information cachée est insérée dans des éléments HTML structurellement insignifiants (commentaires, fausses variables JS/CSS) pour minimiser l'impact visuel et fonctionnel du document.

## 1\. Objectifs du Prototype

Le script `Encoder.py` a été développé pour satisfaire les besoins fonctionnels suivants, définis dans le Cahier des Charges (CdC) :

1.  **Encodage Base64 (BF002) :** Le message secret est encodé en Base64 avant l'injection.
2.  **Injection Discrète (BF004, BF005) :** Le script insère séquentiellement les caractères du *payload* encodé à des intervalles réguliers dans le code source HTML, en alternant entre deux méthodes de dissimulation.
3.  **Création d'un Fichier Hôte Stéganographié (BF003) :** Génération d'un fichier de sortie (`jesuiscacher.html`) visuellement identique au fichier source.

## 2\. Prérequis

Le projet ne nécessite que l'environnement d'exécution **Python 3** et ses librairies standards :

  * `base64`
  * `argparse`
  * `random`
  * `string`
  * `os`, `sys`

## 3\. Utilisation

### 3.1 Exécution

Le script s'exécute directement en ligne de commande (CLI).

**Syntaxe :**

```bash
python Encoder.py <FICHIER_HTML_SOURCE> <CHAINE_A_CACHER>
```

**Exemple :**

Pour cacher le message "Le Projet Secret" dans `mapage.html`, utilisez la commande :

```bash
python Encoder.py mapage.html "Le Projet Secret"
```

### 3.2 Sortie

Si l'exécution est réussie, le script génère un nouveau fichier :

  * **Fichier de sortie :** `jesuiscacher.html`

Ce fichier contient l'intégralité du contenu de `mapage.html` augmenté des injections stéganographiques.

## 4\. Détails Techniques de l'Encodage

L'encodage repose sur l'alternance de deux méthodes d'injection pour chaque caractère du *payload* Base64 :

### 4.1 Injection par Faux Commentaire HTML (BF006)

Le caractère est encapsulé dans un commentaire. Le commentaire inclut un identifiant (`stg_c:`) et un *padding* aléatoire pour masquer la longueur constante de l'information utile.

**Exemple d'injection dans le code source :**

```html
<p>Contenu visible.</p>
<div>Suite du contenu.</div>
```

### 4.2 Injection par Fausse Variable (JS ou CSS) (BF007)

Le caractère est caché dans une déclaration de variable inutilisée, insérée généralement dans le `<head>` ou le `<body>`. Le nom de la variable est généré aléatoirement pour éviter la détection par des motifs statiques.

**Exemple d'injection JavaScript :**

```html
</head>
<script>var _aB7f45 = 'G';</script>
<body>
```

**Exemple d'injection CSS :**

```html
<style> :root {--c2P9j: 'V';} </style>
<body>
```

## 5\. Recommandations et Limitations

  * **Taux d'Injection (`INJECTION_RATE`) :** La variable globale `INJECTION_RATE` (par défaut à 200) détermine le nombre de caractères du fichier hôte entre chaque injection. Un taux plus élevé augmente la discrétion mais nécessite un fichier hôte plus grand pour insérer tout le *payload*.
  * **Intégrité Visuelle :** La validation finale (UC005) consiste à s'assurer qu'aucune des injections (commentaires ou variables) n'est visible dans le rendu du navigateur, ni ne provoque d'erreurs dans la console.
  * **Décodage :** Ce prototype ne contient que l'encodeur. Un script `Decoder.py` sera nécessaire pour extraire, réassembler et décoder en Base64 la chaîne de caractères cachée.

