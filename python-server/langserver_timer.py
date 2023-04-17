import datetime
import threading
import subprocess
import os
from calendar import monthrange

from logging_config import GetLog

log = GetLog(os.path.basename(__file__)).get_log()


def func():
    """凌晨1点开启任务"""
    task()
    # 每天执行
    t = threading.Timer(86400, func)
    t.start()


def task():
    """需要执行的任务"""
    log.info('task任务开始执行')

    kill_shell = os.getcwd().replace('\\', '/') + '/kill_pylsp.sh'
    log.info('脚本路径：%s',kill_shell)
    subprocess.run(kill_shell)

    log.info('task任务执行完毕')


def timer_task(execute_time):
    # 获取当前时间
    now_time = datetime.datetime.now()

    # 获取当前时间年、月、日
    now_year = now_time.year
    now_month = now_time.month
    now_day = now_time.day

    # 今天凌晨1点时间表示
    today_3 = datetime.datetime.strptime(str(now_year) + '-' + str(now_month) + '-' + str(now_day) + ' ' + execute_time,
                                         '%Y-%m-%d %H:%M:%S')
    # 明天凌晨1点时间表示
    # 如果是当月最后一天
    if now_day == monthrange(now_year, now_month)[1]:
        # 获取下一个月的第一天
        next_month = datetime.datetime(now_year, now_month, 1) + datetime.timedelta(days=31)
        tomorrow_3 = datetime.datetime.strptime(
            str(next_month.year) + '-' + str(next_month.month) + '-' + str(1) + ' ' + execute_time, '%Y-%m-%d %H:%M:%S')
    else:
        tomorrow_3 = datetime.datetime.strptime(
            str(now_year) + '-' + str(now_month) + '-' + str(now_day + 1) + ' ' + execute_time, '%Y-%m-%d %H:%M:%S')

    # 判断当前时间是否过了今天凌晨1点,如果没过，则今天凌晨1点开始执行，过了则从明天凌晨1点开始执行，计算程序等待执行的时间
    if now_time <= today_3:
        log.info('定时任务将在%s执行', today_3)
        wait_time = (today_3 - now_time).total_seconds()
    else:
        log.info('定时任务将在%s执行', tomorrow_3)
        wait_time = (tomorrow_3 - now_time).total_seconds()

    # 等待wait_time秒后（今天凌晨1点或明天凌晨1点），开启线程去执行func函数
    t = threading.Timer(wait_time, func)
    t.start()
