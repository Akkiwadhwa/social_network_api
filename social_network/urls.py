"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('api/signup/', views.UserSignupView.as_view(), name='user_signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.GetUserDataView.as_view(), name='get_user_data'),
    path('api/posts/', views.PostListCreateView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', views.PostRetrieveUpdateDestroyView.as_view(), name='post_retrieve_update_destroy'),
    path('api/posts/<int:pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('api/posts/<int:pk>/unlike/', views.PostUnlikeView.as_view(), name='post_unlike'),
    path('admin/', admin.site.urls),
]

# Optional: Add router URLs
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'posts', views.PostViewSet)
# urlpatterns += [path('', include(router.urls))]



