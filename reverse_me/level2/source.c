#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void no(void) {
  puts("Nope.");
  exit(1);
}

void ok(void) {
  puts("Good job.");
  return;
}

int main(void) {
  unsigned int i_tranf;
  size_t cmp_buff_len;
  int res_val;
  bool br_cond;
  char weird[4];
  char str_buff[24];
  char cmp_buff[9];
  unsigned int i;
  int j;
  int found;

  printf("Please enter key: ");
  found = scanf("%23s", str_buff);
  if (found != 1) {
    no();
  }
  if (str_buff[1] != '0') {
    no();
  }
  if (str_buff[0] != '0') {
    no();
  }
  fflush(stdin);
  memset(cmp_buff, 0, 9);
  cmp_buff[0] = 'd';
  weird[3] = 0;
  i = 2;
  j = 1;
  while (true) {
    cmp_buff_len = strlen(cmp_buff);
    i_tranf = i;
    br_cond = false;
    if (cmp_buff_len < 8) {
      cmp_buff_len = strlen(str_buff);
      br_cond = i_tranf < cmp_buff_len;
    }
    if (!br_cond)
      break;
    weird[0] = str_buff[i];
    weird[1] = str_buff[i + 1];
    weird[2] = str_buff[i + 2];
    res_val = atoi(weird);
    cmp_buff[j] = (char)res_val;
    i = i + 3;
    j = j + 1;
  }
  cmp_buff[j] = '\0';
  res_val = strcmp(cmp_buff, "delabere");
  if (res_val == 0) {
    ok();
  } else {
    no();
  }
  return 0;
}
