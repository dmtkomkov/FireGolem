from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_worklog_commentpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatus',
            name='icon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
