import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_app', '0002_cheese_crust_sauce_size_pizza'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('county', models.CharField(max_length=100)),
                ('eircode', models.CharField(max_length=7)),
                ('name_on_card', models.CharField(max_length=100)),
                ('card', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('expiry', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='PizzaUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_ordered', models.DateTimeField(auto_now_add=True)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza_app.pizza')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
