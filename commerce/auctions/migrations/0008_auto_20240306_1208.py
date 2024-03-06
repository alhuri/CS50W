# Generated by Django 3.2.23 on 2024-03-06 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_bid_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biddings', to='auctions.auction'),
        ),
    ]