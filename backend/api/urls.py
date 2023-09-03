from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('pass/', views.PassDBViewSet.as_view({'get': 'list'})),
    path('pass/<int:pk>/', views.PassDBViewSet.as_view({'get': 'retrieve'})),
    path('pass/add/', views.PassDBViewSet.as_view({'post': 'create'})),
    path('pass/update/<int:pk>/', views.PassDBViewSet.as_view({'put': 'update'})),
    path('pass/delete/<int:pk>/', views.PassDBViewSet.as_view({'delete': 'destroy'})),
    path('notes/', views.SecNotesDBViewSet.as_view({'get': 'list'})),
    path('notes/<int:pk>/', views.SecNotesDBViewSet.as_view({'get': 'retrieve'})),
    path('notes/add/', views.SecNotesDBViewSet.as_view({'post': 'create'})),
    path('notes/update/<int:pk>/', views.SecNotesDBViewSet.as_view({'put': 'update'})),
    path('notes/delete/<int:pk>/', views.SecNotesDBViewSet.as_view({'delete': 'destroy'})),
    path('cards/', views.CardsDBViewSet.as_view({'get': 'list'})),
    path('cards/<int:pk>/', views.CardsDBViewSet.as_view({'get': 'retrieve'})),
    path('cards/add/', views.CardsDBViewSet.as_view({'post': 'create'})),
    path('cards/update/<int:pk>/', views.CardsDBViewSet.as_view({'put': 'update'})),
    path('cards/delete/<int:pk>/', views.CardsDBViewSet.as_view({'delete': 'destroy'})),
    path('files/', views.FileDBViewSet.as_view({'get': 'list'})),
    path('files/<int:pk>/', views.FileDBViewSet.as_view({'get': 'retrieve'})),
    path('files/add/', views.FileDBViewSet.as_view({'post': 'create'})),
    path('files/delete/<int:pk>/', views.FileDBViewSet.as_view({'delete': 'destroy'})),
]