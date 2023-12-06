# Generated by Django 4.2.7 on 2023-12-03 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0003_customuser_setor'),
        ('app_control', '0008_delete_responsavel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rotina',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='setor', to='user_control.setor'),
        ),
        migrations.DeleteModel(
            name='Setor',
        ),
    ]