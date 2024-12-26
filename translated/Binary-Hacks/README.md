# Binary Hacks

## Use od to dump the binary file 

 Hexadecimal dump: 

```sh
$ od -t x1 -A x /etc/ld.so .cache | head -5
000000 6c 64 2e 73 6f 2d 31 2e 37 2e 30 00 dc 0b 00 00
000010 03 03 00 00 b8 1c 01 00 cc 1c 01 00 03 03 00 00
000020 e9 1c 01 00 00 1d 01 00 03 03 00 00 20 1d 01 00
000030 36 1d 01 00 03 03 00 00 55 1d 01 00 65 1d 01 00
000040 03 03 00 00 7e 1d 01 00 8b 1d 01 00 03 03 00 00
```

 displays the ASCII code: 

```sh
$ od -t x1z -A x /etc/ld.so.cache | head -5
000000 6c 64 2e 73 6f 2d 31 2e 37 2e 30 00 dc 0b 00 00 >ld.so-1.7.0....<
000010 03 03 00 00 b8 1c 01 00 cc 1c 01 00 03 03 00 00 >............< 
000020 e9 1c 01 00 00 1d 01 00 03 03 00 00 20 1d 01 00 >............ ...<
000030 36 1d 01 00 03 03 00 00 55 1d 01 00 65 1d 01 00 >6.......U.. .e...<
000040 03 03 00 00 7e 1d 01 00 8b 1d 01 00 03 03 00 00 >....~.....<
```

 Line break: 

```sh
$ od -t x1c -A x /etc/ld.so.cache | head -5
000000 6c 64 2e 73 6f 2d 31 2e 37 2e 30 00 dc 0b 00 00
 l d . s o - 1 . 7 . 0 \0 334 \v \0 \0
000010 03 03 00 00 b8 1c 01 00 cc 1c 01 00 03 03 00 00
 003 003 \0 \0 270 034 001 \0 314 034 001 \0 003 003 \0 \0
000020 e9 1c 01 00 00 1d 01 00 03 03 00 00 20 1d 01 00
```

## Static link libraries and shared libraries archive multiple object files into one file, which is called a static link library. The static link library is usually written as follows: 

```sh
$ cc -c -o foo.o foo.c
$ cc -c -o bar.o bar.c
$ ar rUuv libfoo .a libfoo.a foo.o bar.o
ar: creating libfoo.a
a - foo.o
a - bar.o
```

View the contents of the library: 

```sh
$ ar tv libfoo.a 
rw-r--r-- 1000/1000 1920 Oct 23 14: 18 2017 foo.o
rw-r--r-- 1000/1000 1920 Oct 23 14:18 2017 bar.o
```

 When linking a static library, the connector does the following: first find undefined symbols from other target files, and then read the definitions from the specified static link library A copy of the symbol's object file is added to the executable file to complete the link. 

 A static library is an archive of multiple target files, while a shared library copies multiple target files into a huge target file for sharing. Common practice for making shared libraries: 

```sh
$ cc -fPIC -c -o foo.o foo.c
$ cc -fPIC -c -o bar.o bar.c
$ cc -shared -Wl,-soname,libfoo.so.0 -o libfoo.so foo.o bar.o
```

## via ldd Check the dependencies of shared libraries

```sh
$ ldd /bin/ls
 linux-vdso.so.1 (0x00007ffe3d98a000)
 libcap.so.2 => /usr/lib/libcap. so.2 (0x00007f89f1cae000)
 libc.so.6 => /usr/lib/libc.so.6 (0x00007f89f18f7000)
 /lib64/ld-linux-x86-64.so.2 => /usr/lib64/ld-linux-x86-64.so.2 ( 0x00007f89f20d4000)
```

ldd is actually just Shell script, focusing on the environment variable LD_TRACE_LOADED_OBJECTS, setting it to 1 will have the same effect: 

```sh
$ LD_TRACE_LOADED_OBJECTS=1 /bin/ls
 linux-vdso.so.1 (0x00007ffcfc316000)% 0A libcap.so.2 => /usr/lib/libcap.so.2 (0x00007f156098f000)
 libc.so.6 => /usr/lib/libc.so.6 (0x00007f15605d8000)
 /lib64/ld-linux-x86-64.so. 2 (0x00007f1560b93000)
```

## Issues to note when linking C programs and C++ programs

Use gcc and g++ respectively to compile the following functions:

```c 
// dbg.c
#include<stdio.h>
void dbg(const char *s) {
 printf("Log: %s\n", s);
}
```

The generated symbol name is as follows: 

