# coding=utf-8
'''
pip install apscheduler
os.system('comand')
执行括号中的命令
os.path.exists
查看path是否存在

mysql命令
mysqldump - uusername - ppassword
dbname > dbname.sql
导出整个数据库(导出过程会锁表)

mysql命令
mysqldump - -single - transaction - uusername - ppassword
dbname > dbname.sql
导出整个数据库(innodb
导出过程不锁表)


mysql命令
mysqldump - -lock - tables = false - uusername - ppassword
dbname > dbname.sql
导出整个数据库(myisam
导出过程不锁表)
'''
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler

DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'masterchefmb4'
BACK_DIR = '/home/data/'
TODAY = time.strftime('%Y-%m-%d')  # -%H-%M-%S
MONTH = time.strftime('%Y-%m')  # -%H-%M-%S
TODAY_DIR = BACK_DIR + MONTH


def backupsql():
    # 如果目录不存在，新建目录
    if not os.path.exists(TODAY_DIR):
        os.makedirs(TODAY_DIR)
    # 执行mysql命令，导出数据库到新建的文件
    sqlcmd = "mysqldump  --single-transaction -u" + DB_USER + " -p" + DB_PASSWORD + " " + DB_NAME + " > " + TODAY_DIR + "/" + DB_NAME + '_' + TODAY + ".sql"
    os.system(sqlcmd)


# 主函数
def main():
    # 方式一
    # ----------------- 使用 schedule 定时 --------------
    # 经测试，schedule的定时任务没有生效 ...... 换一种思路。
    # python代码只执行备份操作，定时任务由linux系统自带的定时任务实现
    schedule = BlockingScheduler()
    # 每天凌晨1点执行定时任务
    schedule.add_job(func=backupsql, trigger='cron', month='*', day='*', hour='3', minute='30')
    # 启动定时器
    schedule.start()
    # 方式二
    # ----------------- 只 执行备份函数 --------------
    # backupsql()


# 执行主函数
if __name__ == '__main__':
    main()
