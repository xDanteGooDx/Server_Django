from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.TextField(max_length=30, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    group = models.TextField(max_length=20, blank=False, null=True)
    course = models.IntegerField()

    class Meta:
        db_table = 'Student'


class Educator(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    scientific_degree = models.TextField(max_length=50, null=True)
    subject_area = models.TextField(max_length=50, null=True)

    class Meta:
        db_table = 'Educator'


class Answer(models.Model):
    id_answer = models.AutoField(primary_key=True)
    answer_text = models.TextField()
    id_question = models.ForeignKey('Question', models.CASCADE, db_column='id_question')
    is_right = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Answer'


class Book(models.Model):
    id_book = models.AutoField(primary_key=True)
    title_book = models.TextField()
    author = models.ForeignKey('Educator', models.DO_NOTHING, db_column='author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Book'


class Chapter(models.Model):
    id_chapter = models.AutoField(primary_key=True)
    chapter_title = models.TextField()
    id_book = models.ForeignKey(Book, models.CASCADE, db_column='id_book')

    class Meta:
        managed = False
        db_table = 'Chapter'


class File(models.Model):
    id_file = models.AutoField(primary_key=True)
    path_file = models.CharField(max_length=255)
    id_text = models.ForeignKey('Text', models.CASCADE, db_column='id_text')
    format = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'File'


class Question(models.Model):
    id_question = models.AutoField(primary_key=True)
    question_text = models.TextField()
    id_test = models.ForeignKey('Test', models.CASCADE, db_column='id_test')
    get_score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Question'


class Test(models.Model):
    id_test = models.AutoField(primary_key=True)
    test_title = models.TextField()
    author = models.ForeignKey(Educator, models.CASCADE, db_column='author', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Test'


class Text(models.Model):
    id_text = models.AutoField(primary_key=True)
    text_source = models.TextField()
    id_chapter = models.ForeignKey(Chapter, models.CASCADE, db_column='id_chapter')

    class Meta:
        managed = False
        db_table = 'Text'


class TestResult(models.Model):
    id_test = models.ForeignKey(Test, models.CASCADE, db_column='id_test', primary_key=True)
    id_student = models.ForeignKey(Student, models.CASCADE, db_column='id_student')
    attempts = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Test_Result'
        unique_together = (('id_test', 'id_student', 'attempts'),)
