# Generated by Django 4.1.5 on 2023-05-15 10:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("workspaces", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="list",
            old_name="content",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="list",
            old_name="title",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="workspace",
            old_name="content",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="workspace",
            old_name="title",
            new_name="name",
        ),
    ]