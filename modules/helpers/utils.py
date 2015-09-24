# -*- coding: utf-8 -*-

from helpers.log import logger
from gluon.globals import current


class resize(object):
    def __init__(self, nx=160, ny=80, error_message=' image resize'):
        (self.nx, self.ny, self.error_message) = (nx, ny, error_message)

    def __call__(self, value):
        if isinstance(value, str) and len(value) == 0:
            return value, None
        from PIL import Image
        import cStringIO
        try:
            img = Image.open(value.file)
            img.thumbnail((self.nx, self.ny), Image.ANTIALIAS)
            s = cStringIO.StringIO()
            img.save(s, 'JPEG', quality=90)
            s.seek(0)
            value.file = s
        except:
            return value, self.error_message
        else:
            return value, None


def thumb(image, nx=120, ny=120, gae=False, name='thumb'):
    '''
    :param image:
    :param nx:
    :param ny:
    :param gae: In case you run in google app engine
    :param name: prefix name for the entire name picture
    :return:string with the name of the thumb
    '''
    try:
        if image:
            if not gae:
                request = current.request
                from PIL import Image
                import os
                img = Image.open(request.folder + 'uploads/' + image)
                thumb_size = (int(nx), int(ny))
                img.thumbnail(thumb_size, Image.ANTIALIAS)
                root, ext = os.path.splitext(image)
                thumb_name = '%s_%s%s' % (root, name, ext)
                img.save(request.folder + 'uploads/' + thumb_name, 'JPEG', quality=90)
                return thumb_name
            else:
                return image
    except Exception as e:
        logger.error(str(e))
