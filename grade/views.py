from typing import List
from django.shortcuts import render, redirect, get_list_or_404
from django.urls.base import reverse
from .forms import SignUpForm, LoginForm, PasswordChangingForm, StudentInformationForm, StudentSubjectForm
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from .models import Student, Subject, Teacher, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView, CreateView
from .forms import UpdateGradeForm
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'register/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student-grade', pk=user.pk)
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('teacher')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'register/login.html', {'form': form, 'msg': msg})


##### ADMIN #####

def admin(request):
    return render(request, 'grade/admin.html')


class TeacherListView(ListView):
    model = Teacher
    template_name = 'grade/teacher_list.html'
    # context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        return context


class StudentListView(ListView):
    model = Student
    template_name = 'grade/student_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        return context


class StudentInformationView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'grade/student_form.html'
    form_class = StudentInformationForm

    def get_success_url(self):
        return reverse_lazy('admin-student-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.get(pk=self.kwargs.get('pk'))
        return context


class StudentSubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'grade/student_subjects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.filter(name=self.kwargs['pk'])
        context['student_subjects_url'] = Student.objects.get(
            pk=self.kwargs.get('pk'))
        # print(context['student_subjects_url'].pk)
        return context


class StudentSubjectForm(LoginRequiredMixin, CreateView):
    # model = Subject
    template_name = 'grade/subject_form.html'
    form_class = StudentSubjectForm

    def get_success_url(self):
        pk = self.object.pk
        qs = Subject.objects.get(pk=pk)
        student = qs.name.pk
        return reverse_lazy('student-subjects', kwargs={'pk': student})
        # return reverse_lazy('student-subjects', args={self.object.pk})

    # def get_initial(self):
    #     initial = super(StudentSubjectForm, self).get_initial()
    #     initial.update({'name': self.kwargs.get('pk')})
    #     print(self.kwargs.get('pk'))
    #     return initial

    def get_initial(self):
        return {'name': self.kwargs.get('pk')}

    # def form_valid(self, form):
    #     form.instance.name = Subject.objects.get(name=self.kwargs['pk'])
    #     print(self.kwargs['pk'])
    #     return super(StudentSubjectForm, self).form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['student_subjects'] = Subject.objects.get(
    #         name=self.kwargs.get('pk'))
    #     print(context)
    #     return context


##### STUDENT #####


def student(request):
    return render(request, 'student/student.html')


class StudentSubjects(ListView):
    model = Subject
    template_name = 'student/student_grade.html'
    context_object_name = 'student'

    def get_queryset(self, *args, **kwargs):
        names = get_list_or_404(
            Student, pk=self.kwargs.get('pk'))

        if 'school_year' in self.request.GET:
            school_year = self.request.GET['school_year']
            return Subject.objects.filter(name=names[0], year_taken=school_year)

        sub = Subject.objects.filter(name=names[0])
        return sub

    def get_context_data(self, **kwargs):
        names = get_list_or_404(
            Student, pk=self.kwargs.get('pk'))
        a = []
        b = []
        context = super().get_context_data(**kwargs)
        context['id_number'] = Student.objects.filter(
            pk=self.kwargs.get('id_number'))

        context['year'] = Subject.objects.filter(name=names[0])
        for i in context['year']:
            a.append(i.year_taken)
        # print(a)
        for i in a:
            if i not in b:
                b.append(i)
        # print(b)
        # context['years'] = Subject.objects.filter(year_taken=b[0])
        # print(b)

        # context['years'] = Subject.objects.all().order_by('year_taken')
        context['years'] = b

        context['information'] = Student.objects.filter(
            pk=self.request.user.pk)

        return context


##### TEACHER #####


# def teacher(request):
#     return render(request, 'teacher/teacher.html')


class TeacherSubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'teacher/teacher_subjects.html'
    context_object_name = 'teacher_subject'
    # slug_field = 'slug'

    # def get_queryset(self):
    #     return get_object_or_404(Subject, self.get_object())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['teach_sub'] = Subject.objects.filter(
        #     instructor=self.request.user)
        # a = get_object_or_404(Subject, subject_name=self.kwargs.get('id'))
        # a = Subject.objects.filter(instructor=self.request.user.id, year_taken='2019-2020').values(
        #     'subject_name').annotate(Count('name')).order_by()
        # print(a)
        context['teach_sub'] = Subject.objects.filter(
            instructor_id=self.request.user.id).values('subject_name__subject_name', 'subject_name_id', 'year_taken', 'subject_name').annotate(Count('name')).order_by("-year_taken").distinct()

        # print(context)
        return context


class StudentList(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'student_list'
    template_name = 'teacher/student_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # a = Subject.objects.values_list('subject_name', flat=True).distinct()
        # print(a)

        context['students_enrolled'] = Subject.objects.filter(
            instructor=self.request.user.id, subject_name=self.kwargs['subject_name_id'], year_taken=self.kwargs['year_taken'])
        context['title'] = context['students_enrolled'][0]
        # print(context['students_enrolled'][0])

        male = 0
        female = 0
        passed = 0
        failed = 0
        inc = 0

        gender = Subject.objects.filter(instructor=self.request.user.id,
                                        subject_name=self.kwargs['subject_name_id'], year_taken=self.kwargs['year_taken']).values('name__gender')
        for key, value in enumerate(gender):
            if value['name__gender'] == '1':
                male += 1
            else:
                female += 1

        context['male'] = male
        context['female'] = female

        grade = Subject.objects.filter(instructor=self.request.user.id,
                                       subject_name=self.kwargs['subject_name_id'], year_taken=self.kwargs['year_taken']).values('remarks')

        for key, value in enumerate(grade):
            if value['remarks'] == '1':
                passed += 1
            elif value['remarks'] == '2':
                failed += 1
            else:
                inc += 1

        context['passed'] = passed
        context['failed'] = failed
        context['inc'] = inc

        return context


class GradeUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    # template_name = 'teacher/modal.html'
    template_name = 'teacher/update_grade.html'
    # fields = ['grade']
    # success_url = '/'
    form_class = UpdateGradeForm

    def get_success_url(self):
        subject = self.object.subject_name
        year = self.object.year_taken
        return reverse_lazy('student-list', kwargs={"subject_name_id": subject.id, "year_taken": year})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Subject.objects.get(
            pk=self.kwargs.get('pk'))
        return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object
    #     request.POST = request.POST.copy()
    #     request.POST['grade'] = self.object.grade
    #     return super(GradeUpdateView, self).post(request, **kwargs)


class HomeStudentList(ListView):
    model = Subject
    template_name = 'teacher/teacher.html'

    def get_context_data(self, **kwargs):
        male = 0
        female = 0
        context = super().get_context_data(**kwargs)
        context['students'] = Subject.objects.filter(
            instructor=self.request.user.id)

        gender = Subject.objects.filter(
            instructor=self.request.user.id).values('name__gender')
        for key, value in enumerate(gender):
            # print(value['name__gender'])
            if value['name__gender'] == "1":
                male += 1
            else:
                female += 1

        context['male'] = male
        context['female'] = female

        total_student = 0
        t_students = Subject.objects.filter(
            instructor=self.request.user.id).values('name__name')

        for key, value in enumerate(t_students):
            total_student += 1
        context['total_students'] = total_student

        total_subject = 0
        t_subjects = Subject.objects.filter(
            instructor=self.request.user.id).values('subject_name').distinct()
        print(t_subjects)
        for i in t_subjects:
            total_subject += 1
        context['total_subjects'] = total_subject

        return context


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


@login_required
def password_success(request):
    return render(request, 'register/password_success.html')
