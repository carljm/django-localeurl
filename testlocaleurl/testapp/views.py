from django.shortcuts import render_to_response

def dummy(request, test=None):
    return render_to_response('test.html')
