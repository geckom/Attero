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
class TemplateList(LoginRequiredMixin, ListView):
    #permission_required = 'attero.view_project'
    template_name = "template/list.html"
    model = NoteTemplate
    form_class = TemplateForm
    

class TemplateCreate(LoginRequiredMixin, CreateView):
    template_name = "template/form.html"
    form_class = TemplateForm
    model = NoteTemplate
    #fields = ['title', 'note']
    success_url = reverse_lazy('template-list')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        template = form.save()
        return super().form_valid(form)

class TemplateUpdate(LoginRequiredMixin, UpdateView):
    template_name = "template/form.html"
    model = NoteTemplate
    form_class = TemplateForm
    #fields = ['title', 'note']
    success_url = reverse_lazy('template-list')
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['project_id'] = self.object.id
        return context

@login_required()
def TemplateDelete(request, project_id):
    template = NoteTemplate.objects.get(id=template_id)
    template.delete()
    messages.success(request, 'Your template was successfully delete!')
    return HttpResponseRedirect(reverse('template-list'))

from django.http import JsonResponse
from django.core import serializers
def JSONNoteTemplate(request):
    template_id = request.GET.get('template_id', None)
    data = {}
    if(template_id):
        obj = NoteTemplate.objects.get(id=template_id)
        data = serializers.serialize("json", [obj], fields=('title', 'note'))

    return JsonResponse(data, safe=False)



