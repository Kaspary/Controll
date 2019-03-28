# Generated by Django 2.1.7 on 2019-03-27 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemuser',
            name='earnings',
            field=models.ManyToManyField(to='finances.Earnings'),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='expense',
            field=models.ManyToManyField(to='finances.Expense'),
        ),
    ]
