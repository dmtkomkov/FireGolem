from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_task_toworklogsfix'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('aria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Aria')),
            ],
        ),
        migrations.AddField(
            model_name='aria',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Domain'),
        ),
    ]
