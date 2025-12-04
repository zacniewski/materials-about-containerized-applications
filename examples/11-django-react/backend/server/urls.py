from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from todos.views import TodoViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
