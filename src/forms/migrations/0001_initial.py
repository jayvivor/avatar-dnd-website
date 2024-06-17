# Generated by Django 5.0.6 on 2024-06-17 17:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DndAbility',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndCastingSpeed',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndClass',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndComponent',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndDamageType',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndElement',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('general_desc', models.TextField()),
                ('trait_desc', models.TextField()),
                ('combat_desc', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndMasteryLevel',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndDiscipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.dndelement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndForm',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('has_higher_level_bonus', models.BooleanField()),
                ('higher_levels', models.TextField(blank=True)),
                ('concentration', models.BooleanField()),
                ('target', models.CharField(max_length=20)),
                ('duration', models.CharField(max_length=20)),
                ('range', models.CharField(max_length=30)),
                ('costs_slot', models.BooleanField()),
                ('special_reqs', models.TextField()),
                ('casting_speed', models.ManyToManyField(to='forms.dndcastingspeed')),
                ('classes', models.ManyToManyField(to='forms.dndclass')),
                ('components', models.ManyToManyField(to='forms.dndcomponent')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.dnddiscipline')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.dndelement')),
                ('saving_throw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.dndability')),
                ('mastery', models.ManyToManyField(to='forms.dndmasterylevel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DndRoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('num_dice', models.IntegerField()),
                ('num_sides', models.IntegerField()),
                ('damage_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.dnddamagetype')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.dndform')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
