# Generated by Django 4.0.5 on 2022-06-02 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0005_order_alter_contract_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(max_length=250, verbose_name='Вид приказа'),
        ),
    ]
