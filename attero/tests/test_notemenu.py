import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

from ..models import Project, Note, Task


class NotesMenuTests(TestCase):
    def login(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('dashboard'))

        #Check our user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that we got a response "success"
        self.assertEqual(resp.status_code, 200)

    def test_json_menu_data_not_logged_in(self):
        """
        Check if you can get project data when not logged in through the menu json request.
        """
        #self.login()
        test_project = Project.objects.create(title='TestTitle', short_name='TestShortName', status='open')
        test_note = Note.objects.create(title='TestNote', note='Testing', report=False, project=test_project)

	# Goto the json note menu
        resp = self.client.get(reverse('note-menu', kwargs={'project_id': test_project.id}))

	# Check there was a 302 redirect to the login page
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], '/login?next=/json/notes/' + str(test_note.id) + '/')

	# Check that the note is not returned
        #self.assertNotContains(resp, test_note.title)


    def test_json_menu_data_when_logged_in(self):
        """
        Check if you can get project data when not logged in through the menu json request.
        """
        self.login()
        test_project = Project.objects.create(title='TestTitle', short_name='TestShortName', status='open')
        test_note = Note.objects.create(title='TestNote', note='Testing', report=False, project=test_project)

	# Goto the json note menu
        resp = self.client.get(reverse('note-menu', kwargs={'project_id': test_project.id}))

	# Check there was a 200 response code
        self.assertEqual(resp.status_code, 200)

	# Check that the note is not returned
        self.assertContains(resp, test_note.title)
        self.assertContains(resp, "\"name\": \"" + test_note.title + "\"")
        self.assertContains(resp, "\"id\": " + str(test_note.id))
