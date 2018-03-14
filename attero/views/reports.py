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




from docxtpl import *
import re
from django.conf import settings


@login_required()
def ProjectReport(request, project_id):
    project = Project.objects.get(id=project_id)
    notes = Note.objects.filter(project=project, report=True)

    if project.report_template == None:
        return render(request, 'project/report.html', { 'project': project, 'notes': notes })

    doc = DocxTemplate(project.report_template.document)


    docnotes = []
    for note in notes:
        startsentence = note.note
	
        latexbold = re.compile(r'\<b\>(.*)\<\/b\>')
        x = re.split(latexbold, startsentence.replace('<p>','').replace('</p>',"\n\n"))
        rt = RichText()
        l = len(x)
        for i in range(0,l):
            if i%2 == 0:
                rt.add(x[i])
            else:
                rt.add(x[i], bold=True)


        docnotes.append({
		'title': note.title,
		'note':  rt
	})


    context = {
            'title' : project.title,
            'company_name' : "World company",
            'notes' : docnotes
    }

    file_path = os.path.join(settings.MEDIA_ROOT, "generated_doc.docx")

    doc.render(context)
    doc.save(file_path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404





class ReportTemplateList(LoginRequiredMixin, ListView):
    template_name = "report_template/list.html"
    model = ReportTemplate
    #projects = get_objects_for_user(request.user, 'projects.view_project')
    

class ReportTemplateCreate(LoginRequiredMixin, CreateView):
    template_name = "report_template/form.html"
    model = ReportTemplate
    fields = ['name', 'document']
    success_url = reverse_lazy('report-template-list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        object = form.save()
        return super().form_valid(form)

class ReportTemplateUpdate(LoginRequiredMixin, UpdateView):
    template_name = "report_template/form.html"
    model = ReportTemplate
    fields = ['name', 'document']
    success_url = reverse_lazy('report-template-list')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['project_id'] = 3
        return context

@login_required()
def ReportTemplateDelete(request, report_template_id):
    reporttemplate = ReportTemplate.objects.get(id=report_template_id)
    #note = get_object_or_404(Project, pk=note_id)
    reporttemplate.delete()
    messages.success(request, 'Your project was successfully delete!')
    return HttpResponseRedirect(reverse('report-template-list'))



