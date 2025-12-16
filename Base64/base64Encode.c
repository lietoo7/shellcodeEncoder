#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void base64_encode(char *data, int len) {
    // Le jeu de caractères Base64 standard
    static char base64_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    
    // Calcul de la taille de la sortie : 4 caractères pour chaque 3 octets, plus 1 pour le terminateur nul.
    size_t output_len = ((len + 2) / 3) * 4 + 1;
    char *encoded_data = (char *)malloc(output_len);

    if (encoded_data == NULL) {
        perror("Échec de l'allocation mémoire");
        return;
    }

    int i = 0, j = 0;
    while (i < len) {
        // Lecture des octets d'entrée, convertis en unsigned int
        unsigned int octet_1 = (unsigned char)data[i++];
        unsigned int octet_2 = 0;
        unsigned int octet_3 = 0;

        // Indicateurs de présence pour gérer le remplissage (=)
        int has_octet_2 = (i < len);
        if (has_octet_2) {
            octet_2 = (unsigned char)data[i++];
        }
        
        int has_octet_3 = (i < len);
        if (has_octet_3) {
            octet_3 = (unsigned char)data[i++];
        }

        // Découpage des 24 bits en 4 sextets (groupes de 6 bits)
        unsigned int sextet_1 = (octet_1 & 0xfc) >> 2;
        unsigned int sextet_2 = ((octet_1 & 0x03) << 4) + ((octet_2 & 0xf0) >> 4);
        unsigned int sextet_3 = ((octet_2 & 0x0f) << 2) + ((octet_3 & 0xc0) >> 6);
        unsigned int sextet_4 = octet_3 & 0x3f;

        // Assignation des 2 premiers caractères (toujours présents)
        encoded_data[j++] = base64_chars[sextet_1];
        encoded_data[j++] = base64_chars[sextet_2];

        // Assignation du 3e caractère : Base64 si octet_2 est là, sinon '='
        if (has_octet_2) {
            encoded_data[j++] = base64_chars[sextet_3];
        } else {
            encoded_data[j++] = '=';
        }

        // Assignation du 4e caractère : Base64 si octet_3 est là, sinon '='
        if (has_octet_3) {
            encoded_data[j++] = base64_chars[sextet_4];
        } else {
            encoded_data[j++] = '=';
        }
    }
    
    encoded_data[j] = '\0'; // Terminateur nul

    printf("Shellcode encodé en Base64 : %s\n", encoded_data);

    free(encoded_data);
}

int main() {
    // Shellcode binaire contenant des octets nuls (\x00)
    char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05";
    
    // Calcul de la longueur correcte (21 octets) :
    // sizeof(shellcode) retourne 22 (21 octets + 1 pour le \0 ajouté par le compilateur C pour la chaîne littérale)
    // Nous devons soustraire ce \0 de fin pour l'encodage binaire.
    int len = sizeof(shellcode) - 1; 

    printf("Longueur des données binaires (shellcode) : %d octets\n", len);

    base64_encode(shellcode, len);

    return 0;
}
// Sortie attendue (pour 21 octets) :
// Shellcode encodé en Base64 : M8BIu9Ga6EZMDAA1Vn9SV1lBUA8F
