# Generated by Django 5.0 on 2024-01-14 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'permissions': [('can_arrange_quiz', 'can arrange quiz')]},
        ),
    ]