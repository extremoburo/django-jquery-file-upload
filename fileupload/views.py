# encoding: utf-8
import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from .models import File
from .response import JSONResponse, response_mimetype
from .serialize import serialize
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/upload/jquery-ui/')

def login_view(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
       
    return redirect('/upload/jquery-ui/')



class FileCreateView(CreateView):
    model = File

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class BasicVersionCreateView(FileCreateView):
    template_name_suffix = '_basic_form'


class BasicPlusVersionCreateView(FileCreateView):
    template_name_suffix = '_basicplus_form'


class AngularVersionCreateView(FileCreateView):
    template_name_suffix = '_angular_form'


class jQueryVersionCreateView(FileCreateView):
    template_name_suffix = '_jquery_form'


class FileDeleteView(DeleteView):
    model = File

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class FileListView(ListView):
    model = File

    def get_queryset(self):
        return File.objects.filter(username=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
