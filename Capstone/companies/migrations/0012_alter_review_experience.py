# Generated by Django 4.2.4 on 2023-09-12 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_alter_review_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='experience',
            field=models.CharField(choices=[('موظف', 'موظف'), ('مقابلة', 'مقابلة'), ('تدريب', 'تدريب')], max_length=128),
        ),
    ]
