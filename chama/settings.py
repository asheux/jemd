from django.conf import settings

MAX_LENGTH_TEXTAREA = getattr(settings, 'BLOG_MAX_LENGTH_TEXTAREA', None)
