# encoding: utf-8
from django.db import models
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver



def upload_dir_path(instance, filename):
    return 'uploaded_files/%s/%s' % (instance.username, filename)

class File(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.

    """
    file = models.FileField(upload_to=upload_dir_path)
    slug = models.SlugField(max_length=50, blank=True, verbose_name="file name")
    username = models.CharField(max_length=50)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(File, self).save(*args, **kwargs)

    # use post_delete signal instead
    #def delete(self, *args, **kwargs):
    #    """delete -- Remove to leave file."""
    #    self.file.delete(False)
    #    super(File, self).delete(*args, **kwargs)

@receiver(post_delete, sender=File)
def File_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
