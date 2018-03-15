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
    


from django.db import transaction
from django.core import serializers
import xmltodict
from libnmap.parser import NmapParser
from mptt.forms import TreeNodeChoiceField

@login_required()
def ProjectNoteUpload(request, project_id):
    data = ''
    # Output scan in normal, XML, s|<rIpt kIddi3, and Grepable format, respectively, to the given filename.
    import_types = [
            'Plain Text',
            'Nmap'
    ]
    data_structures = [
        'Raw Note Data',
        'Folder Structure'
    ]

    #notes = Note.objects.filter(project=project_id)
    notes = TreeNodeChoiceField(queryset=Note.objects.filter(project=project_id))

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        rawdata = myfile.read().decode('utf-8')
    
        import_type = request.POST.get('import_type')
        structure = request.POST.get('structure')
        parentid = request.POST.get('parentid')
        if(parentid==''):
            parentid = None
        else:
            parentid = Note.objects.get(id=parentid)

        if( import_type =='Plain Text' and structure=='Raw Note Data'):
            data = "Importing... " + str(myfile)
            newnote = Note(
                    title = str(myfile),
                    note = "<br />".join(rawdata.split("\n")),
                    project = Project.objects.get(id=project_id),
                    parent = parentid
            )
            newnote.save()
        elif( import_type == 'Nmap' and structure=='Raw Note Data'):
            data = "Importing... " + str(myfile)
            newnote = Note(
                    title = str(myfile),
                    note = "<pre>"+rawdata+"</pre>",
                    project = Project.objects.get(id=project_id),
                    parent = parentid
            )
            newnote.save()
        elif( import_type == 'Nmap' and structure=='Folder Structure'):
            nmap_report = NmapParser.parse_fromstring(rawdata)
            data += "Nmap scan summary: {0}\n\n".format(nmap_report.summary)
            with transaction.atomic():
                for host in nmap_report.hosts:
                    data += "Importing " + host.address + "\n"
                    note = ''
                    if len(host.hostnames)>0:
                        note = "Hostnames: " + ", ".join(host.hostnames) + "\n"
                    if host.mac != '':
                        note += "MAC Address: " + host.mac + "\n"
                    if host.vendor != '':
                        note += "Vendor: " + host.vendor + "\n"
                    if host.os_fingerprinted:
                        note += "Operating System: " + str(host.os_match_probabilities()[0]) + "\n"
                    if len(host.scripts_results)>0:
                        note += "Scripts:\n"
                        for script in host.scripts_results:
                            note += str(script) + "\n"
                    note += "Serivices:\n"
                    for service in host.services:
                        note += str(service.port) + "/" + str(service.protocol) + " " + service.state + "\n"
                        if len(service.scripts_results)>0:
                            for scripts in service.scripts_results:
                                note += scripts['id'] + ":\n"
                                note += str(scripts['output']) + "\n"
                            
                    #data += "======================\n" + note + "=======================\n"
                    
                    newhost = Note(
                            project = Project.objects.get(id=project_id),
                            title = host.address,
                            note = "<br />".join(note.split("\n")),
                            parent = parentid
                    )
                    newhost.save()


                    data += "Ports " + ', '.join(str(i[0])+"/"+i[1] for i in host.get_ports()) + "\n\n"
                    for service in host.services:
                        title = str(service.port) + "/" + service.protocol + " " + service.service
                        note = service.banner
                        if len(service.scripts_results)>0:
                            for scripts in service.scripts_results:
                                note += scripts['id'] + ":\n"
                                note += str(scripts['output']) + "\n"

                    #for port in host.get_ports():
                    #    service = host.get_service(port[0], port[1])
                    #    title = str(port[0]) + "/" + port[1] + " " + str(service.service) + "\n"
                        data += service.banner + "\n"

                        newport = Note(
                                project = Project.objects.get(id=project_id),
                                title = title,
                                note = "<br />".join(note.split("\n")),
                                parent = newhost
                        )
                        newport.save()

        else:
            data = "Unable to import:\n" + rawdata

    context = {
            'project_id': project_id,
            'import_types': import_types,
            'data_structures': data_structures,
            'notes': notes,
            'data': data
    }
    return render(request, 'note/upload.html', context)





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
