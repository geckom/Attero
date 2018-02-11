from django.forms import ModelForm

#from treebeard.forms import MoveNodeForm
#from treebeard.forms import movenodeform_factory
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


from .models import Note
from .models import Project
from .models import Task
from .models import NoteTemplate

class NoteForm(ModelForm):
    def __init__(self, project_id, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields["parent"].queryset = Note.objects.filter(project=project_id)

    class Meta:
        model = Note
        exclude = ('pub_date',)
        #fields = ['title', 'note', 'project', 'parent']
        widgets = {
                'note': SummernoteWidget(),
            }

class TemplateForm(ModelForm):
#    def __init__(self, *args, **kwargs):
#        super(TemplateForm, self).__init__(*args, **kwargs)
#        self.fields["parent"].queryset = Note.objects()

    class Meta:
        model = NoteTemplate
        exclude = ('pub_date',)
        #fields = ['title', 'note', 'parent']
        widgets = {
                'note': SummernoteWidget(),
            }

class TaskForm(ModelForm):
    def __init__(self, project_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["parent"].queryset = Task.objects.filter(project=project_id)

    class Meta:
        model = Task
        exclude = ('pub_date',)
        #fields = ['name', 'project', 'parent']

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm    

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)
