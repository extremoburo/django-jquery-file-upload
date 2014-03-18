from fileupload.models import File
from django.contrib import admin
from django.http import HttpResponse
import tarfile
from django.contrib import messages

def validate_size(files, maxsize):
    total_size = 0
    if len(files) > 1:
        for file in files:
            total_size += file.file.size

        return total_size <= maxsize
    return True
    
def make_download(modeladmin, request, queryset):
    response = HttpResponse(mimetype='application/x-gzip')
    response['Content-Disposition'] = 'attachment; filename=MD_secure_upload_download.tar.gz'
    tarred = tarfile.open(fileobj=response, mode='w:gz')

    
    if not validate_size(queryset,500000000):
        messages.warning(request, "Download is too big, unselect some files, max size = 500 MB")

    else:
        
        for file in queryset:
            tarred.add("media/"+file.file.name)
        tarred.close()

        return response
    
make_download.short_description = "Download selected files"


class FileAdmin(admin.ModelAdmin):
    actions = [make_download]
   

admin.site.register(File,FileAdmin)
