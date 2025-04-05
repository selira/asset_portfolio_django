# Generated by Django 5.2 on 2025-04-05 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_asset_name_alter_portfolio_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetprice',
            name='price',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
        migrations.AlterField(
            model_name='portfolioassetweight',
            name='weight',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
