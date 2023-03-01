from django.contrib import admin
from django.urls import path
from tree.views import GetParentElements, GetElement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetParentElements.as_view()),
    path('<int:pk>/', GetElement.as_view())
]
