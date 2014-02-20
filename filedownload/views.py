# Create your views here.
from fileupload.models import File
from fileupload.views import FileListView
from fileupload.serialize import serialize 
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
import os

def listMediaDir_view(request):

    upload_path = settings.UPLOAD_ROOT

    if os.path.isdir(upload_path):
        dirlist = os.listdir(upload_path)
        
        return render_to_response('filedownload/downloads.html', {'list': dirlist}
                                  , context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound('<h1>Error.Could not find the media folder</h1>')


class DirectoryFileListView(FileListView):

    # I just need to change this function
    def get_queryset(self):
        return File.objects.filter(username=self.request.GET.get('container'))
