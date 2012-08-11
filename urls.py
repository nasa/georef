# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.conf.urls.defaults import *  # pylint: disable=W0401
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
     {'loginRequired': False, # avoid redirect loop
      }, 'login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        # show logout page instead of redirecting to log in again
        {'loginRequired': False},
        'logout'),

    url(r'^', include('geocamTiePoint.urls')),

)

if settings.USE_STATIC_SERVE:
    urlpatterns += patterns(
        '',

        url(r'^media/(?P<path>.*)$',
            'geocamUtil.views.staticServeWithExpires.staticServeWithExpires',
            dict(document_root=settings.MEDIA_ROOT,
                 show_indexes=True,
                 readOnly=True)),
        
        url(r'^static/(?P<path>.*)$',
            'geocamUtil.views.staticServeWithExpires.staticServeWithExpires',
            dict(document_root=settings.STATIC_ROOT,
                 show_indexes=True,
                 readOnly=True)),
        
        url(r'^data/(?P<path>.*)$',
            'geocamUtil.views.staticServeWithExpires.staticServeWithExpires',
            dict(document_root=settings.DATA_ROOT,
                 show_indexes=True,
                 readOnly=True)),

        url(r'^favicon.ico$', 'django.views.generic.simple.redirect_to',
            {'url': settings.STATIC_URL + 'mapFasten/icons/mapFastenFavicon.ico',
             'readOnly': True}),
        )
