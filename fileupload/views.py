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
import smtplib

def send_email(response,user):

    FROMADDR = "uploads@ml.moldiscovery.com"
    LOGIN    = FROMADDR
    #PASSWORD = ""
    TOADDRS  = ["fabrizio@moldiscovery.com"]
    SUBJECT  = "Files uploaded"
    msg_content = "User: %s \r\n" % user

    for file in response['files']:
        msg_content += "File Uploaded: "+ file['name'] + '\r\n' 
        msg_content += "Download: https://ml.moldiscovery.com"+ file['url'] + '\r\n\r\n' 
   
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
    msg += msg_content+"\r\n"

    server = smtplib.SMTP('localhost', 25)
    #server.set_debuglevel(1)
    server.ehlo("ml.moldiscovery.com")
    #server.starttls()
    #server.login(LOGIN, PASSWORD)
    server.sendmail(FROMADDR, TOADDRS, msg)
    server.quit()  


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
       
    return redirect('home')

class FileCreateView(CreateView):
    model = File

    def form_valid(self, form):
        if not self.request.user.is_authenticated():
            return redirect('home')

        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        send_email(data, self.request.user.username)
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class jQueryVersionCreateView(FileCreateView):
    template_name_suffix = '_jquery_form'


class FileDeleteView(DeleteView):
    model = File

    def delete(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
           return redirect('home')

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

        if not self.request.user.is_authenticated():
            return redirect('home')

        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
