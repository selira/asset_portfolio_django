from django.views.generic import TemplateView
from apps.api.models import Portfolio, Asset, PortfolioAssetWeight
from decimal import Decimal

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
    
class AssetTradeView2(TemplateView):
    template_name = 'asset_trade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.all()
        context['assets'] = Asset.objects.all()
        return context
    
class AssetTradeView3(TemplateView):
    template_name = 'asset_trade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_value = Decimal('1000000000')
        
        assets = Asset.objects.all()
        weights = PortfolioAssetWeight.objects.filter(
            date='2022-02-15'
        ).select_related('asset', 'portfolio')
        
        # Create portfolio arrays with name as first element
        portfolio_amounts = []
        for portfolio in Portfolio.objects.all():
            portfolio_row = [portfolio.name]  # First element is portfolio name
            for asset in assets:
                weight = weights.filter(
                    portfolio=portfolio, 
                    asset=asset
                ).first()
                amount = weight.weight * initial_value if weight else Decimal('0')
                portfolio_row.append(amount)
            portfolio_amounts.append(portfolio_row)

        context['portfolios'] = Portfolio.objects.all()
        context['portfolio_amounts'] = portfolio_amounts
        context['assets'] = assets
        return context
    
class AssetTradeView(TemplateView):
    template_name = 'asset_trade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_value = Decimal('1000000000')
        
        assets = Asset.objects.all()
        weights = PortfolioAssetWeight.objects.filter(
            date='2022-02-15'
        ).select_related('asset', 'portfolio')
        
        # Create asset rows with portfolio amounts
        portfolio_amounts = []
        portfolios = Portfolio.objects.all()

        # Create a row for each asset
        for asset in assets:
            asset_row = [asset.name]  # First element is asset name
            for portfolio in portfolios:
                weight = weights.filter(
                    portfolio=portfolio, 
                    asset=asset
                ).first()
                amount = weight.weight * initial_value if weight else Decimal('0')
                asset_row.append(amount)
            portfolio_amounts.append(asset_row)

        context['portfolio_amounts'] = portfolio_amounts
        context['portfolios'] = portfolios
        context['assets'] = assets
        return context