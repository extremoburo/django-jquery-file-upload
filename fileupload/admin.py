from fileupload.models import File
from django.contrib import admin
from django.http import HttpResponse
import tarfile
import shutil
from django.contrib import messages
from django.conf import settings
import os.path, time

def validate_size(files, maxsize):
    total_size = 0
    if len(files) > 1:
        for file in files:
            total_size += file.file.size

        return total_size <= maxsize
    return True
    
def make_download(modeladmin, request, queryset):

    try:
        response = HttpResponse(mimetype='application/x-gzip')
        response['Content-Disposition'] = 'attachment; filename=MD_secure_upload_download.tar.gz'
        tarred = tarfile.open(fileobj=response, mode='w:gz')


        if not validate_size(queryset,500000000):
            messages.warning(request, "Download group is too big, unselect some files or select just 1, max size of multple download: 500 MB")

        else:

            for file in queryset:
                tarred.add(settings.MEDIA_ROOT+file.file.name, arcname=file.file.name )
            tarred.close()

            return response

    except tarfile.TarError:
            messages.error(request, "Error while creating the TAR archive, contact the webmaster.")
    except :
            messages.error(request, "There was an error, please contact the webmaster")
        
    
make_download.short_description = "Download selected files"


def make_archive(modeladmin, request, queryset):

    try:

        for file in queryset:
            archive_dir = os.path.join(settings.ARCHIVE_ROOT,file.username)
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)

            shutil.copyfile(settings.MEDIA_ROOT+file.file.name, os.path.join(archive_dir,file.slug))

            file.delete()

            messages.info(request, file.slug + " Archived Successfully")

    except shutil.Error:
        messages.error(request, "File Copy error, please contact the webmaster")
    except :
        messages.error(request, "There was an error, please contact the webmaster")

make_archive.short_description = "Archive selected files"


def file_size(obj):
    if obj.file.size < 1000000:
        return ("%s bytes" % (obj.file.size))
    return ("%s MBs" % (obj.file.size/1000000))
file_size.short_description = 'Size'

def last_modified(obj):
    date_text = "%s" % time.ctime(os.path.getmtime(settings.MEDIA_ROOT+obj.file.name))  
    return date_text    

class FileAdmin(admin.ModelAdmin):
    list_display = ('slug','username', file_size, last_modified)
    search_fields = ['slug', 'username']
    ordering = ('username','slug')
    actions = [make_download,make_archive]
   

admin.site.register(File,FileAdmin)
