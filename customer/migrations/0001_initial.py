# Generated by Django 4.2.11 on 2024-03-29 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumner', models.CharField(max_length=128, null=True)),
                ('email', models.CharField(max_length=128, null=True)),
                ('linkedId', models.IntegerField(null=True)),
                ('linkPrecedence', models.CharField(choices=[('p', 'primary'), ('s', 'secondary')], max_length=10)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(null=True)),
            ],
        ),
    ]