# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

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
               url(r'^error', TemplateView.as_view(template_name='error.html'), {}, 'error'),
               ] 