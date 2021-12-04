from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from grade_viewer import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_teacher = models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)


class Course(models.Model):
    course = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return self.course


class Student(models.Model):

    GENDER = (
        ('1', 'Male'),
        ('2', 'Female')
    )

    STATUS = (
        ('1', 'Ongoing'),
        ('2', 'On Probition'),
        ('3', 'NA')
    )

    name = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    id_number = models.IntegerField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER, blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, blank=True, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='3')

    def __str__(self):
        return str(self.name)


class Teacher(models.Model):
    name = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.name)


class SchoolSubject(models.Model):
    subject_name = models.CharField(max_length=250)

    def __str__(self):
        return self.subject_name


class Subject(models.Model):

    SEMESTER_CHOICES = (
        ('1st', '1st Sem'),
        ('2nd', '2nd Sem')
    )
    REMARKS = (
        ('1', 'Passed'),
        ('2', 'Failed'),
        ('3', 'No Grade'),
        ('4', 'Incomplete')
    )
    instructor = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, unique=False)
    name = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    year_taken = models.CharField(max_length=225)
    semester = models.CharField(
        max_length=10, choices=SEMESTER_CHOICES, default='1st')
    # subject_name = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(
        SchoolSubject, on_delete=models.CASCADE, unique=False)
    grade = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, validators=[
                                MinValueValidator(0.00), MaxValueValidator(5.00)])
    remarks = models.CharField(max_length=10, choices=REMARKS, default='3')
    slug = AutoSlugField(populate_from=['subject_name'], max_length=250)

    def __str__(self):
        return str(self.subject_name)

    class Meta:
        ordering = ['-year_taken', '-semester']


@receiver(post_save, sender=User)
def save_user(sender, instance, created, **kwargs):
    if created:
        if instance.is_student:
            Student.objects.create(name=instance)
        elif instance.is_teacher:
            Teacher.objects.create(name=instance)
    # elif instance.is_student and instance.is_teacher:
    #     Student.objects.create(name=instance)
    #     Teacher.objects.create(name=instance)
