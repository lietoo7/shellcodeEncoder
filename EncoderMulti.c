#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Fonction pour encoder un shellcode avec XOR
void xor_encode(char *data, char *key, int len) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key[i % strlen(key)];
    }
}

// Fonction pour encoder un shellcode avec Base64
void base64_encode(char *data, int len) {
    static char base64_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    char *encoded_data = (char *)malloc((len * 4 / 3) + 4);
    int encoded_len = 0;
    int i = 0;

    while (i < len) {
        int value = 0;
        for (int j = 0; j < 3 && i < len; j++) {
            value |= (unsigned char)data[i++] << (8 * (2 - j));
        }

        for (int j = 0; j < 4; j++) {
            if (i < len || j < 3) {
                encoded_data[encoded_len++] = base64_chars[(value >> (6 * (3 - j))) & 0x3F];
            } else {
                encoded_data[encoded_len++] = '=';
            }
        }
    }

    encoded_data[encoded_len] = '\0';

    // Remplace le contenu de data par l'encodage base64
    strcpy(data, encoded_data);
    free(encoded_data);
}

// Fonction pour encoder un shellcode avec ROT13
void rot13_encode(char *data, int len) {
    for (int i = 0; i < len; i++) {
        if (data[i] >= 'a' && data[i] <= 'z') {
            data[i] = 'a' + (data[i] - 'a' + 13) % 26;
        } else if (data[i] >= 'A' && data[i] <= 'Z') {
            data[i] = 'A' + (data[i] - 'A' + 13) % 26;
        }
    }
}

// Fonction pour encoder un shellcode avec UUencode
void uuencode(char *data, int len) {
    char *uuencoded_data = (char *)malloc(len * 2);
    int uuencoded_len = 0;

    uuencoded_data[uuencoded_len++] = 'M'; // début de l'encodage

    for (int i = 0; i < len; i += 3) {
        int value = 0;
        for (int j = 0; j < 3 && i < len; j++) {
            value |= (unsigned char)data[i + j] << (8 * (2 - j));
        }

        for (int j = 0; j < 4; j++) {
            if (i < len || j < 3) {
                uuencoded_data[uuencoded_len++] = ((value >> (6 * (3 - j))) & 0x3F) + ' ';
            } else {
                uuencoded_data[uuencoded_len++] = '`'; // caractère spécial pour la fin
            }
        }
    }

    uuencoded_data[uuencoded_len] = '\0';

    // Remplace le contenu de data par l'encodage uuencode
    strcpy(data, uuencoded_data);
    free(uuencoded_data);
}

// Pour l'encodage AES, nous utiliserons une version simplifiée
// avec openssl, car implementer AES de A à Z est complexe.
// Assurez-vous d'avoir openssl installé et lié.
// #include <openssl/aes.h>
// void aes_encode(char *data, int len, char *key) {
//     // Exemple simplifié, nécessite une clé de 16, 24 ou 32 octets.
//     unsigned char aes_key[32];
//     strcpy((char *)aes_key, key);
//     AES_KEY aes_enc;
//     AES_set_encrypt_key(aes_key, 128, &aes_enc); // 128 bits (16 octets)

//     unsigned char *encrypted_data = (unsigned char *)malloc(len);
//     AES_cbc_encrypt(data, encrypted_data, len, &aes_enc, NULL, AES_ENCRYPT);

//     // Remplace le contenu de data par l'encodage AES
//     memcpy(data, encrypted_data, len);
//     free(encrypted_data);
// }

// Fonction pour combiner plusieurs encodages
void combine_encodings(char *shellcode, int len) {
    char key[] = "maClé";
    xor_encode(shellcode, key, len);
    base64_encode(shellcode, len);
    rot13_encode(shellcode, len);
    uuencode(shellcode, len);
    aes_encode(shellcode, len, key);
}

int main() {
    char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05";
    int len = strlen((char *)shellcode);

    printf("Shellcode original : ");
    for (int i = 0; i < len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    combine_encodings(shellcode, len);

    printf("Shellcode encodé : ");
    for (int i = 0; i < len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    return 0;
}
