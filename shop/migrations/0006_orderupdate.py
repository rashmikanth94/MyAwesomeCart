# Generated by Django 3.0.4 on 2020-06-25 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200624_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orderupdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=3000)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