```sh
$ gcc -c - o dbg.o dbg.c
$ nm dbg.o | grep dbg
0000000000000000 T dbg
$ g++ -c -o dbg.o dbg.c
$ nm dbg.o | grep dbg
0000000000000000 T _Z3dbgPKc
```

In the C++ compiler, the symbol will include the function to which it belongs. Namespace information and function parameter type information. You can use C++filt for dumping, that is, inverse transformation: 

```sh
$ nm dbg.o | c++filt | grep dbg
0000000000000000 T dbg(char const*)
`` `

 Use the C compiler to compile dbg.c and then call it from a function written in C++. The following is sample.cpp: 

```cpp
// sample.cpp
extern "C" void dbg(const char *s);
int main() {
 dbg("foo"); 
 return 0;
}
```

 Compile and run: 

```sh
$ gcc -Wall -c dbg.c
$ g++ -Wall -c sample.cpp
$ g++ -o sample dbg.o sample.o
$ ./sample 
Log: foo
```

If there is no `extern "C"`, or if the type of dbg is written incorrectly, an error will occur. Therefore, you need to prepare the following file header: 

```c
// dbg.h
#ifdef __cplusplus
 extern "C" {
#endif
 void dbg(const char *s);
#ifdef __cplusplus
 }
#endif
```

The following calls C++ from C Functions, two points should be noted. The first is that C++ functions must be compiled in conjunction with C (extern "C"). The second point is that when linking, g++ must be run instead of gcc. 

```c
// gcd.h
#ifdef __cplusplus
extern "C"
#endif
int gcd(int v1, int v2);
````

` ``cpp
// gcd.cpp
#include <boost/math/common_factor.hpp>
#include "gcd.h"

extern "C" {
 int gcd(int v1, int v2) {
 return boost::math::gcd(v1, v2);
 }
}
` ``

```c
// sample.c
#include <stdio.h>
#include "gcd.h"

int main() {
 printf("gcd(%d, %d) = %d\n", 14, 35, gcd(14, 35));
 return 0; 
}
```

```sh
$ g++ -Wall -c gcd.cpp
$ gcc -Wall -c sample.c
$ g++ -o sample sample.o gcd.o
$ ./sample
```

 But there are two points to note. The first point is that C++ functions are not allowed to throw exceptions to C functions. The second point is that C functions that handle function pointers must be added during compilation. on `-fexceptions`. 

## Same-name identifier conflict during linking 

 When `.o` files are organized and linked: 

```c
// a.c
#include <stdio.h >
void func() {
 printf("func() in a.c\n");
}
```

```c
// b.c
#include <stdio.h>
void func() {
 printf("func() in b.c\n");
}
```

```c
void func ();
int main() {
 func();
 return 0;
}
```

 Compile and statically link separately. Because there are multiple `func()`, an error occurs: 

```sh
$ gcc -c a.c % 0A$ gcc -c b.c 
$ gcc -c main.c 
$ gcc -o main a.o b.o main.o
b.o: In function `func':
b.c:(.text+0x0): multiple definition of `func'
a.o:a.c:(.text+0x0): first defined here
collect2: error: ld returned 1 exit status% 0A```

A conflict occurred when merging a.o and b.o into a shared library: 

```sh
$ gcc -fPIC -c a.c
$ gcc -fPIC -c b.c
$ gcc -shared -o libfoo.so a.o b.o
b.o: In function `func':
b.c:(.text+0x0): multiple definition of ` func'
a.o:a.c:(.text+0x0): first defined here
collect2: error: ld returned 1 exit status
```

 The situation when generating the library and linking it: 

 Using ar to generate a static link library and linking a.o and b.o, no error will occur. This is because ar does not check symbols. Conflict: 

```sh
$ ar cr libfoo.a a.o b.o
$ gcc main.o libfoo.a 
$ ./a.out 
func() in a.c
$ rm libfoo.a 
$ ar cr libfoo.a b.o a.o
$ gcc main.o libfoo.a 
$ ./a.out 
func() in b.c
` `

` placed in front of `.o` will be found first, so it will be called. When a.c and b.c are generated as static link libraries respectively, there will be no conflict when linking. The same order is very important: 

```sh
$ ar cr liba.a a.o
$ ar cr libb. a b.o
$ gcc main.o liba.a libb.a 
$ ./a.out 
func() in a.c
```

 Similarly, if the dynamic link library is generated and linked separately, no error will occur: 

```sh
$ gcc -fPIC -shared -o a.so a.c
 $ gcc -fPIC -shared -o b.so b.c
$ gcc -fPIC -shared -o main.so main.c
$ gcc -o main-shared a.so b.so main.so 
$ ./a.out 
func() in a.c
```
