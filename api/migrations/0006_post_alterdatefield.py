from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_datefields_notblank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name=b'date',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.RunSQL(
            'ALTER TABLE api_post MODIFY created DATETIME;',
        ),
    ]
