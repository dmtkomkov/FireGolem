from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_area_project_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='project',
            name='deleted',
        ),
        migrations.AlterField(
            model_name='task',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Area'),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Project'),
        ),
    ]
