#include "encrypt.h"

#include "aes.h"
#include "pkcs7_padding.h"

#define KEY_LEN 16

void setup_encrypt(uint8_t* key1,uint8_t* key2){
    SetKey(key1);
    Set_S_Key(key2);
}

void generateKeys_enc(char* text1,char* text2, uint8_t* key1, uint8_t* key2){
    const unsigned char salt = 0;
    PKCS5_PBKDF2_HMAC_SHA1(text1,-1,&salt,1,1000,KEY_LEN,key1);
    PKCS5_PBKDF2_HMAC_SHA1(text2,-1,&salt,1,1000,KEY_LEN,key2);
}

void encrypt_s_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray)
{  
    uint32_t i;
    uint8_t temparrayin[16];
    uint8_t temparrayout[16];                        

    uint32_t dlen = len;
    
    //Proper Length of report
    uint32_t dlenu = dlen;
    if (dlen % 16) {
        dlenu += 16 - (dlen % 16);
    }else{
        dlenu += 16;
    }

    // Make the uint8_t arrays
    uint8_t hexarray[dlenu];
    
    // Copy report to array with size ready for padding
    memcpy(hexarray,report,len);
    pkcs7_padding_pad_buffer( hexarray, dlen, sizeof(hexarray), 16 );    

    // Process one block at a time
    for(i=0;i<(dlenu/16);i++){
        memcpy(temparrayin,hexarray+(i*16),16);
        NI_AES128_ECB_encrypt(temparrayin,temparrayout);
        memcpy((resarray)+(i*16),temparrayout,16);
    }
    // Return final size
    *enc_len = dlenu;
}

void encrypt_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray)
{  
    uint32_t i;
    uint8_t temparrayin[16];
    uint8_t temparrayout[16];                        

    uint32_t dlen = len;
    
    //Proper Length of report
    uint32_t dlenu = dlen;
    if (dlen % 16) {
        dlenu += 16 - (dlen % 16);
    }else{
        dlenu += 16;
    }

    // Make the uint8_t arrays
    uint8_t hexarray[dlenu];
    
    // Copy report to array with size ready for padding
    memcpy(hexarray,report,len);
    pkcs7_padding_pad_buffer( hexarray, dlen, sizeof(hexarray), 16 );    
    // Process one block at a time
    for(i=0;i<(dlenu/16);i++){
        memcpy(temparrayin,hexarray+(i*16),16);
        AES128_ECB_encrypt(temparrayin,temparrayout);
        memcpy((resarray)+(i*16),temparrayout,16);
    }
    // Return final size
    *enc_len = dlenu;
}

void encrypt_openssl_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray, AES_KEY* wctx)
{  
    uint32_t i;
    uint8_t temparrayin[16];
    uint8_t temparrayout[16];                        

    uint32_t dlen = len;
    
    //Proper Length of report
    uint32_t dlenu = dlen;
    if (dlen % 16) {
        dlenu += 16 - (dlen % 16);
    }else{
        dlenu += 16;
    }

    // Make the uint8_t arrays
    uint8_t hexarray[dlenu];
    
    // Copy report to array with size ready for padding
    memcpy(hexarray,report,len);
    pkcs7_padding_pad_buffer( hexarray, dlen, sizeof(hexarray), 16 );    
    // Process one block at a time
    for(i=0;i<(dlenu/16);i++){
        memcpy(temparrayin,hexarray+(i*16),16);
        AES_encrypt(temparrayin, temparrayout, wctx);
        memcpy((resarray)+(i*16),temparrayout,16);
    }
    // Return final size
    *enc_len = dlenu;
}