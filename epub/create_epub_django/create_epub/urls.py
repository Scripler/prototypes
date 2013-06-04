from django.conf.urls import patterns, include, url
from create_epub import views
from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),                                                  # Admin site
    url(r'^$', 'create_epub.views.create', name='create_1'),                                    # Front page - create EPUB
    url(r'^create/', 'create_epub.views.create', name='create_2'),                              # Create EPUB
	url(r'^epubs/$', views.EpubListView.as_view(), name='epubs'),                               # EPUB list
	#url(r'^epubs/.+\.epub$', views.EpubListView.as_view(), name='epubs'),                      # Download EPUB
	#url(r'^$', views.EpubCreateView.create(self, success_url='/epubs/'), name='create_1'),
	#url(r'^create/', views.EpubCreateView.as_view(success_url='/epubs/'), name='create_2'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)