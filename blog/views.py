from django.views.generic import TemplateView


class index(TemplateView):
    template_name = 'blog/index.html'