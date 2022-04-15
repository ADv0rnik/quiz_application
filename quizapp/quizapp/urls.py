from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from profile.views import register_user
from quizzes.views import *
from profile.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('quizzes/', include('quizzes.urls')),
    path('', include('profile.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
