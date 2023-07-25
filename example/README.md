# InstaCUC

实现一个图片站点。

运行方式：

```bash
# 初始化数据库
flask db init

# 生成迁移文件
flask db migrate

# 迁移数据库，即创建database以及各个表
flask db upgrade

# 创建管理员账号
flask user create-admin <username@email.com> <username> <password>

# 运行站点
set FLASK_RUN_CERT=cert\selfsignedCertificate.pem
set FLASK_RUN_KEY=cert\privateKey.pem
flask run --host=www.cuccloud.getuplate.com --port=443 --cert=cert\selfsignedCertificate.pem --key=cert\privateKey.pem
```
