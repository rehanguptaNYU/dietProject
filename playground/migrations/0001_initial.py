# Generated by Django 5.0.6 on 2024-06-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('cuisine_name', models.CharField(max_length=264)),
                ('food_type', models.CharField(max_length=264)),
                ('allergies', models.CharField(default='No allergies', max_length=264)),
                ('height', models.DecimalField(decimal_places=15, max_digits=20)),
                ('weight', models.DecimalField(decimal_places=15, max_digits=20)),
                ('age', models.IntegerField()),
                ('goals', models.CharField(max_length=10000)),
                ('issues', models.CharField(max_length=10000)),
                ('gender', models.CharField(max_length=264)),
            ],
        ),
    ]
