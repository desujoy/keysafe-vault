from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('pass/<int:pk>/', views.PassViewSet.as_view({'get': 'retrieve'})),
    path('pass/user/<int:pk>/', views.PassViewSet.as_view({'get': 'list_user_pass'})),
    path('pass/add/', views.PassViewSet.as_view({'post': 'create'})),
    path('pass/update/<int:pk>/', views.PassViewSet.as_view({'put': 'update'})),
    path('pass/delete/<int:pk>/', views.PassViewSet.as_view({'delete': 'destroy'})),
    path('notes/<int:pk>/', views.SecNotesViewSet.as_view({'get': 'retrieve'})),
    path('notes/user/<int:pk>/', views.SecNotesViewSet.as_view({'get': 'list_user_notes'})),
    path('notes/add/', views.SecNotesViewSet.as_view({'post': 'create'})),
    path('notes/update/<int:pk>/', views.SecNotesViewSet.as_view({'put': 'update'})),
    path('notes/delete/<int:pk>/', views.SecNotesViewSet.as_view({'delete': 'destroy'})),
    path('cards/<int:pk>/', views.CardsViewSet.as_view({'get': 'retrieve'})),
    path('cards/user/<int:pk>/', views.CardsViewSet.as_view({'get': 'list_user_cards'})),
    path('cards/add/', views.CardsViewSet.as_view({'post': 'create'})),
    path('cards/update/<int:pk>/', views.CardsViewSet.as_view({'put': 'update'})),
    path('cards/delete/<int:pk>/', views.CardsViewSet.as_view({'delete': 'destroy'})),
    path('files/<int:pk>/', views.FilesViewSet.as_view({'get': 'retrieve'})),
    path('files/user/<int:pk>/', views.FilesViewSet.as_view({'get': 'list_user_files'})),
    path('files/add/', views.FilesViewSet.as_view({'post': 'create'})),
    path('files/delete/<int:pk>/', views.FilesViewSet.as_view({'delete': 'destroy'})),
    path('files/download/<int:pk>/', views.FilesViewSet.as_view({'get': 'download'})),
    path('users/', views.UsersViewSet.as_view({'get': 'list'})),
    path('users/add/', views.UsersViewSet.as_view({'post': 'create'})), 
    path('users/update/<int:pk>/', views.UsersViewSet.as_view({'put': 'update'})),
    path('users/delete/<int:pk>/', views.UsersViewSet.as_view({'delete': 'destroy'})),
    path('genkeypass/', views.genkeypass, name='genkeypass')
    
]