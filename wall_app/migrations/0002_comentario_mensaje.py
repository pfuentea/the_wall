# Generated by Django 3.2.5 on 2021-08-31 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('escritor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to='wall_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('escritor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_del_usuario', to='wall_app.user')),
                ('mensaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios_del_mensaje', to='wall_app.mensaje')),
            ],
        ),
    ]
