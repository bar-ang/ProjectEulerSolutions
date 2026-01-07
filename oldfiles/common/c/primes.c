#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#define BYTELEN 8
typedef unsigned char byte;

int get_bit(byte* mem, int pos)
{
    byte block = mem[pos / BYTELEN];
    int loc = pos % BYTELEN;
    return (block & (1 << loc)) != 0;
}

void set_bit(byte* mem, int pos, int v)
{
    byte* block = mem + (pos / BYTELEN);
    int loc = pos % BYTELEN;
    if (v) {
        *block |= (1 << loc);
    } else {
        *block &= ~(1 << loc);
    }
}

void prime_sieve(byte* mem, size_t mem_size)
{
    int num_bits = 2 * mem_size * BYTELEN + 3;
    memset(mem, ~0, mem_size);

    unsigned int p = 3;
    printf("starting...\n");
    while(p*p <= num_bits) {
        if (get_bit(mem, p)) {
            for (unsigned int i = p*p; i < num_bits; i += p) {
                set_bit(mem, (i-3)/2, 0);
            }
        }
        p+=2;
    }
}

int create_file(char *filepath, unsigned int size_kb) {
    char buf[1024];
    
    int urandom = open("/dev/urandom", O_RDONLY);
    if (urandom < 0) {
        printf("Could not open /dev/urandom\n");
        return -1;
    }

    int fd = open(filepath, O_RDWR | O_CREAT | O_TRUNC, 0777);
    if(fd < 0){
        printf("could not create file '%s'\n", filepath);
        return -1;
    }

    for (unsigned int i = 0; i < size_kb; i++) {
        ssize_t nread = read(urandom, buf, sizeof(buf));
        if (nread < sizeof buf) {
            printf("Failed to read from /dev/urandom\n");
            return -1;
        }

        ssize_t  nwritten = write(fd, buf, sizeof(buf));
        if (nwritten < sizeof buf) {
            printf("Failed to write to %s\n", filepath);
            return -1;
        }
    }

    return fd;
}

int main(int argc, char *argv[]){   
    if(argc < 2){
        printf("File path not mentioned\n");
        exit(0);
    }

    const char *filepath = argv[1];
    printf("creating file %s\n", filepath);
    int fd = create_file(argv[1], 2);
    if (fd < 0) {
        printf("Failed to create File\n");
        exit(0);
    }

    struct stat statbuf;
    int err = fstat(fd, &statbuf);
    if(err < 0){
         printf("could not stat file '%s'\n", filepath);
         exit(2);
    }

    char *ptr = mmap(NULL,statbuf.st_size,
                 PROT_READ|PROT_WRITE,MAP_SHARED,fd,0);
    if(ptr == MAP_FAILED){
        printf("Mapping Failed\n");
        return 1;
    }
    close(fd);

    printf("sieving %s\n", filepath);
    prime_sieve(ptr, statbuf.st_size);
    
    err = munmap(ptr, statbuf.st_size);
    if(err != 0){
         printf("UnMapping Failed\n");
         return 1;
    }

     printf("DONE!\n");
     return 0;
}