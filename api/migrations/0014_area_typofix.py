from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_todo_project_aria'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Aria',
            new_name='Area',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='aria',
            new_name='area',
        ),
    ]
