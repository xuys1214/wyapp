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

# from django.db import models
from django.db import models
class HostPerforms(models.Model):
    ip = models.CharField(max_length=20)
    bk_biz_id = models.IntegerField('业务ID')
    bk_cloud_id = models.IntegerField('云区域ID')
    create_time = models.DateTimeField('纳管时间', auto_now=True)

class HostPerformsUsage(models.Model):
    ip = models.CharField(max_length=20)
    mem_usage = models.CharField('内存使用率', max_length=10)
    disk_usage = models.CharField('磁盘使用率', max_length=10)
    cpu_usage = models.CharField('CPU使用率', max_length=10)
    create_time = models.DateTimeField('录入时间', auto_now=True)