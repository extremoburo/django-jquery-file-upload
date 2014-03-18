from fileupload.models import File
from django.contrib import admin
from django.http import HttpResponse
import tarfile

def make_download(modeladmin, request, queryset):
    response = HttpResponse(mimetype='application/x-gzip')
    response['Content-Disposition'] = 'attachment; filename=MD_secure_upload_download.tar.gz'
    tarred = tarfile.open(fileobj=response, mode='w:gz')

    for file in queryset:
       tarred.add("media/"+file.file.name)
    tarred.close()

    return response
    
make_download.short_description = "Download selected files"


class FileAdmin(admin.ModelAdmin):
    actions = [make_download]
   

admin.site.register(File,FileAdmin)
