# Generated by Django 4.2.7 on 2023-12-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_control', '0012_descricao_relatorio_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='rotina',
            name='data_mensal',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rotina',
            name='prazo',
            field=models.CharField(choices=[('Diário', 'Diário'), ('Segunda-Feira', 'Segunda-Feira'), ('Terça-feira', 'Terça-feira'), ('Quarta-Feira', 'Quarta-Feira'), ('Quinta-Feira', 'Quinta-Feira'), ('Sexta-Feira', 'Sexta-Feira'), ('5° Dia Util', '5° Dia Util'), ('15 Dias', '15 Dias'), ('Mensal', 'Mensal')], default='Diário', max_length=15),
        ),
        migrations.AlterField(
            model_name='rotina',
            name='status',
            field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('REALIZADO', 'Realizado'), ('PREVISAO_EXECUCAO', 'Previsão de Execução'), ('REALIZADO_FORA_PRAZO', 'Realizado Fora do Prazo')], default='PENDENTE', max_length=20),
        ),
        migrations.AlterField(
            model_name='statusdiariorotina',
            name='status',
            field=models.CharField(choices=[('PENDENTE', 'Pendente'), ('REALIZADO', 'Realizado'), ('PREVISAO_EXECUCAO', 'Previsão de Execução'), ('REALIZADO_FORA_PRAZO', 'Realizado Fora do Prazo')], default='PENDENTE', max_length=20),
        ),
    ]
