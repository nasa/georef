# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__


from django.conf.urls import url, include

from django.contrib.auth.views import login 
from django.contrib.auth.views import logout
from django.contrib import auth, admin
from django.conf import settings


urlpatterns = [url(r'^accounts/login/$', auth.views.login, {'loginRequired': False}, 'login'),
               url(r'^accounts/logout/$', auth.views.logout, {'loginRequired': False}, 'logout'),
               url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
               url(r'^admin/', include(admin.site.urls)),
               url(r'^', include('geocamTiePoint.urls')),
               url(r'^', include('georefApp.urls')),
               ]