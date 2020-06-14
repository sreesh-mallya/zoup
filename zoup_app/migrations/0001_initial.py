# Generated by Django 2.2 on 2020-06-13 12:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('account_type', models.PositiveSmallIntegerField(choices=[(0, 'superuser'), (1, 'admin'), (2, 'restaurant'), (3, 'staff'), (4, 'customer')], default=4)),
                ('contact', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True)),
                ('location', models.CharField(choices=[('kochi', 'Kochi'), ('bengaluru', 'Bengaluru'), ('mumbai', 'Mumbai')], max_length=100)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_approved', models.BooleanField(default=False, verbose_name='approved')),
                ('is_available', models.BooleanField(default=True, verbose_name='available')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('slug', models.SlugField(blank=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('description', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Appetizer', 'Appetizer'), ('Main Course', 'Main Course'), ('Dessert', 'Dessert'), ('Beverage', 'Beverage')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('banner', models.URLField(blank=True, null=True)),
                ('license_number', models.CharField(max_length=10)),
                ('pan_or_gstin', models.CharField(max_length=10)),
                ('fssai', models.CharField(max_length=10)),
                ('location', models.CharField(choices=[('kochi', 'Kochi'), ('bengaluru', 'Bengaluru'), ('mumbai', 'Mumbai')], max_length=50)),
                ('is_serving', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True)),
                ('cuisines', models.CharField(choices=[('North Indian', 'North Indian'), ('South Indian', 'South Indian'), ('Tandoor', 'Tandoor'), ('Chinese', 'Chinese'), ('Bakery', 'Bakery'), ('Asian', 'Asian')], max_length=50)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('support_delivery', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True)),
                ('banner', models.URLField(blank=True, null=True)),
                ('description', models.CharField(max_length=1000)),
                ('from_date', models.DateTimeField(blank=True)),
                ('to_date', models.DateTimeField(blank=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zoup_app.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='zoup_app.Restaurant')),
                ('items', models.ManyToManyField(to='zoup_app.Item')),
            ],
        ),
    ]
