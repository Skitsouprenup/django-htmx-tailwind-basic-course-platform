# Generated by Django 5.2.1 on 2025-05-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_lesson_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='public_id',
            field=models.CharField(db_index=True, default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='public_id',
            field=models.CharField(db_index=True, default='', max_length=150, null=True),
        ),
    ]
