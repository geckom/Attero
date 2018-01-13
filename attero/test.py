import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Project


def create_project(title, client_name, short_name, status):
    """
    Create a project with the given `title`
    """
    return Project.objects.create(title=title, short_name=short_name, status=status)


class ProjectListTests(TestCase):
    def test_no_projects(self):
        """
        If no projects exist, an appropriate message is displayed.
        """
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('project-list'))

        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'project/list.html')

        #Check that initially we don't have any projects in list 
        self.assertTrue('object_list' in resp.context)
        self.assertEqual( len(resp.context['object_list']),0)

        # Check for no projects text
        self.assertContains(resp, "No projects are available.")

