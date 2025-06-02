from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

def validate_component_schema(value):
    #Si c'est une chaîne (par exemple venant d'un formulaire texte brut), on parse en JSON
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError('Invalid JSON schema')

    #À ce stade, value est censé être un dict
    if not isinstance(value, dict):
        raise ValidationError('Schema must be a JSON object')

    required_fields = ['type', 'properties']
    if not all(field in value for field in required_fields):
        raise ValidationError('Schema must contain "type" and "properties"')
#vérifie que le champ schema contient un JSON valide, avec au minimum deux champs : "type" et "properties"

class TemplateComponent(models.Model): #sert à créer et stocker des blocs HTML dynamiques
    COMPONENT_TYPES = [
        ('button', 'Button'),
        ('title', 'Title'),
        ('image', 'Image'),
        ('product', 'Product'),
        ('form', 'Form'),
    ]

    name = models.CharField(max_length=100) #exemple: bouton d'ajout,titre,..
    type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    schema = models.JSONField(validators=[validate_component_schema]) #Décrire les propriétés du composant
    html_template = models.TextField() #sera utilisé pour afficher le composant dynamiquement
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True) #Activer/désactiver un composant sans le supp

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.type})"

    def clean(self):
        super().clean()
        # Validate that html_template is not empty
        if not self.html_template.strip():
            raise ValidationError({'html_template': 'HTML template cannot be empty'})

    def render_from_template(self):
        from django.template import Template, Context
        try:
            # Assure-toi que schema est bien un dict (et pas une chaîne JSON)
            schema = self.schema if isinstance(self.schema, dict) else json.loads(self.schema)
            properties = schema.get("properties", {})
            template = Template(self.html_template)
            return template.render(Context(properties))
            
        except Exception as e:
            return f"<p>Erreur de rendu : {str(e)}</p>"

class TemplatePage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    components = models.ManyToManyField('TemplateComponent', through='PageComponent')

    def __str__(self):
        return self.title

class PageComponent(models.Model):
    page = models.ForeignKey(TemplatePage, on_delete=models.CASCADE)
    component = models.ForeignKey('TemplateComponent', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']