#__BEGIN_LICENSE__
# Copyright (c) 2017, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The GeoRef platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

from django.conf.urls import url, include
from django.conf.urls import handler400, handler403, handler404, handler500
from django.views.generic.base import TemplateView
from georefApp import views

# handler400 = 'my_app.views.bad_request'
# handler403 = 'my_app.views.permission_denied'
# handler404 = 'my_app.views.page_not_found'
# handler500 = 'my_app.views.server_error'

urlpatterns = [url(r'^$', views.home, {}, 'georef_home'), 
               url(r'^georefV2demo/$', views.osdDemoPage, {}, 'georef_osd_demo'),
               url(r'^error', TemplateView.as_view(template_name='error.html'), {}, 'georef_error'),
               ] 