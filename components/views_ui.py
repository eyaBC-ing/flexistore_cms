from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import TemplateComponent, TemplatePage, PageComponent

@user_passes_test(lambda u: u.is_superuser)
def create_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        page = TemplatePage.objects.create(title=title, slug=slug)

        component_ids = request.POST.getlist('components')
        for cid in component_ids:
            order = int(request.POST.get(f'order_{cid}', 0))
            component = TemplateComponent.objects.get(pk=cid)
            PageComponent.objects.create(page=page, component=component, order=order)

        return redirect('page_detail', slug=page.slug)

    components = TemplateComponent.objects.all()
    return render(request, 'create_page.html', {'components': components})

@user_passes_test(lambda u: u.is_superuser)
def page_detail(request, slug):
    page = get_object_or_404(TemplatePage, slug=slug)
    page_components = page.pagecomponent_set.select_related('component').order_by('order')

    def render_component(component):
        data = component.schema_data or {}
        ctype = component.type

        if ctype == "title":
            text = data.get("text", "")
            size = data.get("size", "xl")
            return f"<h1 class='text-{size} font-bold'>{text}</h1>"

        elif ctype == "button":
            label = data.get("label", "Cliquez ici")
            color = data.get("color", "blue")
            return f"<button class='bg-{color}-500 text-white p-2 rounded'>{label}</button>"

        elif ctype == "image":
            url = data.get("url", "")
            alt = data.get("alt", "")
            return f"<img src='{url}' alt='{alt}' class='rounded shadow'/>"

        elif ctype == "text":
            content = data.get("content", "")
            return f"<p class='text-gray-700'>{content}</p>"

        elif ctype == "form":
            placeholder = data.get("placeholder", "Entrer une valeur")
            return f"<form><input class='border p-2 rounded' placeholder='{placeholder}'></form>"

        return "<div>Composant inconnu</div>"

    return render(request, 'page_detail.html', {
        'page': page,
        'components': page_components,
        'render_component': render_component,
    })
