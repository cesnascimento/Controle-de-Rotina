# Generated by Django 4.2.7 on 2024-02-08 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0013_rotina_data_mensal_alter_rotina_prazo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusdiariorotina',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='rotinas_arquivos/'),
        ),
    ]
