# vecotor容量增长测试

> 没有废话直接上代码和测试结果

## test.cpp

```
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main()
{
        int capacity = 0;
        vector<int> v1;
        while(capacity < 524288)
        {
                if(capacity != v1.capacity())
                {
                        cout << capacity << endl;
                        capacity = v1.capacity();
                }
                v1.push_back(1);
        }
        return 0;
}
```

## 运行结果

```
[pip@localhost 测试Vector内存增长]$ ./test_vector 
0
1
2
4
8
16
32
64
128
256
512
1024
2048
4096
8192
16384
32768
65536
131072
262144
[pip@localhost 测试Vector内存增长]$ 
```

## 总结

> 从运行结果可以看出，vector的增长每次增加为之前的两倍，emmm就这样，结论总是倍简单。

## 测试环境

>g++版本
>
>>Using built-in specs.
>>COLLECT_GCC=g++
>>COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.8.5/lto-wrapper
>>Target: x86_64-redhat-linux
>>Configured with: ../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-initfini-array --disable-libgcj --with-isl=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/isl-install --with-cloog=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/cloog-install --enable-gnu-indirect-function --with-tune=generic --with-arch_32=x86-64 --build=x86_64-redhat-linux
>>Thread model: posix
>>gcc version 4.8.5 20150623 (Red Hat 4.8.5-16) (GCC) 
>
>系统内核
>
>> Linux localhost.localdomain 3.10.0-514.el7.x86_64 #1 SMP Wed Oct 19 11:24:13 EDT 2016 x86_64 x86_64 x86_64 GNU/Linux

