# Generated by Django 4.2.6 on 2023-10-19 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tracker", "0003_book_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="readerbookrelationship",
            name="reader",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="Reader",
        ),
    ]
