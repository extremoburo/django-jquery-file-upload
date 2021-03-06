# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 37:
        return name
    return name[:37] + "..." + name[-7:]


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a File instance into a dict.

    instance -- File instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        #'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'type': mimetypes.guess_type(obj.path)[0],
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse('upload-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
    }


