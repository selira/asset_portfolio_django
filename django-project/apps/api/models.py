from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Portfolio(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name
    
class PortfolioAssetWeight(BaseModel):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=24, decimal_places=12)
    date = models.DateField()

    class Meta:
        unique_together = ['asset', 'portfolio', 'date']

    def __str__(self):
        return f"{self.asset} - {self.weight}%"
    
class Asset(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class AssetPrice(BaseModel):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=24, decimal_places=12)
    date = models.DateField()

    class Meta:
        unique_together = ['asset', 'date']
        indexes = [
            models.Index(fields=['date', 'asset']),
        ]

    def __str__(self):
        return f"{self.asset} - {self.price}"