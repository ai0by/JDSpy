## JDSPY - 大商创京东采集入库

- 京东商品信息采集
- 商品图片下载
- 一键入库（目前支持大商创,ECShop）
- 一键采集入库
![JDSPY](http://fulicos.sbcoder.cn/2019/03/14/5c89ad40669bf.png)
![JDSPY](http://fulicos.sbcoder.cn/2019/03/14/5c89ad3c800de.png)

## 使用说明

- 将post.php放到大商创网站根目录
- 执行 python start.py 即可
- 本程序使用了大商创官方放接口，安全快捷，主要用于快速上传商品

## 使用前请确保以下环境的安装

- Python2.7.9
- Beautifulsoup4
- requests
- photomjs  （待改进）
- selenium

## 配置文件说明

- 配置文件均存放在 config.py 中，按照说明填写即可
- 需要大商创的后台权限
- 需要大商创的数据库写入权限，用于上传商品详情
