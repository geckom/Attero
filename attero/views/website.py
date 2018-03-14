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
            'completed_tasks' : completed_tasks,
    }
    return render(request, 'pages/dashboard.html', context)

@login_required()
def Settings(request):
    context = {}
    return render(request, 'pages/settings.html', context)


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
@login_required()
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



@login_required()
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






@login_required()
class IndexView(generic.ListView):
    template_name = 'pages/index.html'
    context_object_name = 'latest_note_list'

    def get_queryset(self):
        """Return the last five published notes."""
        return Note.objects.order_by('-pub_date')[:5]




