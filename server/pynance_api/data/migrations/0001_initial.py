# Generated by Django 3.0.8 on 2021-02-16 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoTicker',
            fields=[
                ('ticker', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='EquityTicker',
            fields=[
                ('ticker', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='StatSymbol',
            fields=[
                ('symbol', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='EquityMarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('open_price', models.DecimalField(decimal_places=4, max_digits=20)),
                ('close_price', models.DecimalField(decimal_places=4, max_digits=20)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.EquityTicker')),
            ],
        ),
        migrations.CreateModel(
            name='Economy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('value', models.DecimalField(decimal_places=10, max_digits=20)),
                ('statistic', models.ForeignKey(max_length=10, on_delete=django.db.models.deletion.CASCADE, to='data.StatSymbol')),
            ],
        ),
        migrations.CreateModel(
            name='Dividends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Payment Date')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=20)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.EquityTicker')),
            ],
        ),
        migrations.CreateModel(
            name='CryptoMarket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('open_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('close_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.CryptoTicker')),
            ],
        ),
    ]
