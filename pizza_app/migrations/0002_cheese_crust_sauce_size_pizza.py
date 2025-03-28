import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheese',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cheese', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Crust',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('crust', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sauce',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sauce', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pepperoni', models.BooleanField(default=False)),
                ('chicken', models.BooleanField(default=False)),
                ('ham', models.BooleanField(default=False)),
                ('pineapple', models.BooleanField(default=False)),
                ('peppers', models.BooleanField(default=False)),
                ('mushrooms', models.BooleanField(default=False)),
                ('onions', models.BooleanField(default=False)),
                ('olives', models.BooleanField(default=False)),
                ('cheese', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_app.cheese')),
                ('crust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_app.crust')),
                ('sauce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_app.sauce')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_app.size')),
            ],
        ),
    ]
