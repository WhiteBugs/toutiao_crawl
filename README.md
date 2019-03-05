# 头条up主视频信息爬虫
### 爬虫介绍

该爬虫是朋友要做一个社会学调查，需要爬up主的视频相关数据，所以顺手写的一个小爬虫

### 使用方法

* 双击crawl.py文件即可，运行时会读取id.txt(和crawl.py文件在同一目录)来获取up主的信息以便爬取
* id.txt文件每一行放一个up主的信息，每行两个信息，保存的表格名字(可以设置为up主名字),以及up主的userId(可在up主的个人主页找到),这两个信息用一个空格隔开
* finish.txt文件保存已爬完的up主userId，如果想重新爬某个up主的信息可以把该up主从finish.txt里删除再重新运行爬虫即可

### 其他相关文件说明

* sign.js文件是头条用来生成签名的js文件,我用execjs库执行该文件以获得签名来构造url
* UserAgent.txt文件用来放UA以便随机读取一个UA来构造连接,持续使用同一个UA会被头条所封锁

### todo

* 添加配置文件以便增加其他字段的爬取( 其实也很简单，参照头条返回的数据结构，在saveContent函数里面将相关字段提取出来写到文件即可。。。以及在表格首行添加字段名称。所以后期可能不写了