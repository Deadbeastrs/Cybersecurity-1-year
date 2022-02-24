#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <mtwister.h>
#include <speed_tools.h>
#include <fcntl.h>
#include <unistd.h>

void print_array(unsigned char *a,int array_length){
    int i;
    for(i=0;i<array_length;i++){
        printf("%d,",(unsigned char) *a);
        a++;          //for incrementing the position of array.
    }
    printf("\n");
}


unsigned long concatenate(unsigned long x, unsigned long y) {
    unsigned pow = 10;
    while(y >= pow)
        pow *= 10;
    return x * pow + y;        
}

int compareBuffers(unsigned char* x,int sizex,unsigned char* y,int sizey){
    if(sizex != sizey){
        return 0;
    }
    for(int i=0;i<sizex;i++){
        if(x[i] != y[i]){
            return 0;
        }
    }
    return 1;
}

void genConfusionPattern(unsigned char* confusionString,int confusionStringLen, unsigned char* confusionPattern){
    int seed = 0;
    for(int i=0;i<confusionStringLen;i++){
        seed = concatenate(seed,confusionString[i]) % 2147483647;
    }
    init_genrand(seed);
    for(int i=0;i<confusionStringLen;i++){
        confusionPattern[i] = genrand_int32() % 256;
    }
}

int startGenerator(char* password,int passLen, unsigned char* confusion_string,int confusion_stringLen, int iter){
    unsigned char bootstrap_seed[16];
    int i;
    memset((void*)bootstrap_seed,0,16);
    unsigned char confusionPattern[confusion_stringLen];
    PKCS5_PBKDF2_HMAC_SHA1(password,passLen,(unsigned char*) confusion_string,confusion_stringLen,iter,16,(unsigned char*) bootstrap_seed);

    unsigned long long seed = 0;
    
    for(i=0;i<16;i++){
        seed = concatenate(seed,bootstrap_seed[i]) % 2147483647;
    }
    
    genConfusionPattern(confusion_string,confusion_stringLen,confusionPattern);

    unsigned char buffer[confusion_stringLen];
    int temp = 0;
    //printf("Working");
    fflush(stdout);
    
    for(int p=0;p<iter;p++){
        init_genrand(seed);
        while(1){
            buffer[temp] = genrand_int32() % 256;
            if(compareBuffers(buffer,confusion_stringLen,confusionPattern,confusion_stringLen)){
                seed = 0;
                for(int pi=0;pi<16;pi++){
                    seed = concatenate(seed,genrand_int32() % 256) % 2147483647;
                }
                //print_array(confusionPattern,confusion_stringLen);
                //print_array(buffer,confusion_stringLen);
                break;
                
            }
            temp++;
            if(temp == confusion_stringLen){
                temp = 0;
            }
        }
    }
    return 0;
}

int main(int argc, char const *argv[])
{    
    
    if(argc != 4 && argc != 2){
        printf("Usage: ./randgen password confusion_string iter_count | ./randgen speedtest \n");
        exit(-1);
    }
    
    char password[500];
    unsigned char confusion_string[500];
    
    int iter;
    long result;
    if(argc == 2 && strcmp(argv[1],"speedtest") == 0){
        struct timespec encTime;
        unsigned long long temp_time;
        int randomData = open("/dev/random", O_RDONLY);
        read(randomData, password, 64);
        printf("\n**Speedtest**\n");
        printf("Testing with a random 64 byte password\n\n");
        printf("%-25s%-20s%-20s\n", "Confusion String Size", "Iterations", "Time (ns)");
        for(int cs = 1; cs < 4; cs++){
            for(int it = 1; it < 20; it++){
                memset(confusion_string,0,500);
                read(randomData, confusion_string, cs);
                encTime = timer_start();
                startGenerator(password,64,confusion_string,cs,it);
                temp_time = timer_end(encTime);
                int testInteger = 0;
                printf("%-25d%-20d%-20lld\n",cs,it, temp_time);
                fflush(stdout);
            }
        }
        close(randomData);
    }
    else if(argc == 4){
        strcpy(password,argv[1]);
        strcpy(confusion_string,argv[2]);
        iter = atoi(argv[3]);
        startGenerator(password,strlen(password),confusion_string,strlen(confusion_string),iter);
        for(int i=0;i<16;i++){
            result = genrand_int32();
            fwrite(&result, 1, 4, stdout);
        }
    }
    else{
        printf("Usage: ./randgen password confusion_string iter_count | ./randgen speedtest \n");
        exit(-1);
    }
    
    
    return 0;

}
