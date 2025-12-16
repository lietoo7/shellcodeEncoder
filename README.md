# shellcodeEncoder
```
#include <stdio.h>

int main(void) {
    // Fragment d'ASCII Art fourni par l'utilisateur
    const char *fragment_art[] = {
        "                        .               ",
        "                   .   .%@#.  ..        ",
        "          .:      .%@#=*@@@*+%@%.       ",
        "       =#:+@-:-.   .@@@#-.-%@@%.        ",
        "       .@*..-@*.  .:@@.     :@@:..      ",
        "     .#@%.  .#@#-@@@@=      .#@@@@.     ",
        "      .-@*-:+@-   .=@@.    .:@@:        ",
        "       = .@%.**..:.:@@@@::-@@@%:        ",
        "          ..@@+.%@%%@*:+@@@=:%@@.       ",
        "           .+@@%#@@**%-.#@*.  ..        ",
        "        .%@@@-    -@@-  ...             ",
        "          .%#.    .#@-                  ",
        "         .+@@+.   -@@@%.                ",
        "         .*+-%@@@@@* ",
        "             #@+..%@.                   ",
        "....         ...  ..                    ",
        "+==+...:...                             ",
        "+==+.......                             ",
        "++++.......                             ",
        NULL // Marqueur de fin de tableau
    };

    printf("--- Fragment d'ASCII Art ---\n");
    
    for (int i = 0; fragment_art[i] != NULL; ++i) {
        puts(fragment_art[i]);
    }
    
    return 0;
}
```
