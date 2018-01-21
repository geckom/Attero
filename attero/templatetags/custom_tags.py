from django import template
from django.template import Template

register = template.Library()

from ..models import Project,Note

@register.filter
def to_class_name(value):
    return value.__class__.__name__



@register.inclusion_tag('modules/notemenu.html')
def show_notes(Project):
    return {'project_id': Project}
    #root_nodes = cache_tree_children(Note.objects.filter(project=Project))
    #dicts = []
    #for n in root_nodes:
    #    dicts.append(recursive_node_to_dict(n))
    #return {'nodes': json.dumps(dicts, indent=4)}

    #notedata = Note.objects.filter(project=Project)
    #return {'nodes': notedata}

@register.inclusion_tag('modules/projectdata.html')
def project_data(project_id):
    project = Project.objects.get(id=project_id)
    return {'project': project}

@register.inclusion_tag('modules/projectlist.html')
def projects_list():
    projects = Project.objects.filter(status='open')
    return {'projects': projects}

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='filterproject')
def filterproject(form_field, arg):
    return form_field

