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




@login_required()
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



@login_required()
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


@login_required()
def ProjectNoteDelete(request, project_id, note_id):
    note = Note.objects.get(id=note_id)
    #note = get_object_or_404(Note, pk=note_id)
    note.delete()
    messages.success(request, 'Your note was successfully delete!')
    return HttpResponseRedirect(reverse('project-update', kwargs={'pk':project_id}))
    


@login_required()
def ProjectNoteUpload(request, project_id):
    return render(request, 'note/upload.html', { 'project_id': project_id})





from mptt.templatetags.mptt_tags import cache_tree_children
from django.http import HttpResponse

@login_required()
def noteMenu(request, project_id):
    project = Project.objects.get(id=project_id)
    root_nodes = cache_tree_children(Note.objects.filter(project=project))
    dicts = []
    for n in root_nodes:
        dicts.append(recursive_node_to_dict(n))

    return HttpResponse(json.dumps(dicts, indent=4), content_type='application/json')

import json


def recursive_node_to_dict(node):
    result = {
        'id': node.pk,
        'name': node.title,
        'url': reverse('project-note-update', kwargs={'project_id': node.project.id, 'note_id': node.pk}),

    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result











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
