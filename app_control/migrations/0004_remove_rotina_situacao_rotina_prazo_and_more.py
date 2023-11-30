# Generated by Django 4.2.7 on 2023-11-29 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_control', '0003_remove_responsavel_created_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rotina',
            name='situacao',
        ),
        migrations.AddField(
            model_name='rotina',
            name='prazo',
            field=models.CharField(choices=[('Diário', 'Diário'), ('Segunda-Feira', 'Segunda-Feira'), ('Terça-feira', 'Terça-feira'), ('Quarta-Feira', 'Quarta-Feira'), ('Quinta-Feira', 'Quinta-Feira'), ('Sexta-Feira', 'Sexta-Feira'), ('5° Dia Util', '5° Dia Util')], default='prevista', max_length=15),
        ),
        migrations.AlterField(
            model_name='rotina',
            name='responsavel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsavel', to=settings.AUTH_USER_MODEL),
        ),
    ]
