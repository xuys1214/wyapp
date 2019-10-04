# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
import time

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger
from blueking.component.shortcuts import get_client_by_user
from models import HostPerforms, HostPerformsUsage


# @task()
# def async_task(x, y):
#     """
#     定义一个 celery 异步任务
#     """
#     logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
#     return x + y
#
#
# def execute_task():
#     """
#     执行 celery 异步任务
#
#     调用celery任务方法:
#         task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
#         task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
#         delay(): 简便方法，类似调用普通函数
#         apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
#                       详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
#     """
#     now = datetime.datetime.now()
#     logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
#     # 调用定时任务
#     async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))
#
#
# @periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
# def get_time():
#     """
#     celery 周期任务示例
#
#     run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
#     periodic_task：程序运行时自动触发周期任务
#     """
#     execute_task()
#     now = datetime.datetime.now()
#     logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))

@task()
def get_performs_task():
    user = 'admin'
    client = get_client_by_user(user)
    logger.error('celery 定时任务执行成功')

    hostPerforms = HostPerforms.objects.all()

    for _data in hostPerforms:
        params = {
            'bk_biz_id': _data.bk_biz_id,
            'script_content': 'IyEvYmluL2Jhc2gKTUVNT1JZPSQoZnJlZSAtbSB8IGF3ayAnTlI9PTJ7cHJpbnRmICIlLjJmJSUiLCAkMyoxMDAvJDJ9JykKRElTSz0kKGRmIC1oIHwgYXdrICckTkY9PSIvIntwcmludGYgIiVzIiwgJDV9JykKQ1BVPSQodG9wIC1ibjEgfCBncmVwIGxvYWQgfCBhd2sgJ3twcmludGYgIiUuMmYlJSIsICQoTkYtMil9JykKREFURT0kKGRhdGUgIislWS0lbS0lZCAlSDolTTolUyIpCmVjaG8gLWUgIiREQVRFfCRNRU1PUll8JERJU0t8JENQVSI',
            'script_timeout': 1000,
            'account': 'root',
            'script_type': 1,
            'ip_list': [{
                "bk_cloud_id": _data.bk_cloud_id,
                "ip": _data.ip
            }]
        }
        res = client.job.fast_execute_script(params)
        if (res["result"]):
            # 查询执行日志
            job_instance_id = res.get('data').get('job_instance_id', -1)
            params = {
                'bk_biz_id': _data.bk_biz_id,
                'job_instance_id': job_instance_id
            }
            time.sleep(0.1)
            res = client.job.get_job_instance_log(params)
            while (res["result"]):
                if (res.get('data')[0].get('is_finished', False)):
                    print('job_res:', res)
                    log_content = res.get('data')[0].get('step_results')[0].get('ip_logs')[0].get('log_content')
                    print('log_content:', log_content)
                    log_content_split = log_content.split('|')
                    print('log_content_split:', log_content_split)
                    # 写入数据库
                    HostPerformsUsage.objects.create(
                        ip=_data.ip,
                        mem_usage=log_content_split[1],
                        disk_usage=log_content_split[2],
                        cpu_usage=log_content_split[3],
                    )
                    break
                time.sleep(0.1)
                res = client.job.get_job_instance_log(params)

    return True

@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_performs_periodic():
    """
        获取内存、磁盘、CPU使用率周期执行定义
    """
    get_performs_task.delay()
    now = datetime.datetime.now()
    logger.error(u"get_performs_task 周期任务调用成功，当前时间：{}".format(now))