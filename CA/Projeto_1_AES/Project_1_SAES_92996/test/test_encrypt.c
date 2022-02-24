#include "../encrypt.h"

int main(int argc, char *argv[])
{   
    if(argc < 2){
        printf("Usage: ./encrypt key1 key2\n");
        exit(-1);
    }

    uint8_t hex_output[4112];
    int final_size;
    char report[4096];

    scanf("%[^\n]%*c", report); // remove last \n
    
    uint8_t key1[16];
    uint8_t key2[16];
    
    if(argc == 2){
        generateKeys_enc(argv[1],"0",key1,key2);
        setup_encrypt(key1,key2);
        encrypt_aes((unsigned char*) report,strlen(report),&final_size,hex_output);
    }else{
        generateKeys_enc(argv[1],argv[2],key1,key2);
        setup_encrypt(key1,key2);
        encrypt_s_aes((unsigned char*) report,strlen(report),&final_size,hex_output);
    }
    // Print result
    for (int i=0; i<final_size;i++){
        printf("%02x",hex_output[i]);
    }
    return 0;
}