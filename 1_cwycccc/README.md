# cwycccc个人实验报告


## 1 功能完成情况
### 1.1 主要贡献 
- 实现https绑定证书到域名而非IP地址
- 完成第一部分基于网页的用户注册与登录系统的基本结构的实现（实现用户注册合法用户名，口令验证和限制，密文存储用户口令等功能）
- 修改用户忘记密码时候的验证码会出现在URL信息中的小问题

### 1.2 参与完成
- 参与后期整体情况优化
- 参与研究文件加密和签名的思路

## 2 实验总结
对实验过程以及学习到的内容进行汇总，提出印象深刻的Bug和解决方法

### 2.1 X.509证书
#### 实现过程
- 使用Python中的`cryptography`库来生成私钥（private key）和自签名证书（self-signed certificate）。
- 首先用RSA算法生成4096位的私钥对象，然后利用私钥和其他信息来生成证书，使用`x509.Name`来构建证书的主题信息和颁发者信息，其中包括国家（Country）、省份（State/Province）、城市（Locality）、组织（Organization）、组织单位（Organizational Unit）和通用名称（Common Name）。然后，使用私钥的公钥、证书序列号、有效期等信息来构建证书内容，并使用私钥对证书进行签名。
**没有涉及中间证书的生成，只生成了一个自签名证书（也就是证书的颁发者和主题是一致的）**
#### 实现过程中遇到问题以及解决方法
1. 自签名的证书无法被浏览器信任的问题
- 因为我生成的这个证书颁发者和主题是一样的，没有中间证书，但是浏览器默认只信任受信任的第三方根证书，自签名证书缺乏信任和完整的信任链
- 将自签名证书加到根证书存储中，并不能满足浏览器完整的信任链，所以同时需要加到中间证书颁发机构
**注意**
需要修改本地的hosts文件，添加`127.0.0.1 www.cuccloud.getuplate.com`的映射关系,否则服务器无法确认本机身份，无法建立安全连接

2. `flask run `无法修改端口以及主机问题
flask 启动有两种方式，一种是通过python **.py,还有一种是直接flask run整个应用
```python 
if __name__ == '__main__'
    certFile='./cert/selfsignedCertificate.pem'
    keyFile='./cert/privateKey.pem'
    app.run(host='www.cuccloud.getuplate.com',port=443,ssl_context=(certFile,keyFile))
```
运行这两种方式的时候发现，python **.py可以通过上面的代码换端口和主机，但是
flask run整个项目的时候默认是127.0.0.1，端口5000     

除非在配置的时候规定指定主机和端口
```python
# 运行站点
set FLASK_RUN_CERT=cert\selfsignedCertificate.pem
set FLASK_RUN_KEY=cert\privateKey.pem
flask run --host=www.cuccloud.getuplate.com --port=443 --cert=cert\selfsignedCertificate.pem --key=cert\privateKey.pem
```
### 2.2 用户注册和登录
- 正则表达式校验用户注册信息，不匹配的时候弹出提示
（刚开始在这里卡很久，因为不懂怎么传到前端）
- 用户口令加密存储
在存入数据库之前对用户输入的进行哈希操作，使用的是bcrypt密码哈希函数，过增加计算成本和盐值的使用来增加密码破解的难度。

### 2.3 如何隐藏URL中的验证码

- 最开始想的是在前端隐藏，但是做了好久都没实现，后面换成了加密传输token到前端

## 3 总结
半个月的小学期时间，我好像每天都在琢磨怎么解决各种问题，怎么让这个代码跑起来，怎么快点进行下一步,怎么能快点结束，有时候可能一天下来什么都没有变。

这个小学期收获还是满满的，从我完成之后的只能注册的界面到现在的功能完善的项目，好像在做梦一样。

特别感谢组长大人帮我，很多时候他都是随叫随到，告诉我架构是怎么实现的，怎么去解决这个问题，真的特别崇拜他。

## 4 参考链接
- [X.509 Reference](https://cryptography.io/en/latest/x509/reference/#cryptography.x509.CertificateSigningRequest)
- [Run flask application over HTTPS](https://nagasudhir.blogspot.com/2022/10/run-flask-application-over-https.html)
- [Flask 如何更改flask命令使用的主机和端口](https://deepinout.com/flask/flask-questions/73_flask_how_can_i_change_the_host_and_port_that_the_flask_command_uses.html)
