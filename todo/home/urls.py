from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToDoViewSet, UserCreate, CustomAuthToken, home_view,  dashboard_view
from . import views

router = DefaultRouter()
router.register(r'todos', ToDoViewSet, basename='todo')

urlpatterns = [
    path('todo/', home_view, name='todo_app'),  # Use 'todo_app_view' for the todo app
    path('', home_view, name='home'), 
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Use 'home_view' for the root URL
    path('api/', include(router.urls)),
    path('api/register/', UserCreate.as_view(), name='register'),
    path('api/api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]
