from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='Название проекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Проекты'
        verbose_name = 'Проект'
        ordering = ['name']


class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название задачи')
    description = models.TextField(null=True, blank=True, verbose_name='Описание задачи')
    start_date = models.DateField(auto_now_add=True, db_index=True, verbose_name='Срок начала задачи')
    end_date = models.DateField(null=True, blank=True, db_index=True, verbose_name='Срок выполнения задачи')
    project = models.ForeignKey(to='Project', null=True, on_delete=models.PROTECT, verbose_name='Проект')

    class Meta:
        verbose_name_plural = 'Задачи'
        verbose_name = 'Задача'
        ordering = ['project', 'title']