#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>

void ___syscall_malloc()
{
    puts("Nope.");
    exit(1);
}

int64_t ____syscall_malloc()
{
    return puts("Good job.");
}

int main(int argc, char ** argv, char ** envp) {
    bool stop;
    int i;
    unsigned long len;
    long j;
    int c;
    char var_14;
    char input[24];
    char result[9];
    char tmp[4];

    printf("Please enter key: ");
    i = scanf("%23s", input);
    if (!(i == 1)) {
        ___syscall_malloc();
    }
    else if (!(input[1] == 50)) {
        ___syscall_malloc();
    }
    else if (!(input[0] == 52)) {
        ___syscall_malloc();
    }
    else {
        fflush(stdin);
        memset(result, 0, 9);
        result[0] = '*';
        j = 2;
        i = 1;
        while (true) {
            len = strlen(result);
						stop = false;
            if (len < 8) {
                len = strlen(input);
                stop = j < len;
            }
            if ((stop & 1) == 0) {
                break;
            }
            tmp[0] = input[j];
            tmp[1] = input[j + 1];
            tmp[2] = input[j + 2];
            tmp[3] = 0;
            c = atoi(tmp);
            result[i] = c;
            j += 3;
            i++;
        }
        result[i] = 0x0;
        i = strcmp(result, "********");
        switch(i) {
        case 0:
            ____syscall_malloc();
            return 0;
        case 1:
            ___syscall_malloc();
            break;
        case 2:
            ___syscall_malloc();
            break;
        case 3:
            ___syscall_malloc();
            break;
        case 4:
            ___syscall_malloc();
            break;
        case 5:
            ___syscall_malloc();
            break;
        case 115:
            ___syscall_malloc();
            break;
        case 0xfffffffe:
            ___syscall_malloc();
            break;
        case 0xffffffff:
            ___syscall_malloc();
            break;
        default:
            ___syscall_malloc();
        }
    }
}
