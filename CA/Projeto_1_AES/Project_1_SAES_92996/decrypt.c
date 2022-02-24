#include "decrypt.h"
#include "aes.h"
#include "pkcs7_padding.h"


#define KEY_LEN 16

void setup_decrypt(uint8_t* key1,uint8_t* key2){
    SetKey(key1);
    Set_S_Key(key2);
}

void generateKeys_dec(char* text1,char* text2, uint8_t* key1, uint8_t* key2){
    const unsigned char salt = 0;
    PKCS5_PBKDF2_HMAC_SHA1(text1,-1,&salt,1,1000,KEY_LEN,key1);
    PKCS5_PBKDF2_HMAC_SHA1(text2,-1,&salt,1,1000,KEY_LEN,key2);
}

void decrypt_s_aes(uint8_t* hexarray,int len,int* dec_len,uint8_t* decarray)
{
    uint32_t i;
    uint8_t temparrayin[16];
    uint8_t temparrayout[16];

    int dlen = len;
    int dlenu = dlen;

    // Process a block at a time ad decrypt a block at a time
    for(i=0;i<((int) dlenu/16);i++){
        memcpy(temparrayin,hexarray+(i*16),16);
        NI_AES128_ECB_decrypt(temparrayin,temparrayout);
        memcpy((decarray)+(i*16),temparrayout,16);
    }

    size_t actualDataLength = pkcs7_padding_data_length( (decarray) , dlenu, 16);
    // Return actual length of decoded
    *dec_len = actualDataLength;
}

void decrypt_aes(uint8_t* hexarray,int len,int* dec_len,uint8_t* decarray)
{
    uint32_t i;
    uint8_t temparrayin[16];
    uint8_t temparrayout[16];

    int dlen = len;
    int dlenu = dlen;

    // Process a block at a time ad decrypt a block at a time
    for(i=0;i<((int) dlenu/16);i++){
        memcpy(temparrayin,hexarray+(i*16),16);
        AES128_ECB_decrypt(temparrayin,temparrayout);
        memcpy((decarray)+(i*16),temparrayout,16);
    }

    size_t actualDataLength = pkcs7_padding_data_length( (decarray) , dlenu, 16);
    // Return actual length of decoded
    *dec_len = actualDataLength;
}

void decrypt_openssl_aes(uint8_t* hexarray,int len,int* dec_len,uint8_t* decarray, AES_KEY* wctx)
{  
    uint32_t i;
    uint8_t temparrayin[16];
    uint8_t temparrayout[16];

    int dlen = len;
    int dlenu = dlen;

    // Process a block at a time ad decrypt a block at a time
    for(i=0;i<((int) dlenu/16);i++){
        memcpy(temparrayin,hexarray+(i*16),16);
        AES_decrypt(temparrayin, temparrayout, wctx);
        memcpy((decarray)+(i*16),temparrayout,16);
    }

    size_t actualDataLength = pkcs7_padding_data_length( (decarray) , dlenu, 16);
    // Return actual length of decoded
    *dec_len = actualDataLength;
}