from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# Create your views here.
from django.template.backends.base import BaseEngine

from django.urls import reverse_lazy


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.http import HttpResponse
from django.template import loader


from django.forms.models import model_to_dict


from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


from .models import Note
from .models import Project
from .models import Task

from .forms import NoteForm
from .forms import TaskForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin




def Home(request):
    template = loader.get_template('pages/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required(login_url="login")
def Dashboard(request):
    open_projects = get_objects_for_user(request.user, 'attero.view_project').filter(status="open")
    completed_projects= get_objects_for_user(request.user, 'attero.view_project').filter(status='closed').count

    open_notes = Note.objects.filter(project__in=open_projects)
    #latest_notes = Note.objects.filter(project__in=open_projects).order_by('updated')[:5]
    latest_notes = open_notes.order_by('updated')[:5]

    completed_tasks = Task.objects.filter(project__in=open_projects, complete=True)
    #completed_tasks = Task.objects.filter(complete=True)
    #incomplete_tasks = Task.objects.filter(complete=False)
    incomplete_tasks = Task.objects.filter(project__in=open_projects, complete=False)
    #latest_tasks = Task.objects.order_by('updated')[:5]
    latest_tasks = Task.objects.filter(project__in=open_projects).order_by('updated')[:5]

    context = {
            'open_projects' : open_projects,
            'open_notes' :  open_notes,
            'latest_notes' : latest_notes,
            'incomplete_tasks' : incomplete_tasks,
            'completed_projects' : completed_projects,
            'latest_tasks' : latest_tasks,
            'completed_tasks' : completed_tasks
    }
    return render(request, 'pages/dashboard.html', context)

@login_required(login_url="login")
def Settings(request):
    context = {}
    return render(request, 'pages/settings.html', context)


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password.html', {
        'form': form
    })

from .forms import UserChangeForm

@login_required(login_url="login")
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'registration/profile.html', context)





def TaskList(request):
    tasks = Task.objects.all()
    return render(request, 'task/all.html', { 'tasks': tasks})







@login_required(login_url="login")
class IndexView(generic.ListView):
    template_name = 'pages/index.html'
    context_object_name = 'latest_note_list'

    def get_queryset(self):
        """Return the last five published notes."""
        return Note.objects.order_by('-pub_date')[:5]


#@login_required(login_url="login")
class ProjectList(LoginRequiredMixin, PermissionListMixin, ListView):
    permission_required = 'attero.view_project'
    template_name = "project/list.html"
    model = Project
    #projects = get_objects_for_user(request.user, 'projects.view_project')
    

class ProjectCreate(LoginRequiredMixin, CreateView):
    template_name = "project/form.html"
    model = Project
    fields = ['title', 'client_name', 'short_name', 'status']
    success_url = reverse_lazy('project-list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        project = form.save()
        assign_perm('view_project', self.request.user, project)
        return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    template_name = "project/form.html"
    model = Project
    fields = ['title', 'client_name', 'short_name', 'status']
    success_url = reverse_lazy('project-list')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project_id'] = self.object.id
        return context

@login_required(login_url="login")
def ProjectDelete(request, project_id):
    project = Project.objects.get(id=project_id)
    #note = get_object_or_404(Project, pk=note_id)
    project.delete()
    messages.success(request, 'Your project was successfully delete!')
    return HttpResponseRedirect(reverse('project-list'))










@login_required(login_url="login")
def ProjectNoteCreate(request, project_id):
    
    if request.method == 'POST':
        form = NoteForm(project_id, request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, 'Your note was successfully updated!')
            return HttpResponseRedirect(reverse('project-note-update', kwargs={'project_id':project_id,'note_id':note.id}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = NoteForm(project_id, initial={'project':project_id})
    return render(request, 'note/form.html', { 'form': form, 'project_id': project_id})



@login_required(login_url="login")
def ProjectNoteUpdate(request, project_id, note_id):
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        form = NoteForm(project_id, request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            messages.success(request, 'Your note was successfully updated!')
            return HttpResponseRedirect(reverse('project-note-update', kwargs={'project_id':project_id,'note_id':note.id}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        
        form = NoteForm(project_id, instance=note)
    return render(request, 'note/form.html', { 'form': form, 'project_id': project_id})


@login_required(login_url="login")
def ProjectNoteDelete(request, project_id, note_id):
    note = Note.objects.get(id=note_id)
    #note = get_object_or_404(Note, pk=note_id)
    note.delete()
    messages.success(request, 'Your note was successfully delete!')
    return HttpResponseRedirect(reverse('project-update', kwargs={'pk':project_id}))
    


@login_required(login_url="login")
def ProjectNoteUpload(request, project_id):
    return render(request, 'note/upload.html', { 'project_id': project_id})











def ProjectTaskList(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'task/list.html', { 'tasks': tasks, 'project_id': project_id})


@login_required(login_url="login")
def ProjectTaskCreate(request, project_id):
    
    if request.method == 'POST':
        form = TaskForm(project_id, request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Your task was successfully updated!')
            return HttpResponseRedirect(reverse('project-task-list', kwargs={'project_id':project_id}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = TaskForm(project_id, initial={'project':project_id})
    return render(request, 'task/form.html', { 'form': form, 'project_id': project_id})

@login_required(login_url="login")
def ProjectTaskUpdate(request, project_id, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = TaskForm(project_id, request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Your task was successfully updated!')
            return HttpResponseRedirect(reverse('project-task-list', kwargs={'project_id':project_id}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        
        form = TaskForm(project_id, instance=task)
    return render(request, 'task/form.html', { 'form': form, 'project_id': project_id})

@login_required(login_url="login")
def ProjectTaskDelete(request, project_id, note_id):
    note = Note.objects.get(id=note_id)
    #note = get_object_or_404(Note, pk=note_id)
    note.delete()
    messages.success(request, 'Your note was successfully delete!')
    return HttpResponseRedirect(reverse('project-update', kwargs={'pk':project_id}))
    







@login_required(login_url="login")
def ProjectReport(request, project_id):
    project = Project.objects.get(id=project_id)
    notes = Note.objects.filter(project=project, report=True)
    return render(request, 'project/report.html', { 'project': project, 'notes': notes })

















class NoteList(LoginRequiredMixin, ListView):
    model = Note

class NoteCreate(LoginRequiredMixin, CreateView):
    form_class = NoteForm
    model = Note
    #fields = ['title', 'note']
    success_url = reverse_lazy('note-list')

class NoteUpdate(LoginRequiredMixin, UpdateView):
    form_class = NoteForm
    model = Note
    #field = ['title', 'note']
    success_url = reverse_lazy('note-list')



