#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <unistd.h>

void red () {
  printf("\033[1;31m");
}

void blue () {
  printf("\033[0;34m");
}

void yellow () {
  printf("\033[1;33m");
}

void green () {
  printf("\033[0;32m");
}

void reset () {
  printf("\033[0m");
}
int main(int argc, char const *argv[])
{
    setuid(1000); // Set uid as jovemgui to acess files
    char result[4096];
    FILE *fp;
    /* Open the command for reading. */
    fp = popen("/bin/cat to_do.txt", "r"); //Full Path
    if (fp == NULL) {
        printf("Failed to run command\n" );
        exit(1);
    }
    blue();
    printf("JovemGuilhas personal software\n");
    reset();
    printf("\nReading to_do list\n-------------\n\n");
    /* Read the output a line at a time - output it. */
    while (fgets(result, sizeof(result), fp) != NULL) {
        if(strcmp(result,"Important:\n") == 0){
            red();
        }
        if(strcmp(result,"SemiImportant:\n") == 0){
            yellow();
        }
        if(strcmp(result,"NotImportant:\n") == 0){
            green();
        }
        printf("%s", result);
    }
    reset();
    printf("\n\n");
    /* close */
    pclose(fp);
    printf("------------\n");
    printf("\nSystem information: \n");

    system("/bin/uname"); //Full Path

    printf("\n");
    return 0;
}
