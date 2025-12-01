#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void base64_encode(char *data, int len) {
    static char base64_chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    char *encoded_data = (char *)malloc(((len + 2) / 3) * 4 + 1);

    int i = 0, j = 0;
    while (i < len) {
        int octet_1 = (i < len) ? data[i++] : 0;
        int octet_2 = (i < len) ? data[i++] : 0;
        int octet_3 = (i < len) ? data[i++] : 0;

        int sextet_1 = (octet_1 & 0xfc) >> 2;
        int sextet_2 = ((octet_1 & 0x03) << 4) + ((octet_2 & 0xf0) >> 4);
        int sextet_3 = ((octet_2 & 0x0f) << 2) + ((octet_3 & 0xc0) >> 6);
        int sextet_4 = octet_3 & 0x3f;

        encoded_data[j++] = base64_chars[sextet_1];
        encoded_data[j++] = base64_chars[sextet_2];
        if (i < len + 1) {
            encoded_data[j++] = '=';
        } else {
            encoded_data[j++] = base64_chars[sextet_3];
        }
        if (i < len) {
            encoded_data[j++] = base64_chars[sextet_4];
        } else {
            encoded_data[j++] = '=';
        }
    }
    encoded_data[j] = '\0';

    printf("Shellcode encodé en Base64 : %s\n", encoded_data);

    free(encoded_data);
}

int main() {
    char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9a\xe8\x46\x0c\x00\x00\x53\x54\x5f\x52\x57\x59\x41\x50\x0f\x05";
    int len = strlen((char *)shellcode);

    base64_encode(shellcode, len);

   
