import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Project, Note, Task


class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Project.objects.create(title='Test Project', client_name='Test Industries', short_name='TP')

    def test_title_label(self):
        project=Project.objects.get(id=1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_title_length(self):
        project=Project.objects.get(id=1)
        max_length = project._meta.get_field('title').max_length
        self.assertEquals(max_length,255)

    def test_client_name_label(self):
        project=Project.objects.get(id=1)
        field_label = project._meta.get_field('client_name').verbose_name
        self.assertEquals(field_label,'client name')

    def test_clienit_name_length(self):
        project=Project.objects.get(id=1)
        max_length = project._meta.get_field('client_name').max_length
        self.assertEquals(max_length,255)



class NoteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        project = Project.objects.create(title='Test Project', client_name='Test Industries', short_name='TP')
        Note.objects.create(title='Test Note', note='This is a note', project=project, report=False)

class ProjectListTests(TestCase):
    def test_no_projects_page(self):
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

    def test_with_projects_page(self):
        test_project = Project.objects.create(title='TestTitle', short_name='TestShortName', status='open')

	# Loing and goto the project list page
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('project-list'))

        # Check for no projects text
        self.assertNotContains(resp, "No projects are available.")
        self.assertContains(resp, "TestTitle")
        self.assertContains(resp, "TestShortName")
        self.assertContains(resp, "Open")




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

