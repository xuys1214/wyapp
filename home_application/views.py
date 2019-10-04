# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import time

from blueking.component.shortcuts import get_client_by_user
from common.mymako import render_mako_context, render_json
import json
from models import HostPerforms, HostPerformsUsage


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def helloworld(request):
    """

    :param request:
    :return:
    """
    return render_mako_context(request, '/home_application/helloworld.html')

def apitest(request):
    """

    :param request:
    :return:
    """
    return render_json({"result": "OK", "username": request.user.username})

def services(request):
    return render_mako_context(request, '/home_application/app/index.js')

def get_services_info(request):
    client = get_client_by_user(request.user.username)
    params = {
        "bk_supplier_account": "0",
        "fileds": [
            "bk_biz_id",
            "bk_biz_name"
        ]
    }
    res = client.cc.search_business(params)
    if res["result"]:
        return render_json({"result": True, "data": res["data"]})
    else:
        return render_json({"result": False, "message": res["message"]})

def dist(request):
    return render_mako_context(request, '/dist/index.html')


def get_business_info(request):
    client = get_client_by_user(request.user.username)

    if request.method == 'POST':
        fields = request.POST.get('fields', '')
        print(fields)

    params = {
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ]
    }
    res = client.cc.search_business(params)
    if (res["result"]):
        return render_json({"result": True, "data": res["data"]})
    else:
        return render_json({"result": False, "message": res["message"]})

def get_host_info(request):
    client = get_client_by_user(request.user.username)

    if request.method == 'POST':
        data = json.loads(request.body)
        bk_biz_id = data.get('bk_biz_id', '')
        ip = data.get('ip', {})

        params = {
            'bk_biz_id': bk_biz_id,
            'ip': ip
        }
        print(params)
        res = client.cc.search_host(params)
        if (res["result"]):
            return render_json({"result": True, "data": res["data"]})
        else:
            return render_json({"result": False, "message": res["message"]})
    else:
        return render_json({"result": False, "message": "Method is not allowed"})

def get_job_instance_log(request):
    if (request.method == 'GET'):
        client = get_client_by_user(request.user.username)

        bk_biz_id = request.GET.get('bk_biz_id', '')
        job_instance_id = request.GET.get('job_instance_id', -1)
        params = {
            'bk_biz_id': bk_biz_id,
            'job_instance_id': job_instance_id
        }
        print(params)
        res = client.job.get_job_instance_log(params)
        if (res["result"]):
            return render_json({"result": True, "data": res["data"]})
        else:
            return render_json({"result": False, "message": res["message"]})
    else:
        return render_json({"result": False, "message": "Method is not allowed"})


def fast_execute_script(request):
    client = get_client_by_user(request.user.username)
    if (request.method == 'POST'):
        data = json.loads(request.body)
        bk_biz_id = data.get('bk_biz_id', '2')
        script_content = data.get('script_content', '')
        script_timeout = data.get('script_timeout', 1000)
        account = data.get('account', 'root')
        script_type = data.get('script_type', 1)
        ip_list = data.get('ip_list', [])
        params = {
            'bk_biz_id': bk_biz_id,
            'script_content': script_content,
            'script_timeout': script_timeout,
            'account': account,
            'script_type': script_type,
            'ip_list': ip_list
        }
        print('params:', params)
        res = client.job.fast_execute_script(params)
        print('resulu:', res)
        if (res["result"]):
            return render_json({"result": True, "data": res["data"]})
        else:
            return render_json({"result": False, "message": res["message"]})
    else:
        return render_json({"result": False, "message": "Method is not allowed"})


def get_host_performs(request):
    client = get_client_by_user(request.user.username)
    if (request.method == 'POST'):
        data = json.loads(request.body)
        bk_biz_id = data.get('bk_biz_id', '2')
        script_content = data.get('script_content', '')
        script_timeout = data.get('script_timeout', 1000)
        account = data.get('account', 'root')
        script_type = data.get('script_type', 1)
        ip_list = data.get('ip_list', [])
        params = {
            'bk_biz_id': bk_biz_id,
            'script_content': script_content,
            'script_timeout': script_timeout,
            'account': account,
            'script_type': script_type,
            'ip_list': ip_list
        }
        res = client.job.fast_execute_script(params)
        if (res["result"]):
            # 查询执行日志
            job_instance_id = res.get('data').get('job_instance_id', -1)
            params = {
                'bk_biz_id': bk_biz_id,
                'job_instance_id': job_instance_id
            }
            time.sleep(0.1)
            res = client.job.get_job_instance_log(params)
            while (res["result"]):
                if (res.get('data')[0].get('is_finished', False)):
                    return render_json({"result": True, "data": res["data"]})
                time.sleep(0.1)
                res = client.job.get_job_instance_log(params)
            return render_json({"result": False, "message": res["message"]})
        else:
            return render_json({"result": False, "message": res["message"]})
    else:
        return render_json({"result": False, "message": "Method is not allowed"})

def add_host_performs(request):
    if (request.method == 'GET'):
        client = get_client_by_user(request.user.username)

        ip = request.GET.get('ip', '')
        bk_biz_id = request.GET.get('bk_biz_id', -1)
        bk_cloud_id = request.GET.get('bk_cloud_id', -1)
        if (ip != '' and bk_biz_id != -1 and bk_cloud_id != -1):
            HostPerforms.objects.update_or_create(
                ip=ip,
                bk_biz_id=bk_biz_id,
                bk_cloud_id=bk_cloud_id
            )
            return render_json({"result": True, "message:": "Add success"})
        else:
            return render_json({"result": False, "message:":"Params is error"})
    else:
        return render_json({"result": False, "message": "Method is not allowed"})

def remove_host_performs(request):
    if (request.method == 'GET'):
        client = get_client_by_user(request.user.username)
        ip = request.GET.get('ip', '')
        if (ip != ''):
            ret = HostPerforms.objects.get(ip=ip).delete()
            return render_json({"result": True, "data:": ret})
        else:
            return render_json({"result": False, "message:":"Params is error"})
    else:
        return render_json({"result": False, "message": "Method is not allowed"})

def get_host_performs_ip(request):
    host_performs_ip = HostPerforms.objects.all()
    ip_list = []
    for _data in host_performs_ip:
        ip_list.append(
            _data.ip
        )
    return render_json(({"result": True, "data": ip_list}))

def get_host_performs_history(request):

    ip = request.GET.get('ip', '')
    hostPerformsUsage = HostPerformsUsage.objects.all()
    if ip:
        hostPerformsUsage = hostPerformsUsage.filter(ip=ip)

    dataList = []
    for _data in hostPerformsUsage:
        dataList.append({
            'ip': _data.ip,
            'mem': _data.mem_usage,
            'disk': _data.disk_usage,
            'cpu': _data.cpu_usage,
            'create_time': _data.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return render_json({"result": True, 'data': dataList})


def test_cerely(request):
    user = 'admin'
    client = get_client_by_user(user)

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
                    HostPerformsUsage.objects.update_or_create(
                        ip=_data.ip,
                        mem_usage=log_content_split[1],
                        disk_usage=log_content_split[2],
                        cpu_usage=log_content_split[3],
                    )
                    return True
                time.sleep(0.1)
                res = client.job.get_job_instance_log(params)

