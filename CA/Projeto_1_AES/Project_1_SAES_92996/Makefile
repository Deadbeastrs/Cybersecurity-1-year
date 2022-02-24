CC           = gcc
INC_DIR      = include
CFLAGS       = -g -O0 -Wall -msse2 -msse -fno-common -march=native -maes -I$(INC_DIR)
OBJCOPY      = objcopy
LDLIBS 		 = -lssl -lcrypto 
DEPS 		 = aes_ni.h speed_tools.h

.SILENT:
.PHONY:  clean

CODE_SOURCE= encrypt.c decrypt.c aes.c pkcs7_padding.c
CODE_OBJS= $(CODE_SOURCE:.c=.o)

TEST_SOURCE= test/test_decrypt.c
TEST_OBJS= $(TEST_SOURCE:.c=.o)

TEST1_SOURCE= test/test_encrypt.c
TEST1_OBJS= $(TEST1_SOURCE:.c=.o)

TEST2_SOURCE= test/speed.c
TEST2_OBJS= $(TEST2_SOURCE:.c=.o)

all: encrypt decrypt speed

encrypt:  $(TEST1_OBJS) $(CODE_OBJS)
	$(LINK.c)  -o $@ $(TEST1_OBJS) $(CODE_OBJS) $(LDLIBS)

decrypt:  $(TEST_OBJS) $(CODE_OBJS)
	$(LINK.c) -o $@ $(TEST_OBJS) $(CODE_OBJS) $(LDLIBS)

speed:  $(TEST2_OBJS) $(CODE_OBJS)
	$(LINK.c) -o $@ $(TEST2_OBJS) $(CODE_OBJS) $(LDLIBS)

clean:
	rm encrypt $(CODE_OBJS) $(TEST1_OBJS)
	rm decrypt $(TEST_OBJS)
	rm speed $(TES2T_OBJS)

tencrypt:  encrypt
	./encrypt

tdecrypt:  decrypt
	./decrypt

tspeed:  speed
	./speed
	
