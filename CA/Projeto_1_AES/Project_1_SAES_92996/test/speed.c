#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>

#include "../encrypt.h"
#include "../decrypt.h"
#include "speed_tools.h"

#include<openssl/crypto.h>
#include<openssl/evp.h>
#include<openssl/aes.h>
#include<openssl/rand.h>


int main(int argc, char const *argv[])
{
    unsigned char buffer[4096];
    int fd = open("/dev/urandom", O_RDONLY);
    int sizeEnc = 0;
    int sizeDec = 0;
    uint8_t bufferEnc[4112];
    uint8_t bufferDec[4112];

    uint8_t key1[16];
    uint8_t key2[16];
    
    struct timespec encTime;
    struct timespec decTime;
    long temp_time = 0;
    long lowestTime_aes = 9999999999;
    long lowestTime_s_aes = 9999999999;

    AES_KEY wctx;
    AES_KEY wctx1;
    printf("The test will start, this process may take up to 5 minutes:\n");
    for(int i = 0; i < 100000;i++){
        // New keys
        memset(buffer,0,4096);
        memset(bufferDec,0,4096);
        read(fd, key1, 16);
        read(fd, key2, 16);

        AES_set_encrypt_key((unsigned char*) key1, 128, &wctx);

        read(fd, buffer, 4096);
        //Encryption time
        encTime = timer_start1();
        encrypt_openssl_aes(buffer,4096,&sizeEnc,bufferEnc,&wctx);
        temp_time = timer_end1(encTime);
        AES_set_decrypt_key((unsigned char*) key1, 128, &wctx1);
        //Decryption time
        decTime = timer_start1();
        decrypt_openssl_aes(bufferEnc,sizeEnc,&sizeDec,bufferDec,&wctx1);
        temp_time += timer_end1(decTime);
        //Check if the original buffer has the same result as the decrypted buffer
        if(memcmp(buffer, bufferDec, 4096) != 0){
            printf("Error! Original Buffer and Decrypted buffer are not the same!\n");
            return -1;
        }
        if(temp_time < lowestTime_aes){
            lowestTime_aes = temp_time;
        }
    }
    printf("\nNormal AES done, starting S-AES:\n");
    for(int i = 0; i < 100000;i++){
        // New keys
        memset(buffer,0,4096);
        memset(bufferDec,0,4096);
        read(fd, key1, 16);
        read(fd, key2, 16);

        setup_encrypt(key1,key2);
        read(fd, buffer, 4096);
        //Encryption time
        encTime = timer_start1();
        encrypt_s_aes(buffer,4096,&sizeEnc,bufferEnc);
        temp_time = timer_end1(encTime);
        setup_decrypt(key1,key2);     
        //Decryption time
        decTime = timer_start1();
        decrypt_s_aes(bufferEnc,sizeEnc,&sizeDec,bufferDec);
        temp_time += timer_end1(decTime);

        //Check if the original buffer has the same result as the decrypted buffer
        if(memcmp(buffer, bufferDec, 4096) != 0){
            printf("Error! Original Buffer and Decrypted buffer are not the same!\n");
            return -1;
        }
        if(temp_time < lowestTime_s_aes){
            lowestTime_s_aes = temp_time;
        }
    }
    printf("\nLowest Time for encryption and decryption of 100000 buffers of 4kb of S-AES and Openssl AES:\nS-AES:%ld ns\nAES: %ld ns\n",lowestTime_s_aes,lowestTime_aes);
    
    close(fd);

    return 0;
}
