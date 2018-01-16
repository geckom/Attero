from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from guardian.admin import GuardedModelAdmin


# Register your models here.

from .models import Note
class NoteAdmin(MPTTModelAdmin, SummernoteModelAdmin):  # instead of ModelAdmin
    summer_note_fields = ('note',)
admin.site.register(Note, NoteAdmin)


from .models import Project
admin.site.register(Project,GuardedModelAdmin)


from .models import Task
admin.site.register(Task)


from .models import ReportTemplate
admin.site.register(ReportTemplate)
