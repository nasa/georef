# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

from django.http import HttpResponseForbidden


class ClosedBetaMiddleware(object):
    def process_request(self, request):
        if request.path.startswith('/public') or request.path == '/':
            return None
        if getattr(request, 'user', None) is None or request.user.is_anonymous():
            return HttpResponseForbidden('401 Sorry, MapFasten is in closed beta and you do not appear to be on the list of authorized testers.')
        return None
