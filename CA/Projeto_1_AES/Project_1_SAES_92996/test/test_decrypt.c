#include "../decrypt.h"
#include <stdlib.h>     /* strtol */

int main(int argc, char *argv[])
{   
    if(argc < 2){
        printf("Usage: ./decrypt key1 key2\n");
        exit(-1);
    }

    char encoded_text[8224];

    scanf("%[^\n]%*c", encoded_text); // remove last \n 

    uint8_t hex_input[strlen(encoded_text) / 2];
    
    uint8_t output[4112];
    
    memset( hex_input, 0, strlen(encoded_text) / 2 );

    int finalSize;
    char tempP[3];
    tempP[2] = '\0';
    int c = 0;
    int i = 0;

    // Convert from hex char array to hex array
    int dlen = strlen(encoded_text);
    for(i=0;i<dlen-1;i=i+2){
        tempP[0] = encoded_text[i];
        tempP[1] = encoded_text[i+1];
        hex_input[c] = (uint8_t)strtol(tempP, NULL, 16);
        c++;
    }

    uint8_t key1[16];
    uint8_t key2[16];
    // Normal AES or S-AES
    if(argc == 2){
        generateKeys_dec(argv[1],"0",key1,key2);
        setup_decrypt(key1,key2);
        decrypt_aes(hex_input,strlen(encoded_text)/2,&finalSize,output);
    }else{
        generateKeys_dec(argv[1],argv[2],key1,key2);
        setup_decrypt(key1,key2);
        decrypt_s_aes(hex_input,strlen(encoded_text)/2,&finalSize,output);
    }
    // Print result
    for (i=0; i<finalSize;i++){
        printf("%c",output[i]);
    }

    return 0;
}