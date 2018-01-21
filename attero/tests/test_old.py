import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from guardian.shortcuts import assign_perm

from ..models import Project, Note, Task



class NoteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        project = Project.objects.create(title='Test Project', client_name='Test Industries', short_name='TP')
        Note.objects.create(title='Test Note', note='This is a note', project=project, report=False)


class AllTaskListTests(TestCase):
    def test_no_projects(self):
        """
        If no tasks exist, an appropriate message is displayed.
        """
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('task-list'))

        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(resp, 'task/all.html')

        #Check that initially we don't have any tasks in list 
        self.assertTrue('tasks' in resp.context)
        self.assertEqual( len(resp.context['tasks']),0)

        # Check for no tasks text
        self.assertContains(resp, "No tasks are available.")

