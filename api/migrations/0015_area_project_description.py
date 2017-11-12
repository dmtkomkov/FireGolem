from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_area_typofix'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='area',
            name=b'name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name=b'name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
