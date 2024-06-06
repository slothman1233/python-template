import subprocess
import schedule
import threading
import time

import os
count = os.cpu_count()


def job1():
    print("I'm working for job1")
    subprocess.Popen("scrapy crawl selenium")


def job1_task():
    return threading.Thread(target=job1)


def start():
    print(count)
    for _ in range(count):
        t1 = job1_task()
        t1.setDaemon(True)
        t1.start()

    # schedule.every(10).seconds.do(job1_task)
    # schedule.every(3).seconds.do(job1_task)
    # schedule.every(2).hour.do(job2_task)
if __name__ == '__main__':
    start()
    # print('当前时间为{}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    while True:
        schedule.run_pending()
        time.sleep(1)
