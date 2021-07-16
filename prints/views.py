from django.views.generic import ListView
from .models import Prints

class PrintsHomeView(ListView):
    model = Prints
    paginate_by = 2
    template_name = 'prints/prints_list.html'
    context_object_name = 'prints'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все печатные'
        return context