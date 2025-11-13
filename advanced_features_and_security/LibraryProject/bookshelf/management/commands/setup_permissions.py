from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, Library


class Command(BaseCommand):
    help = 'Setup groups and assign permissions for the bookshelf application'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('Setting up groups and permissions...'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Get content types
        book_ct = ContentType.objects.get_for_model(Book)
        library_ct = ContentType.objects.get_for_model(Library)
        
        # Get permissions for Book model
        book_permissions = {
            'can_view': Permission.objects.get(codename='can_view', content_type=book_ct),
            'can_create': Permission.objects.get(codename='can_create', content_type=book_ct),
            'can_edit': Permission.objects.get(codename='can_edit', content_type=book_ct),
            'can_delete': Permission.objects.get(codename='can_delete', content_type=book_ct),
        }
        
        # Get permissions for Library model
        library_permissions = {
            'can_view': Permission.objects.get(codename='can_view', content_type=library_ct),
            'can_create': Permission.objects.get(codename='can_create', content_type=library_ct),
            'can_edit': Permission.objects.get(codename='can_edit', content_type=library_ct),
            'can_delete': Permission.objects.get(codename='can_delete', content_type=library_ct),
        }
        
        # ====================================================================
        # Setup Viewers Group
        # ====================================================================
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            viewers_group.permissions.add(
                book_permissions['can_view'],
                library_permissions['can_view']
            )
            self.stdout.write(self.style.SUCCESS('✓ Created Viewers group'))
            self.stdout.write('  Permissions: can_view (Books and Libraries)')
        else:
            self.stdout.write(self.style.WARNING('  Viewers group already exists'))
        
        # ====================================================================
        # Setup Editors Group
        # ====================================================================
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            editors_group.permissions.add(
                book_permissions['can_view'],
                book_permissions['can_create'],
                book_permissions['can_edit'],
                library_permissions['can_view'],
                library_permissions['can_create'],
                library_permissions['can_edit']
            )
            self.stdout.write(self.style.SUCCESS('✓ Created Editors group'))
            self.stdout.write('  Permissions: can_view, can_create, can_edit (Books and Libraries)')
        else:
            self.stdout.write(self.style.WARNING('  Editors group already exists'))
        
        # ====================================================================
        # Setup Admins Group
        # ====================================================================
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            admins_group.permissions.add(
                book_permissions['can_view'],
                book_permissions['can_create'],
                book_permissions['can_edit'],
                book_permissions['can_delete'],
                library_permissions['can_view'],
                library_permissions['can_create'],
                library_permissions['can_edit'],
                library_permissions['can_delete']
            )
            self.stdout.write(self.style.SUCCESS('✓ Created Admins group'))
            self.stdout.write('  Permissions: ALL (Books and Libraries)')
        else:
            self.stdout.write(self.style.WARNING('  Admins group already exists'))
        
        # Display summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ Setup completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write(self.style.SUCCESS('\nGroup Summary:'))
        self.stdout.write(f'  • Viewers:  {viewers_group.permissions.count()} permissions')
        self.stdout.write(f'  • Editors:  {editors_group.permissions.count()} permissions')
        self.stdout.write(f'  • Admins:   {admins_group.permissions.count()} permissions')
        
        self.stdout.write(self.style.SUCCESS('\nPermission Details:'))
        self.stdout.write('  Viewers: Can VIEW books and libraries')
        self.stdout.write('  Editors: Can VIEW, CREATE, EDIT books and libraries')
        self.stdout.write('  Admins:  Can VIEW, CREATE, EDIT, DELETE books and libraries')
        
        self.stdout.write(self.style.SUCCESS('\nNext Steps:'))
        self.stdout.write('  1. Create test users (if needed):')
        self.stdout.write('     python manage.py createsuperuser')
        self.stdout.write('  2. Assign users to groups in Django admin at:')
        self.stdout.write('     http://127.0.0.1:8000/admin/')
        self.stdout.write('  3. Or assign programmatically:')
        self.stdout.write("     user.groups.add(Group.objects.get(name='Editors'))")
        self.stdout.write('  4. Run tests:')
        self.stdout.write('     python manage.py test bookshelf')
        self.stdout.write(self.style.SUCCESS('='*60))