from django.test import TestCase

"""
Comprehensive unit tests for permissions and groups functionality.
Tests all permission levels for the bookshelf application.

Run with: python manage.py test bookshelf
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Book, Library


class PermissionsSetupTestCase(TestCase):
    """Test that custom permissions are properly defined."""
    
    def test_book_permissions_exist(self):
        """Test that custom permissions exist for Book model."""
        book_ct = ContentType.objects.get_for_model(Book)
        
        # Check all custom permissions exist
        self.assertTrue(Permission.objects.filter(
            codename='can_view', content_type=book_ct
        ).exists())
        self.assertTrue(Permission.objects.filter(
            codename='can_create', content_type=book_ct
        ).exists())
        self.assertTrue(Permission.objects.filter(
            codename='can_edit', content_type=book_ct
        ).exists())
        self.assertTrue(Permission.objects.filter(
            codename='can_delete', content_type=book_ct
        ).exists())
    
    def test_library_permissions_exist(self):
        """Test that custom permissions exist for Library model."""
        library_ct = ContentType.objects.get_for_model(Library)
        
        # Check all custom permissions exist
        self.assertTrue(Permission.objects.filter(
            codename='can_view', content_type=library_ct
        ).exists())
        self.assertTrue(Permission.objects.filter(
            codename='can_create', content_type=library_ct
        ).exists())
        self.assertTrue(Permission.objects.filter(
            codename='can_edit', content_type=library_ct
        ).exists())
        self.assertTrue(Permission.objects.filter(
            codename='can_delete', content_type=library_ct
        ).exists())


class ViewerPermissionsTestCase(TestCase):
    """Test case for Viewers group permissions."""
    
    def setUp(self):
        """Set up test data for viewer tests."""
        # Create viewer user
        self.viewer = User.objects.create_user('viewer', 'viewer@test.com', 'pass123')
        
        # Get content type and permissions
        book_ct = ContentType.objects.get_for_model(Book)
        can_view = Permission.objects.get(codename='can_view', content_type=book_ct)
        
        # Create and configure Viewers group
        viewers_group = Group.objects.create(name='Viewers')
        viewers_group.permissions.add(can_view)
        
        # Assign user to group
        self.viewer.groups.add(viewers_group)
        
        # Create test book
        admin_user = User.objects.create_user('admin_temp', 'admin@test.com', 'pass123')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2024,
            created_by=admin_user
        )
        
        # Create client
        self.client = Client()
    
    def test_viewer_can_view_book_list(self):
        """Test that viewers can view book list."""
        self.client.login(username='viewer', password='pass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_viewer_can_view_book_detail(self):
        """Test that viewers can view book details."""
        self.client.login(username='viewer', password='pass123')
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_viewer_cannot_create_book(self):
        """Test that viewers cannot create books."""
        self.client.login(username='viewer', password='pass123')
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 403)
    
    def test_viewer_cannot_edit_book(self):
        """Test that viewers cannot edit books."""
        self.client.login(username='viewer', password='pass123')
        response = self.client.get(reverse('book_edit', args=[self.book.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_viewer_cannot_delete_book(self):
        """Test that viewers cannot delete books."""
        self.client.login(username='viewer', password='pass123')
        response = self.client.get(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_viewer_has_correct_permissions(self):
        """Test that viewer has only can_view permission."""
        self.assertTrue(self.viewer.has_perm('bookshelf.can_view'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_create'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_edit'))
        self.assertFalse(self.viewer.has_perm('bookshelf.can_delete'))


class EditorPermissionsTestCase(TestCase):
    """Test case for Editors group permissions."""
    
    def setUp(self):
        """Set up test data for editor tests."""
        # Create editor user
        self.editor = User.objects.create_user('editor', 'editor@test.com', 'pass123')
        
        # Get content type and permissions
        book_ct = ContentType.objects.get_for_model(Book)
        can_view = Permission.objects.get(codename='can_view', content_type=book_ct)
        can_create = Permission.objects.get(codename='can_create', content_type=book_ct)
        can_edit = Permission.objects.get(codename='can_edit', content_type=book_ct)
        
        # Create and configure Editors group
        editors_group = Group.objects.create(name='Editors')
        editors_group.permissions.add(can_view, can_create, can_edit)
        
        # Assign user to group
        self.editor.groups.add(editors_group)
        
        # Create test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2024,
            created_by=self.editor
        )
        
        # Create client
        self.client = Client()
    
    def test_editor_can_view_books(self):
        """Test that editors can view books."""
        self.client.login(username='editor', password='pass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_editor_can_create_book(self):
        """Test that editors can create books."""
        self.client.login(username='editor', password='pass123')
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_editor_can_edit_book(self):
        """Test that editors can edit books."""
        self.client.login(username='editor', password='pass123')
        response = self.client.get(reverse('book_edit', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_editor_cannot_delete_book(self):
        """Test that editors cannot delete books."""
        self.client.login(username='editor', password='pass123')
        response = self.client.get(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 403)
    
    def test_editor_has_correct_permissions(self):
        """Test that editor has view, create, and edit permissions."""
        self.assertTrue(self.editor.has_perm('bookshelf.can_view'))
        self.assertTrue(self.editor.has_perm('bookshelf.can_create'))
        self.assertTrue(self.editor.has_perm('bookshelf.can_edit'))
        self.assertFalse(self.editor.has_perm('bookshelf.can_delete'))
    
    def test_editor_can_post_new_book(self):
        """Test that editor can successfully create a book via POST."""
        self.client.login(username='editor', password='pass123')
        response = self.client.post(reverse('book_create'), {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2024,
            'description': 'A test book'
        })
        
        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)
        
        # Verify book was created
        self.assertTrue(Book.objects.filter(title='New Book').exists())


class AdminPermissionsTestCase(TestCase):
    """Test case for Admins group permissions."""
    
    def setUp(self):
        """Set up test data for admin tests."""
        # Create admin user
        self.admin = User.objects.create_user('testadmin', 'admin@test.com', 'pass123')
        
        # Get content type and permissions
        book_ct = ContentType.objects.get_for_model(Book)
        can_view = Permission.objects.get(codename='can_view', content_type=book_ct)
        can_create = Permission.objects.get(codename='can_create', content_type=book_ct)
        can_edit = Permission.objects.get(codename='can_edit', content_type=book_ct)
        can_delete = Permission.objects.get(codename='can_delete', content_type=book_ct)
        
        # Create and configure Admins group
        admins_group = Group.objects.create(name='Admins')
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        
        # Assign user to group
        self.admin.groups.add(admins_group)
        
        # Create test book
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2024,
            created_by=self.admin
        )
        
        # Create client
        self.client = Client()
    
    def test_admin_can_view_books(self):
        """Test that admins can view books."""
        self.client.login(username='testadmin', password='pass123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_create_book(self):
        """Test that admins can create books."""
        self.client.login(username='testadmin', password='pass123')
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_edit_book(self):
        """Test that admins can edit books."""
        self.client.login(username='testadmin', password='pass123')
        response = self.client.get(reverse('book_edit', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_delete_book(self):
        """Test that admins can delete books."""
        self.client.login(username='testadmin', password='pass123')
        response = self.client.get(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_has_all_permissions(self):
        """Test that admin has all permissions."""
        self.assertTrue(self.admin.has_perm('bookshelf.can_view'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_create'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_edit'))
        self.assertTrue(self.admin.has_perm('bookshelf.can_delete'))
    
    def test_admin_can_delete_book_post(self):
        """Test that admin can successfully delete a book via POST."""
        self.client.login(username='testadmin', password='pass123')
        book_id = self.book.pk
        
        response = self.client.post(reverse('book_delete', args=[book_id]))
        
        # Should redirect after successful deletion
        self.assertEqual(response.status_code, 302)
        
        # Verify book was deleted
        self.assertFalse(Book.objects.filter(pk=book_id).exists())


class UnauthenticatedUserTestCase(TestCase):
    """Test that unauthenticated users cannot access protected views."""
    
    def setUp(self):
        """Set up test data."""
        admin_user = User.objects.create_user('admin', 'admin@test.com', 'pass123')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2024,
            created_by=admin_user
        )
        self.client = Client()
    
    def test_unauthenticated_redirected_from_list(self):
        """Test that unauthenticated users are redirected from book list."""
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_unauthenticated_redirected_from_detail(self):
        """Test that unauthenticated users are redirected from book detail."""
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_unauthenticated_redirected_from_create(self):
        """Test that unauthenticated users are redirected from create view."""
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class GroupMembershipTestCase(TestCase):
    """Test group membership functionality."""
    
    def test_user_can_be_in_multiple_groups(self):
        """Test that a user can belong to multiple groups."""
        user = User.objects.create_user('multigroup', 'multi@test.com', 'pass123')
        
        viewers = Group.objects.create(name='Viewers')
        editors = Group.objects.create(name='Editors')
        
        user.groups.add(viewers, editors)
        
        self.assertTrue(user.groups.filter(name='Viewers').exists())
        self.assertTrue(user.groups.filter(name='Editors').exists())
        self.assertEqual(user.groups.count(), 2)
    
    def test_group_has_correct_users(self):
        """Test that groups contain the correct users."""
        user1 = User.objects.create_user('user1', 'user1@test.com', 'pass123')
        user2 = User.objects.create_user('user2', 'user2@test.com', 'pass123')
        
        editors = Group.objects.create(name='Editors')
        editors.user_set.add(user1, user2)
        
        self.assertEqual(editors.user_set.count(), 2)
        self.assertIn(user1, editors.user_set.all())
        self.assertIn(user2, editors.user_set.all())
