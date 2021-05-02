from django.db import models


# Create your models here.
class Answer(models.Model):
    choice_text = models.CharField('Ответ', max_length=200)

    def __str__(self):
        return self.choice_text


class Question(models.Model):
    text = models.CharField('Название вопроса', max_length=200)
    types = (
        ('1', 'Ответ текстом'),
        ('2', 'Ответ с выбором одного варианта'),
        ('3', 'Ответ с выбором нескольких вариантов'),
    )
    type = models.CharField('Тип', max_length=50, choices=types)
    pos_answers = models.ManyToManyField(Answer, verbose_name='Ответы', blank=True)

    def __str__(self):
        return self.text


class Poll(models.Model):
    name = models.CharField('Имя опроса', max_length=200)
    start_date = models.DateTimeField('Дата начала', auto_now_add=True)
    end_date = models.DateTimeField('Дата конца')
    description = models.TextField('Описание')
    questions = models.ManyToManyField(Question, verbose_name='Вопросы')

    def __str__(self):
        return self.name


class User(models.Model):
    site_id = models.IntegerField('ID', unique=True)


class UserAnswer(models.Model):
    user_id = models.ForeignKey(User, verbose_name='ID пользователя', on_delete=models.CASCADE, null=True)
    answer_id = models.ForeignKey(Answer, verbose_name='ID ответа', on_delete=models.CASCADE, blank=True, null=True)
    question_id = models.ForeignKey(Question, verbose_name='ID вопроса', on_delete=models.CASCADE)
    poll_id = models.ForeignKey(Poll, verbose_name='ID опроса', on_delete=models.CASCADE)
    text = models.CharField('Пользовательский ответ', max_length=200, null=True)

