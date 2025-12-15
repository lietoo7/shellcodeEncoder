# Base64 Encoder
1.  Le but du projet.
2.  Comment le compiler et l'exécuter.
3.  Une brève explication du fonctionnement de l'encodage Base64 dans ce contexte.

## 📝 README: Encodeur Base64 de Shellcode en C

### 🚀 1. Aperçu du Projet

Ce projet implémente une fonction simple et auto-contenue en langage **C** pour effectuer l'encodage **Base64** de données binaires arbitraires, spécifiquement un "shellcode".

L'objectif principal est de démontrer comment un shellcode (qui contient souvent des octets nuls `\x00`) peut être transformé en une chaîne de caractères ASCII imprimables, ce qui le rend plus facile à manipuler ou à transmettre dans des environnements qui n'aiment pas les octets nuls (comme certaines chaînes de bases de données ou les arguments de ligne de commande).

### ⚙️ 2. Compilation et Exécution

#### 2.1 Prérequis

  * Un compilateur C (par exemple, GCC).

#### 2.2 Compilation

Enregistrez le code source (incluant les corrections) sous un nom de fichier comme `base64_encoder.c`.

Compilez le fichier en utilisant GCC :

```bash
gcc base64_encoder.c -o base64_encoder
```

#### 2.3 Exécution

Exécutez l'exécutable généré :

```bash
./base64_encoder
```

**Sortie attendue :**

```
Longueur des données binaires (shellcode) : 21 octets
Shellcode encodé en Base64 : M8BIu9Ga6EZMDAA1Vn9SV1lBUA8F
```

-----

### 💡 3. Fonctionnement de l'Encodage Base64

L'encodage Base64 est un schéma qui convertit des données binaires en une séquence de caractères ASCII.

#### Principe de Conversion

Le processus se déroule par blocs :

  * **3 octets d'entrée (3 \* 8 bits = 24 bits)** sont lus.
  * Ces 24 bits sont divisés en **4 groupes de 6 bits (4 \* 6 bits = 24 bits)**.
  * Chaque groupe de 6 bits, appelé **sextet**, est mappé à un caractère dans l'alphabet Base64 (64 caractères, $2^6$ possibilités).

#### Gestion des Données Binaires (`\x00`)

L'une des fonctions clés de ce programme est de gérer les données binaires (le shellcode) qui peuvent contenir des octets nuls (`\x00`).

La fonction `main` contourne le problème de la fonction standard `strlen` (qui s'arrêterait au premier `\x00`) en calculant la longueur réelle du tableau avec :

```c
int len = sizeof(shellcode) - 1;
```

Cela garantit que le shellcode complet est encodé, même s'il contient des octets nuls.

#### Remplissage (Padding)

Si la longueur des données binaires n'est pas un multiple de 3, le caractère de remplissage **`=`** est ajouté à la fin de la sortie pour compléter le dernier bloc de 4 caractères :

| Longueur des données | Caractères de sortie | Remplissage |
| :---: | :---: | :---: |
| Multiple de 3 | N/A | Aucun |
| Reste 2 octets | 3 caractères Base64 | Un `=` final |
| Reste 1 octet | 2 caractères Base64 | Deux `==` finaux |

-----

### ⚠️ 4. Avertissement

Ce code est fourni à des fins **éducatives et de démonstration** uniquement (sécurité offensive, étude de l'encodage binaire, etc.). Veuillez l'utiliser de manière responsable et uniquement sur des systèmes où vous avez l'autorisation explicite d'effectuer des tests.

-----

Voulez-vous ajouter une section spécifique, comme des instructions détaillées sur la façon d'intégrer cette fonction dans un projet plus vaste ?
