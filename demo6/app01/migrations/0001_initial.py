# Generated by Django 3.0.8 on 2020-08-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '权限表',
                'verbose_name_plural': '权限表',
            },
        ),
        migrations.CreateModel(
            name='Userinfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('permission', models.ManyToManyField(blank=True, null=True, to='app01.Permission')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
    ]
