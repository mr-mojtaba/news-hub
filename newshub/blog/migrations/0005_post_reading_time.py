# Generated by Django 5.0.1 on 2024-02-15 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reading_time',
            field=models.PositiveIntegerField(default=0, verbose_name='زمان مطالعه'),
            preserve_default=False,
        ),
    ]