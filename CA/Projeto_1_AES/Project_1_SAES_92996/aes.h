#ifndef _AES_H_
#define _AES_H_

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>


// #define the macros below to 1/0 to enable/disable the mode of operation.
//
// CBC enables AES128 encryption in CBC-mode of operation and handles 0-padding.
// ECB enables the basic ECB 16-byte block algorithm. Both can be enabled simultaneously.

// The #ifndef-guard allows it to be configured before #include'ing or at compile time.

#ifndef ECB
  #define ECB 1
#endif



#if defined(ECB) && ECB

void AES128_ECB_encrypt(uint8_t* input, uint8_t *output);
void AES128_ECB_decrypt(uint8_t* input, uint8_t *output);

void S_AES128_ECB_encrypt(uint8_t* input,uint8_t* output);
void S_AES128_ECB_decrypt(uint8_t* input,uint8_t* output);

void NI_AES128_ECB_encrypt(uint8_t* input, uint8_t* output_t);
void NI_AES128_ECB_decrypt(uint8_t* input, uint8_t *output_t);

void SetKey(uint8_t* key);
void Set_S_Key(uint8_t* s_key);
#endif // #if defined(ECB) && ECB

#endif //_AES_H_
