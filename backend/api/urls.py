from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('pass/', views.PassViewSet.as_view({'get': 'list'})),
    path('pass/<int:pk>/', views.PassViewSet.as_view({'get': 'retrieve'})),
    path('pass/add/', views.PassViewSet.as_view({'post': 'create'})),
    path('pass/update/<int:pk>/', views.PassViewSet.as_view({'put': 'update'})),
    path('pass/delete/<int:pk>/', views.PassViewSet.as_view({'delete': 'destroy'})),
    path('notes/', views.SecNotesViewSet.as_view({'get': 'list'})),
    path('notes/<int:pk>/', views.SecNotesViewSet.as_view({'get': 'retrieve'})),
    path('notes/add/', views.SecNotesViewSet.as_view({'post': 'create'})),
    path('notes/update/<int:pk>/', views.SecNotesViewSet.as_view({'put': 'update'})),
    path('notes/delete/<int:pk>/', views.SecNotesViewSet.as_view({'delete': 'destroy'})),
    path('cards/', views.CardsViewSet.as_view({'get': 'list'})),
    path('cards/<int:pk>/', views.CardsViewSet.as_view({'get': 'retrieve'})),
    path('cards/add/', views.CardsViewSet.as_view({'post': 'create'})),
    path('cards/update/<int:pk>/', views.CardsViewSet.as_view({'put': 'update'})),
    path('cards/delete/<int:pk>/', views.CardsViewSet.as_view({'delete': 'destroy'})),
    path('files/', views.FilesViewSet.as_view({'get': 'list'})),
    path('files/<int:pk>/', views.FilesViewSet.as_view({'get': 'retrieve'})),
    path('files/add/', views.FilesViewSet.as_view({'post': 'create'})),
    path('files/delete/<int:pk>/', views.FilesViewSet.as_view({'delete': 'destroy'})),
]