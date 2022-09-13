#include <arpa/inet.h>
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/bio.h>
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <openssl/rand.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>

int main(int argc, char *argv[]) {
	int iVar1;
	FILE *local_18;
	uint local_c;
	FILE *ptr;
	ptr = fopen("aes_key.bin","wb");
	uint timestamp = 1651092844;
	srand(timestamp);
	char buffer[16];
      	memset(buffer,0,16);
        for (int in = 0; in < 16; in = in + 1) {
	    buffer[in] = rand();
	}
	fwrite(buffer,16,1,ptr);
	fclose(ptr);
}
