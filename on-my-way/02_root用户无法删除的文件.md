参考文档：https://jingyan.baidu.com/album/fcb5aff7786e1eedab4a7142.html?picindex=3

# root用户无法删除文件???

>如果遇到一个文件使用root用户无法删除该怎么半，`lsattr filename`查看该文件信息，发现不可删除文件具有`i`属性，那么就需要去除`i`属性就可以了

```
去除i属性：chattr -i filename

添加i属性：chattr +i filename
```



