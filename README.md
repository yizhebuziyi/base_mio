这个说明文件，可以在新项目保留，也可以删除。

主要讲的是环境配置

生产环境：Debian 10 + pypy3.6-7.3.1/Python 3.6.9

脚本是基于这个配置编写，如需升级，请自行处理。

创建 Systemd 启动脚本

如果是pypy环境
```shell script
installer/install_service.pypy.sh 用户名 项目名 worker数
systemctl daemon-reload
systemctl restart 项目名
```
如果是Python环境
```shell script
installer/install_service.sh 用户名 项目名 worker数
systemctl daemon-reload
systemctl restart 项目名
```