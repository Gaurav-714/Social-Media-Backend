# Generated by Django 5.0.1 on 2024-05-10 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_post_title_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='displayPic',
            field=models.ImageField(blank=True, null=True, upload_to='display_pics'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='post_imgs'),
        ),
    ]
