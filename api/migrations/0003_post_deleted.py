from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
