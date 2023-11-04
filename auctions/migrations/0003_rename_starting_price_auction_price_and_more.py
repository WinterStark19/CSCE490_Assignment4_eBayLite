# Generated by Django 4.1.2 on 2023-11-04 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_auction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='starting_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='imageURL',
        ),
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='auction',
            name='imageurl',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
