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


#@login_required()
class ProjectList(LoginRequiredMixin, PermissionListMixin, ListView):
    permission_required = 'attero.view_project'
    template_name = "project/list.html"
    model = Project
    #projects = get_objects_for_user(request.user, 'projects.view_project')
    

class ProjectCreate(LoginRequiredMixin, CreateView):
    template_name = "project/form.html"
    model = Project
    fields = ['title', 'client_name', 'short_name', 'status', 'report_template']
    success_url = reverse_lazy('project-list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        project = form.save()
        assign_perm('view_project', self.request.user, project)
        return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    template_name = "project/form.html"
    model = Project
    fields = ['title', 'client_name', 'short_name', 'status', 'report_template']
    success_url = reverse_lazy('project-list')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['project_id'] = self.object.id
        return context

@login_required()
def ProjectDelete(request, project_id):
    project = Project.objects.get(id=project_id)
    #note = get_object_or_404(Project, pk=note_id)
    project.delete()
    messages.success(request, 'Your project was successfully delete!')
    return HttpResponseRedirect(reverse('project-list'))


from django.core import serializers
@login_required()
def ProjectExport(request, project_id):
    all_objects = list({Project.objects.get(id=project_id)})#  + list(Note.objects.all())
    all_objects += list(Note.objects.all().filter(project=project_id))
    all_objects += list(Task.objects.all().filter(project=project_id))
    data = serializers.serialize("json", all_objects, indent=2)
    context = {
        'data': data
    }


    response = HttpResponse(data, content_type="text/plain; charset=UTF-8")
    response['Content-Disposition'] = 'attachment; filename=project.json'
    return response
#return render(request, 'project/export.html', context)


from django.db import transaction

@login_required()
def ProjectImport(request):
    data =''
    if request.method == 'POST' and request.FILES['myfile']:

        myfile = request.FILES['myfile']
        #fs = FileSystemStorage()
        #filename = fs.save(myfile.name, 'uploads/projects/'+myfile)
	#uploaded_file_url = fs.url(filename)
        #data =filename
        jsondata = myfile.read().decode('utf-8')
        #with open(myfile) as f:
        #    data = f.read()

        project_id = 0
        new_project = None
        id_mapping = {}
        with transaction.atomic():
            for obj in serializers.deserialize("json", jsondata):
                if isinstance(obj.object, Project):
                    data += "Insert project: " + str(obj.object.pk) + ":" + str(obj.object) + "\n"
                    obj.object.pk = None
                    obj.object.save()
                    project_id = obj.object.pk
                    new_project = obj.object
                    data += "New Project ID: " + str(project_id) + "\n"
                elif isinstance(obj.object, Note):
                    data += "Insert note: " + str(obj.object.title) + "\n"
                    importobj = obj.object.__dict__

                    new_parent = None
                    if importobj['parent_id'] != None :
                        if importobj['parent_id'] in id_mapping:
                            #obj.object.parent = id_mapping[importobj['parent_id']]
                            new_parent = id_mapping[importobj['parent_id']]

                    newobj = Note(
                            title= importobj['title'],
                            note= importobj['note'],
                            report= importobj['report'],
                            project= new_project,
                            parent= new_parent,
                            added= importobj['added'],
                            updated= importobj['updated'],
                    )
                    newobj.save()
                    new_id = newobj.pk

                    id_mapping[importobj['id']] = newobj
        #data += str(id_mapping)
    
    context = {
            'data': data
    }

    return render(request, 'project/import.html', context)


