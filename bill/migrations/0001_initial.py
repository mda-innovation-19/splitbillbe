# Generated by Django 4.2.4 on 2025-03-24 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('amount', models.IntegerField(default=0)),
                ('service_fee', models.IntegerField(default=0)),
                ('tax', models.IntegerField(default=0)),
                ('discount', models.IntegerField(default=0)),
                ('total_amount', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
        migrations.CreateModel(
            name='Billitem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.bill')),
            ],
        ),
        migrations.CreateModel(
            name='BillSplit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tax', models.IntegerField()),
                ('service_fee', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.bill')),
                ('billitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill.billitem')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
    ]
