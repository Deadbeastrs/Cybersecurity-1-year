CC           = gcc
INC_DIR      = include
CFLAGS       = -g -O0 -Wall -msse2 -msse -march=native -maes -I$(INC_DIR)
OBJCOPY      = objcopy
LDLIBS 		 = -lssl -lcrypto 
DEPS 		 = mtwister.h speed_tools.h

.SILENT:
.PHONY:  clean

GENERATOR_CODE_SOURCE= generator.c
GENERATOR_CODE_OBJS= $(GENERATOR_CODE_SOURCE:.c=.o)

KEY_CODE_SOURCE= key_gen.c
KEY_CODE_OBJS= $(KEY_CODE_SOURCE:.c=.o)

all: randgen rsagen

randgen:  $(GENERATOR_CODE_OBJS)
			$(LINK.c) -o $@ $(GENERATOR_CODE_OBJS) $(LDLIBS)

rsagen: $(KEY_CODE_OBJS) 
		$(LINK.c) -o $@ $(KEY_CODE_OBJS) $(LDLIBS)

clean:
	rm randgen $(GENERATOR_CODE_OBJS)
	rm rsagen $(KEY_CODE_OBJS)

	
