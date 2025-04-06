from django.views.generic import ListView, TemplateView
from apps.api.models import Item, Portfolio

class ItemListView(ListView):
    model = Item
    template_name = 'items.html'
    context_object_name = 'items'

class PortfolioHistoryView(TemplateView):
    template_name = 'portfolio_history.html'

    def get_template_names(self):
        if self.request.GET.get('portfolio_id'):
            return ['portfolio_results.html']
        return ['portfolio_history.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.all()
        context['min_date'] = '2022-02-15'
        context['max_date'] = '2023-02-16'
        return context