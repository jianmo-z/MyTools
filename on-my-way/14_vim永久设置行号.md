# VIM永久设置行号

> 参看文档：
>
> ​	https://zhidao.baidu.com/question/546824143.html
>
> ​	https://blog.csdn.net/u011642663/article/details/54620126
>
> ​	https://blog.csdn.net/lwj103862095/article/details/8122316
>
> ​	https://blog.csdn.net/jianfyun/article/details/6594930

## 第一步

> `cd ~`，进入到当前用户的家目录下

## 第二步

> `vim .vimrc`，编辑配置文件，如果没有该配置文件则会新建一个文件，`.`开头的文件在linux下都是隐藏属性的哦，下次想编辑直接输入就可以，并非不存在，只是看不见而已。

## 第三步

> 进入到插入模式后，可选择添加如下内容
>
> `set nu`：设置显示行号，取消显示为`set noun`
>
> `set ai`：自动对齐，即自动补齐`TAB或者空格`
>
> `set cindent shiftwidth=4`：设置缩进为`4个空格`长
>
> `set tabstop=4`：设置`TAB`宽度为四个空格
>
> `set smartindent`：智能的选择对齐方式
>
> `set autoindent`：当前行的对齐方式应用到下一行 

## 补充

> `gg`：光标移动到文档的开始位置
>
> `G`：光标移动到文档的末尾位置

