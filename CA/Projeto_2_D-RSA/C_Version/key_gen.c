
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/bn.h>
#include <openssl/rand.h>

void printBigNum(BIGNUM* p){
	char * number_str1 = BN_bn2dec(p);
  	
	printf("%s\n", number_str1);
}

void nextSafePrime(BIGNUM *num, BIGNUM *res){
	BIGNUM *temp = BN_new();
	BIGNUM *temp1 = BN_new();
	BN_CTX* ctx = BN_CTX_new();
	BIGNUM *value2 = BN_new();
	BN_dec2bn( &value2, "2" );
	BN_copy(temp,num);
	BN_add(temp,temp,BN_value_one());
	while(!BN_is_prime_ex(temp,64,ctx,NULL) || !BN_is_prime_ex(temp1,64,ctx,NULL)){
		BN_add(temp,temp,BN_value_one());
		BN_mul(temp1,temp,value2,ctx);
		BN_add(temp1,temp1,BN_value_one());
	}
	BN_copy(res,temp);
	BN_free(temp);
	BN_free(temp1);
	BN_free(value2);
	BN_CTX_free(ctx);
}

int generate_key(uint8_t* rawSeed){
	
	RSA				*r = NULL;
	BIGNUM			*bne = NULL;
	BIO				*bp_public = NULL, *bp_private = NULL;

	unsigned long	e = RSA_F4;

	BIGNUM *d,*e1,*p,*q,*n,*z,*temp1,*temp2;
	BIGNUM *dmp1 = BN_new ();
	BIGNUM *dmq1 = BN_new ();
	BIGNUM *iqmp = BN_new ();
	BIGNUM *num1 = BN_new();
	BIGNUM *seed = BN_new();
	BIGNUM *seed2 = BN_new();
	BN_CTX *ctx;
	//Bytes to Hex char*
	char hexArray[128];
	char hexTemp[3];
	for(int k=0;k<64;k++){
		sprintf(hexTemp,"%02x",rawSeed[k]);
		memcpy(hexArray + k*2,hexTemp,2);
	}
	BN_dec2bn( &num1, "1" );
	BN_hex2bn( &seed, hexArray );
	ctx = BN_CTX_new();
	p = BN_new();
	q = BN_new();
	d = BN_new();
	n = BN_new();
	e1 = BN_new();
	dmp1 = BN_new();

	BN_set_word(e1, RSA_F4);

	BN_set_bit(seed,511);
	BN_set_bit(seed,510);

	nextSafePrime(seed,p);

	BN_copy(seed2,p);
	BN_set_bit(seed2,511);
	BN_set_bit(seed2,510);

	nextSafePrime(seed2,q);

	temp1 = BN_new();

	temp2 = BN_new();

	BN_sub(temp1,p,num1);

	BN_sub(temp2,q,num1);

	z = BN_new();

	BN_mul(z,temp1,temp2,ctx);

	BN_mod_inverse(d,e1,z,ctx);
	
	BN_mul(n,p,q,ctx);
	
	BN_mod (dmp1, d, temp1, ctx);
	/* dmq1 = d mod (q-1) */
	BN_mod (dmq1, d, temp2, ctx);
	/* iqmp = q^-1 mod p */
	BN_mod_inverse (iqmp, q, p, ctx);
	// 1. generate rsa key
	bne = BN_new();
	BN_set_word(bne,e);

	r = RSA_new();
	
	RSA_set0_key(r,n,e1,d);
	RSA_set0_factors(r,p,q);
	RSA_set0_crt_params(r, dmp1, dmq1, iqmp);
	
	EVP_PKEY *pkey = EVP_PKEY_new();
	EVP_PKEY_set1_RSA(pkey, r);

	// 2. save public key
	
	bp_public = BIO_new_file("public.pem", "w+");
	
	PEM_write_bio_PUBKEY(bp_public,pkey);
	
	
	// 3. save private key
	bp_private = BIO_new_file("private.pem", "w+");
	PEM_write_bio_PrivateKey(bp_private,pkey, NULL, NULL, 0, NULL, NULL);


	// 4. free

	BIO_free_all(bp_public);
	BIO_free_all(bp_private);
	RSA_free(r);

	return 1;
}

int main(int argc, char* argv[]) 
{
	uint8_t buffer[64];
	memset(buffer,0,64);
	read(STDIN_FILENO, buffer, 64);
	generate_key(buffer);
	return 0;
}