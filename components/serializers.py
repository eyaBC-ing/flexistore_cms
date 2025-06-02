from rest_framework import serializers
from .models import TemplatePage, PageComponent, TemplateComponent

class ComponentSchemaSerializer(serializers.Serializer):
    type = serializers.CharField()
    properties = serializers.DictField()

    def validate(self, data):
        if 'type' not in data or 'properties' not in data:
            raise serializers.ValidationError("Le schéma doit contenir 'type' et 'properties'")
        return data
# vérifie que les deux champs obligatoires sont bien présents dans le JSON (type et properties).
class TemplateComponentSerializer(serializers.ModelSerializer):
    schema = ComponentSchemaSerializer()

    class Meta:
        model = TemplateComponent
        fields = ['id', 'name', 'type', 'schema', 'html_template', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['created_at', 'updated_at']

    def validate_html_template(self, value):
        if not value.strip():
            raise serializers.ValidationError("Le template HTML ne peut pas être vide")
        return value

    def validate_schema(self, value):
        # Validation supplémentaire du schéma si nécessaire
        if not isinstance(value, dict):
            raise serializers.ValidationError("Le schéma doit être un objet JSON valide")
        return value

class ComponentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateComponent
        fields = ['id', 'name', 'type', 'is_active']


class TemplateComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateComponent
        fields = ['id', 'name', 'json_schema', 'rendered_html']

class PageComponentSerializer(serializers.ModelSerializer):
    component = TemplateComponentSerializer()

    class Meta:
        model = PageComponent
        fields = ['order', 'component']

class TemplatePageSerializer(serializers.ModelSerializer):
    components = PageComponentSerializer(source='pagecomponent_set', many=True)

    class Meta:
        model = TemplatePage
        fields = ['id', 'title', 'slug', 'components']