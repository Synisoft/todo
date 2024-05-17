from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import ToDo
from .serializers import ToDoSerializer, UserSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import render


def home_view(request):
    return render(request, 'home/index.html')


def dashboard_view(request):
    return render(request, 'home/dashboard.html')

class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = ToDo.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['completed', 'created_at']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserCreate(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
