# Generated by Django 4.2.2 on 2023-07-09 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=64, verbose_name='customer')),
                ('item', models.CharField(max_length=64, verbose_name='item')),
                ('total', models.IntegerField(verbose_name='total')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
