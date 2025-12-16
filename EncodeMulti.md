# Outil d'Obscurcissement de Shellcode Multi-Couches

Cet outil en C démontre une technique d'obscurcissement courante utilisée en sécurité et en anti-malware. 
Il prend un *shellcode* binaire et applique une séquence de quatre encodages différents pour le rendre non reconnaissable par les scanners de signatures statiques.

## Objectif du Programme

Le but de ce script est de transformer un *shellcode* brut en une chaîne 
de caractères encodée qui peut être intégrée sans danger dans un programme hôte (un *loader* ou un *dropper*). 
L'encodage appliqué est une séquence de chiffrement et de transformations binaires-texte.

## ⚙️ Compilation

Ce programme utilise la librairie **OpenSSL** pour l'encodage Base64, en particulier la suite d'outils **libcrypto**.

Vous devez vous assurer que les bibliothèques de développement OpenSSL sont installées sur votre système.

Utilisez la commande `gcc` suivante pour compiler :

```bash
gcc -Wall -Wextra -o encode encode.c -lcrypto
```

| Option | Description |
| :--- | :--- |
| `-Wall`, `-Wextra` | Active tous les avertissements pour un code robuste. |
| `-o encode` | Nom du fichier exécutable de sortie. |
| `-lcrypto` | Lie le programme à la librairie cryptographique OpenSSL (libcrypto). |

## Exécution

Exécutez l'outil pour voir le *shellcode* original et sa version encodée finale :

```bash
./encode
```

**Exemple de sortie :**

```
Shellcode original (21 octets) : \x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05

Représentation encodée :
M-S965A=Q9!N4:3T:1A]E1A]O;2$
```

## Chaîne d'Encodage

Le *shellcode* binaire est transformé par une séquence de quatre étapes. Pour *déchiffrer* le *shellcode* à l'exécution, le programme hôte doit appliquer ces étapes dans l'ordre inverse (4 $\rightarrow$ 3 $\rightarrow$ 2 $\rightarrow$ 1).

### 1\. XOR (Chiffrement Symétrique)

  * **Action :** Chiffrement binaire du *shellcode* original en utilisant la clé définie par la macro `#define XOR_KEY "maClé"`.
  * **But :** Rendre les octets binaires illisibles et briser toute signature binaire statique.
  * **Fonction :** `xor_encode`

### 2\. Base64 (Encodage Binaire-Texte)

  * **Action :** Conversion des données binaires (le résultat XORé) en une chaîne de caractères ASCII.
  * **But :** S'assurer que le *payload* encodé final ne contienne aucun caractère non imprimable ou nul (`\x00`), ce qui pourrait perturber le code C ou les systèmes de transport.
  * **Fonction :** `base64_encode`

### 3\. ROT13 (Substitution de Caractères)

  * **Action :** Décalage de 13 positions de toutes les lettres de la chaîne Base64.
  * **But :** Ajouter une couche d'obscurcissement textuel supplémentaire.
  * **Fonction :** `rot13_encode`

### 4\. UUencode Simplifié (Encodage Binaire-Texte)

  * **Action :** Conversion finale de la chaîne textuelle (résultat ROT13) en un format de type UUencode.
  * **But :** Obscurcir la chaîne de caractères finale et masquer le motif Base64/ROT13.
  * **Fonction :** `uuencode`

-----

## Robustesse et Conception

  * **Gestion de la Mémoire :** Le programme inclut des vérifications d'erreur pour les échecs d'allocation mémoire (`malloc`) pour garantir la robustesse.
  * **Sécurité :** Après avoir généré la chaîne encodée, l'intégralité du tableau `shellcode` (qui contient la version XORée sensible) est effacée de la mémoire de la pile à l'aide de `memset`.

 
