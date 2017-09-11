from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_task_worklog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name=b'worklog',
        ),
        migrations.AddField(
            model_name='worklog',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Task'),
        ),
    ]
