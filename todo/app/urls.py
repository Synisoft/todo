from .import views

urlpatterns = [
    path('', views.home, name="home"),
]

