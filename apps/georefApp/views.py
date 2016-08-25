# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

# from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response('georef/home.html',
                              RequestContext(request,{}))
    
    
def osdDemoPage(request):
    return render_to_response('georef/osd_sandbox.html',
                              RequestContext(request,{}))
    
