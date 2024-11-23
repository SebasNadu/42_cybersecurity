#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
	char input[64];
	const char *password = "__stack_check";

	printf("Please enter key: ");
	scanf("%63s", input);
	if (!strcmp(input, password)) {
			printf("Good job.\n");
	} else {
			printf("Nope.\n");
	}
	return 0;
}
