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


from ..models import *
from ..forms import *

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin


def TaskList(request):
    tasks = Task.objects.all()
    return render(request, 'task/all.html', { 'tasks': tasks})




def ProjectTaskList(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'task/list.html', { 'tasks': tasks, 'project_id': project_id})


@login_required()
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

@login_required()
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

@login_required()
def ProjectTaskDelete(request, project_id, note_id):
    note = Note.objects.get(id=note_id)
    #note = get_object_or_404(Note, pk=note_id)
    note.delete()
    messages.success(request, 'Your note was successfully delete!')
    return HttpResponseRedirect(reverse('project-update', kwargs={'pk':project_id}))
    
