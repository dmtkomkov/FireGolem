from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_deleted_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='estimation',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
