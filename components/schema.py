import strawberry
from strawberry.scalars import JSON 
import json
import strawberry_django
from .models import TemplateComponent, TemplatePage
from typing import Optional

@strawberry_django.type(TemplateComponent)
class ComponentType:
    id: strawberry.ID
    name: str
    type: str
    schema: JSON
    html_template: str
    is_active: bool
    created_at: str
    updated_at: str

@strawberry.input
class ComponentInput:
    name: str
    type: str
    schema: JSON
    html_template: str
    is_active: Optional[bool] = True

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_component(self, data: ComponentInput) -> ComponentType:
        return TemplateComponent.objects.create(
            name=data.name,
            type=data.type,
            schema=data.schema,
            html_template=data.html_template,
            is_active=data.is_active
        )

    @strawberry.mutation
    def update_component(self, id: strawberry.ID, data: ComponentInput) -> ComponentType:
        component = TemplateComponent.objects.get(pk=id)
        for key, value in data.__dict__.items():
            setattr(component, key, value)
        component.save()
        return component

    @strawberry.mutation
    def delete_component(self, id: strawberry.ID) -> bool:
        try:
            TemplateComponent.objects.get(pk=id).delete()
            return True
        except TemplateComponent.DoesNotExist:
            return False

@strawberry.type
class Query:
    @strawberry.field
    def components(self) -> list[ComponentType]:
        return TemplateComponent.objects.all()
    
    @strawberry.field
    def component(self, id: strawberry.ID) -> ComponentType:
        return TemplateComponent.objects.get(pk=id)

    @strawberry.field
    def render_component(self, id: strawberry.ID, data: str) -> str:
        component = TemplateComponent.objects.get(pk=id)
        return component.render_from_template(json.loads(data))

schema = strawberry.Schema(query=Query, mutation=Mutation)