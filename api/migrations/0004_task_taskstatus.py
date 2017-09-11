import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_post_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('worklog', models.PositiveSmallIntegerField(default=0)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TaskStatus'),
        ),
        migrations.RunSQL(
            'ALTER TABLE api_task MODIFY created DATETIME;'
        ),
        migrations.RunSQL(
            'ALTER TABLE api_task MODIFY updated DATETIME;'
        ),
    ]
