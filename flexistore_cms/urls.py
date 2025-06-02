from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from strawberry.django.views import GraphQLView
from components.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    # Routes API
    path('api/', include('components.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # GraphQL endpoint
    path('graphql/', GraphQLView.as_view(schema=schema)),
    # Routes de l'interface utilisateur
    path('', include('components.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)