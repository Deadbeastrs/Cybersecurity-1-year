#ifndef _ENC_H_
#define _ENC_H_

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>
#include<openssl/aes.h>
#include<openssl/rand.h>

void encrypt_s_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray);

void encrypt_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray);

void generateKeys_enc(char* text1,char* text2, uint8_t* key1, uint8_t* key2);

void setup_encrypt(uint8_t* key1,uint8_t* key2);

void encrypt_openssl_aes(unsigned char* report,int len, int* enc_len, uint8_t* resarray, AES_KEY* wctx);
#endif //_ENC_H_