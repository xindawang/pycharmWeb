from django.conf.urls import url
from WangEditor.views import uploadFile
from django.views.static import serve

import os
from django.conf import settings

STATIC_ROOT = os.path.join(settings.STATIC_ROOT, 'editor')

MEDIA_ROOT = settings.STATIC_ROOT

urlpatterns = [
	url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
	url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
	url(r'upload/', uploadFile),
]