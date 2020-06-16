import itertools
import random
import string

from django.template.defaultfilters import slugify


def slugify_fields(instance, attr1, attr2):
    klass = instance.__class__
    slug = temp = slugify(getattr(instance, attr1) + getattr(instance, attr2))
    for x in itertools.count(1):
        if not klass.objects.filter(slug=slug).exists():
            break
        slug = '%s-%d' % (temp, x)
    return slug


def slugify_field(instance, attr):
    klass = instance.__class__
    slug = temp = slugify(getattr(instance, attr))
    for x in itertools.count(1):
        if not klass.objects.filter(slug=slug).exists():
            break
        slug = '%s-%d' % (temp, x)
    return slug


def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
