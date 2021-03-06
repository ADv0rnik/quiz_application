from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from quizzes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('quizzes/', include('quizzes.urls')),
    path('', include('profile.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#handler404 = pageNotFound