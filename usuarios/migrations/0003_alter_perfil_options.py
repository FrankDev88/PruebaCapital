# Generated by Django 4.2.7 on 2024-06-06 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_rename_usuario_perfil_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'verbose_name_plural': 'Perfiles'},
        ),
    ]