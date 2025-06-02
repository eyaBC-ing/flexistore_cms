from django.views.generic import ListView, CreateView, UpdateView
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import TemplateComponent, TemplatePage
from .serializers import TemplateComponentSerializer, ComponentListSerializer, TemplatePageSerializer
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Vues API existantes
class TemplateComponentViewSet(viewsets.ModelViewSet):
    queryset = TemplateComponent.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ComponentListSerializer
        return TemplateComponentSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        component = self.get_object()
        component.is_active = not component.is_active
        component.save()
        return Response({'status': 'success', 'is_active': component.is_active})
    
    def perform_create(self, serializer):
        serializer.save()
        
    def perform_update(self, serializer):
        serializer.save()

# Nouvelles vues pour l'interface utilisateur
class ComponentListView(ListView):
    model = TemplateComponent
    template_name = 'component_list.html'
    context_object_name = 'components'

class ComponentCreateView(CreateView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = TemplateComponent
    template_name = 'component_form.html'
    fields = ['name', 'type', 'schema', 'html_template', 'is_active']
    success_url = reverse_lazy('component-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component_types'] = TemplateComponent.COMPONENT_TYPES

        if self.object:
            context['component'] = self.object
            try:
                if isinstance(self.object.schema, dict):
                    context['component'].schema = json.dumps(self.object.schema, indent=2)
                elif isinstance(self.object.schema, str):
                    json.loads(self.object.schema)  # Juste pour valider
            except json.JSONDecodeError:
                context['component'].schema = "{}"
        else:
            context['component'] = None  # ou un objet vide si ton template l'exige

        return context



    def form_valid(self, form):
        try:
            schema_data = form.cleaned_data['schema']
            # Convertir en chaîne JSON si ce n'est pas déjà le cas
            if not isinstance(schema_data, str):
                form.instance.schema = json.dumps(schema_data)
            else:
                # Vérifier que la chaîne est un JSON valide
                try:
                    json.loads(schema_data)
                    form.instance.schema = schema_data
                except json.JSONDecodeError:
                    form.add_error('schema', 'Le schéma doit être un JSON valide')
                    return self.form_invalid(form)
            return super().form_valid(form)
        except Exception as e:
            form.add_error('schema', f'Erreur de validation du schéma: {str(e)}')
            return self.form_invalid(form)

class ComponentUpdateView(UpdateView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = TemplateComponent
    template_name = 'component_form.html'
    fields = ['name', 'type', 'schema', 'html_template', 'is_active']
    success_url = reverse_lazy('component-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = self.object  # essentiel
        context['component_types'] = TemplateComponent.COMPONENT_TYPES
    
        # Préparation du schema lisible si c'est du JSON brut
        try:
            if isinstance(self.object.schema, dict):
                context['component'].schema = json.dumps(self.object.schema, indent=2)
            elif isinstance(self.object.schema, str):
                json.loads(self.object.schema)  # valide
        except json.JSONDecodeError:
            context['component'].schema = "{}"
        
        return context

@require_POST
def preview_component(request):
    try:
        schema = json.loads(request.POST.get('schema', '{}'))
        html_template = request.POST.get('html_template', '')
        # Ici, vous pouvez ajouter une logique pour valider et rendre le template
        preview_html = render_to_string('component_preview.html', {
            'preview_html': html_template  # Dans une version plus avancée, vous rendrez le template avec le schéma
        })
        return JsonResponse({'html': preview_html})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON schema'}, status=400)

@require_POST
def toggle_component(request, pk):
    component = get_object_or_404(TemplateComponent, pk=pk)
    component.is_active = not component.is_active
    component.save()
    return JsonResponse({
        'is_active': component.is_active,
        'message': 'Component activated' if component.is_active else 'Component deactivated'
    })



class TemplatePageViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TemplatePage.objects.all()
    serializer_class = TemplatePageSerializer