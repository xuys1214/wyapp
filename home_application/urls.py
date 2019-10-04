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

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    # (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^helloworld/$', 'helloworld'),
    (r'^api/test$', 'apitest'),
    (r'^services/$', 'get_services_info'),
    (r'^$', 'dist'),
    (r'^performs$/$', 'dist'),
    # (r'^dist/$', 'dist'),
    # (r'^dist/performs$', 'dist'),
    (r'^t/api/get_business_info$', 'get_business_info'),
    (r'^t/api/get_host_info$', 'get_host_info'),
    (r'^t/api/get_job_instance_log$', 'get_job_instance_log'),
    (r'^t/api/get_host_performs$', 'get_host_performs'),
    (r'^t/api/add_host_performs$', 'add_host_performs'),
    (r'^t/api/remove_host_performs$', 'remove_host_performs'),
    (r'^t/api/get_host_performs_ip$', 'get_host_performs_ip'),
    (r'^t/api/get_host_performs_history$', 'get_host_performs_history'),
)
