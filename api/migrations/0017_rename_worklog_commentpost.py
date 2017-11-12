from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_area_project_ondelete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worklog',
            old_name=b'comment',
            new_name='post',
        ),
    ]
