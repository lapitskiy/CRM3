from django.views.generic import ListView
from .models import Money

class MoneyHomeView(ListView):
    model = Money
    paginate_by = 10
    template_name = 'money/money_list.html'
    context_object_name = 'money'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Деньги'
        return context