from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_task_default_values'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aria',
            name=b'domain',
        ),
        migrations.RemoveField(
            model_name='project',
            name=b'aria',
        ),
        migrations.AddField(
            model_name='task',
            name='aria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Aria'),
        ),
        migrations.DeleteModel(
            name='Domain',
        ),
    ]
