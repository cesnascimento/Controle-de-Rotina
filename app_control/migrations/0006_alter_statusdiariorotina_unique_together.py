# Generated by Django 4.2.7 on 2023-11-29 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0005_rotina_status_alter_rotina_prazo_statusdiariorotina'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='statusdiariorotina',
            unique_together=set(),
        ),
    ]
