from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplatePageViewSet
from . import views, views_ui

# Configuration du routeur API REST
router = DefaultRouter()
router.register(r'api/components', views.TemplateComponentViewSet)
router.register(r'pages', TemplatePageViewSet, basename='pages')
# URLs pour l'interface utilisateur
urlpatterns = [
    # Routes API
    path('api/', include(router.urls)),
    path('pages/create/', views_ui.create_page, name='create_page'),
    path('pages/<slug:slug>/', views_ui.page_detail, name='page_detail'),
    # Routes pour l'interface utilisateur
    path('', views.ComponentListView.as_view(), name='component-list'),
    path('create/', views.ComponentCreateView.as_view(), name='component-create'),
    path('<int:pk>/edit/', views.ComponentUpdateView.as_view(), name='component-edit'),
    path('<int:pk>/toggle/', views.toggle_component, name='component-toggle'),
    path('preview/', views.preview_component, name='component-preview'),
]
