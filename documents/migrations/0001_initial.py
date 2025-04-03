# Generated by Django 5.0.2 on 2025-03-25 13:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='documents/')),
                ('document_type', models.CharField(choices=[('pdf', 'PDF'), ('txt', 'Text'), ('doc', 'Word Document'), ('docx', 'Word Document (New)')], max_length=10)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('summary', models.TextField(blank=True, null=True)),
                ('vector_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('file_size', models.IntegerField(help_text='File size in bytes')),
                ('page_count', models.IntegerField(blank=True, null=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='DocumentChunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('chunk_index', models.IntegerField()),
                ('vector_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chunks', to='documents.document')),
            ],
            options={
                'ordering': ['chunk_index'],
                'unique_together': {('document', 'chunk_index')},
            },
        ),
    ]
