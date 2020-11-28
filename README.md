# 项目目录
```
|—— sql         # 存放相关数据库sql语句
|—— static      # 存放静态资源文件
|—— |—— css    
|—— |—— images
|—— |—— js
|—— templates   # 存放html文件
|—— |—— *.html
|—— utils       # 存放一些功能函数
|—— config.py
|—— main.py
```
# 项目环境
- Python:3.*
- mysql:8.*
- Flask:1.1.2
- numpy
# 使用
```
- 安装相关库
```
pip install Flask
pip install numpy
pip install pymysql
```
- 初始化数据库
    - 来到`sql/目录下`命令行进入mysql
    ```
    mysql -u 'userName' -p 
    ```
    - 创建数据库
    ```
    create database game;
    ```
    - 插入数据
    ```
    use game;
    source schema.sql;
    source user.sql;
    source company.sql;
    source game.sql;
    source insert_LikeGame.sql;
    source insert_purchase.sql;
    ```
- 回到主目录
    - 修改`config.py`中
    ```
    config = {
        'default': Config,
        'MYSQL_PASSWORD': 'my password',
        'DATABASE_NAME': 'game'
    }

    - 执行
    ```
    python main.py
    ```
- 打开浏览器,输入
```
localhost:5000
```

