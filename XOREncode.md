Outil d'Obfuscation Simple par XOR

### Introduction

Ce projet est une implémentation éducative et optimisée d'une technique d'obfuscation de données binaires utilisant l'opération **XOR symétrique** avec une clé répétitive (*repeating-key stream cipher*).

Son objectif principal est de démontrer :

1.  Le principe fondamental de la cryptographie symétrique (où le chiffrement et le déchiffrement utilisent la même opération).
2.  Les meilleures pratiques de programmation en C pour la manipulation de données binaires (octets nuls inclus) et l'optimisation des performances.

### Fonctionnement Technique

#### 1\. Le Principe XOR

L'opération XOR (Ou Exclusif) est son propre inverse : appliquer la même opération deux fois annule l'effet.

[Image of XOR logic gate truth table]

  * **Chiffrement :** $C = D \oplus K$
  * **Déchiffrement :** $D = C \oplus K$

Où $D$ est la donnée, $K$ est la clé, et $C$ est la donnée chiffrée.

#### 2\. Fonction `xor_encode_optimized`

La fonction utilise la clé de manière cyclique sur la séquence de données :

```c
// data[i] est chiffré/déchiffré en utilisant un caractère de la clé
data[i] ^= key[i % key_len]; 
```

### Optimisations de Performance et Robustesse

Cette version du code intègre des corrections essentielles pour améliorer sa fiabilité et son efficacité.

| Problème Original | Correction Appliquée | Bénéfice |
| :--- | :--- | :--- |
| **Erreur de Longueur (`strlen`)** | La longueur des données binaires est fixée par une constante (`SHELLCODE_LEN = 21`). | Permet de manipuler des données contenant l'octet `\x00` sans que `strlen()` n'arrête le calcul prématurément. |
| **Performance Inefficace** | La longueur de la clé (`key_len`) est calculée une seule fois avant la boucle. | Réduit la complexité de $O(N \times L)$ à $O(N)$, offrant un gain de performance significatif pour les grandes quantités de données. |
| **Gestion des Types** | Utilisation cohérente du type `size_t` pour toutes les longueurs et les indices de boucle. | Conformité aux standards C pour la gestion des tailles et suppression du risque de *integer overflow*. |

### Exemple de Sortie

```
Longueur du shellcode (Corrigée) : 21 octets
Shellcode chiffré : \x5c\xa1\x0b\xd7\x12\x33\x85\x27\x4f\x6c\xc3\xfa\x39\x3e\x11\x3b\x9a\xe8\x3d\x6e\x46
Shellcode décodé : \x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05
```

### Note de Sécurité Importante

Il est crucial de noter que le chiffrement XOR est une forme d'**obfuscation** très simple et **non une méthode de chiffrement sécurisée**.

  * **Vulnérabilité :** Si la clé est courte et répétée (comme ici), elle est extrêmement vulnérable à la **cryptanalyse par recherche d'occurrence** (*frequency analysis*), car l'attaquant peut déduire la clé en analysant les répétitions dans le texte chiffré (une technique courante en rétro-ingénierie de *malware*).
  * **Contexte :** Cette technique est principalement utilisée dans des scénarios où l'objectif est de contourner les outils de détection de signatures statiques, non pas de protéger des données sensibles contre une attaque cryptanalytique dédiée.

-----

Souhaitez-vous ajouter ou modifier une section de ce `README` avant de le finaliser ?
