from django.views.generic import TemplateView
from users.decorators import should_not_be_logged_in
from django.utils.decorators import method_decorator

@method_decorator(should_not_be_logged_in, name = 'dispatch')
class HomePage(TemplateView):
    template_name = 'home.html'
