from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_post_alterdatefield'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.PositiveSmallIntegerField(default=0)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Post')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name=b'worklog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WorkLog'),
        ),
        migrations.RunSQL(
            'ALTER TABLE api_post MODIFY created DATETIME;'
        ),
    ]
