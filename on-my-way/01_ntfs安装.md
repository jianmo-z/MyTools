参考文档:

https://www.cnblogs.com/magialmoon/archive/2013/05/09/3070163.html

https://askubuntu.com/questions/586308/error-mounting-dev-sdb1-at-media-on-ubuntu-14-04-lts

https://askubuntu.com/questions/47700/fix-corrupt-ntfs-partition-without-windows

# 环境

> Linux localhost.localdomain 3.10.0-514.el7.x86_64 #1 SMP Wed Oct 19 11:24:13 EDT 2016 x86_64 x86_64 x86_64 GNU/Linux



# 错误

> 当我硬盘插入系统时，却无法打开，显示需要`ntfs`挂载，所以，百度呗

# 解决

> 还好百度到了解决方案所以写出来，为后人铺路，此教程U盘也适用

```
Error mounting /dev/sdb1 at /run/media/pip/风吹过: Command-line `mount -t "ntfs" -o "uhelper=udisks2,nodev,nosuid,uid=1000,gid=1000,dmask=0077,fmask=0177" "/dev/sdb1" "/run/media/pip/风吹过"' exited with non-zero exit status 32: mount: unknown filesystem type 'ntfs'
```



## 查看下硬盘名

```
lsblk //列出所有的分区，或者通过fdisk -l、df -h也可以，不过我用这两个命令没有查看到我的硬盘



[pip@localhost ~]$ lsblk
NAME          MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda             8:0    0 465.8G  0 disk 
├─sda1          8:1    0    99M  0 part /boot/efi
├─sda2          8:2    0   128M  0 part 
├─sda3          8:3    0  99.5G  0 part 
├─sda4          8:4    0   478M  0 part 
├─sda5          8:5    0    50G  0 part 
├─sda6          8:6    0    50G  0 part 
├─sda7          8:7    0    50G  0 part 
├─sda8          8:8    0     1G  0 part /boot
└─sda9          8:9    0 214.6G  0 part 
  ├─rhel-root 253:0    0    50G  0 lvm  /
  ├─rhel-swap 253:1    0   3.9G  0 lvm  [SWAP]
  └─rhel-home 253:2    0 160.7G  0 lvm  /home
sdb             8:16   0 931.5G  0 disk 
└─sdb1          8:17   0 931.5G  0 part 


sdb1 就是我的硬盘，记住这个后面会用到，每个人的不一样
```

## 下载`ntfs-3g`包

```
wget http://tuxera.com/opensource/ntfs-3g_ntfsprogs-2013.1.13.tgz //下载ntfs包，如果下载
```

> [百度网盘连接](https://pan.baidu.com/s/1s1R95cr4iEbzdrXWXOk_eQ)

## 解压

```
tar -zxvf  ntfs-3g_ntfsprogs-2013.1.13.tgz
```

## 安装

```
cd  ntfs-3g_ntfsprogs-2013.1.13
./configure
make
make install //这一步需要管理员权限
```

## 挂载

```
//记住你刚才看到的你的要挂载的硬盘名
mount -t ntfs-3g /dev/sdb1 /mnt/harddisk
```

>说明：
>
>/dev/sdb1 是你的硬盘/U盘名 
>/mnt/harddisk 是要挂载的目录，这个目录可以自己指定没有的话可以创建，最好找一个空目录

## 卸载

```
umount -t ntfs-3g /mnt/harddisk
```

# 修复`ntfs`

```
ntfsfix /dev/sdb1
```

> 修复你的硬盘，不过我的硬盘修复后，还没发现其他的变化(手动捂脸苦笑)，本以为修复后就直接系统能识别了，但是还是需要手动挂载。。。。。。