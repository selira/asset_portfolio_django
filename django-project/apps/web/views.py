from django.views.generic import TemplateView
from apps.api.models import Portfolio
from apps.api.selectors import get_initial_amounts

class PortfolioView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.all()
        context['min_date'] = '2022-02-15'
        context['max_date'] = '2023-02-16'
        return context

class PortfolioHistoryView(TemplateView):
    template_name = 'portfolio_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.all()
        context['min_date'] = '2022-02-15'
        context['max_date'] = '2023-02-16'
        return context
    
class AssetTradeView(TemplateView):
    template_name = 'asset_trade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        assets, portfolios, portfolio_amounts = get_initial_amounts()

        context['portfolio_amounts'] = portfolio_amounts
        context['portfolios'] = portfolios
        context['assets'] = assets
        return context