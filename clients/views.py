from django.views.generic import ListView, DetailView, CreateView
from .models import Clients

class ClientsHomeView(ListView):
    model = Clients
    paginate_by = 2
    template_name = 'clients/clients_list.html'
    context_object_name = 'clients'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все клиенты'
        return context
