# Generated by Django 5.2 on 2025-04-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0004_alter_professor_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matter_choices', models.CharField(choices=[('CH', 'Ciencias Humanas'), ('L', 'Linguagens'), ('M', 'Matematica'), ('CN', 'Ciencias da Natureza')], max_length=50, null=True)),
            ],
        ),
    ]
