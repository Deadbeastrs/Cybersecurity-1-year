#ifndef _DEC_H_
#define _DEC_H_

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>
#include<openssl/aes.h>
#include<openssl/rand.h>

void generateKeys_dec(char* text1,char* text2, uint8_t* key1, uint8_t* key2);

void decrypt_s_aes(uint8_t* hexarray,int len,int* dec_len,uint8_t* decarray);

void decrypt_aes(uint8_t* hexarray,int len,int* dec_len,uint8_t* decarray);

void decrypt_openssl_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray, AES_KEY* wctx);

void decrypt(uint8_t* hexarray,int len,int* dec_len,uint8_t* decarray);

void setup_decrypt(uint8_t* key1,uint8_t* key2);

#endif //_DEC_H_