from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        group, created = Group.objects.get_or_create(name='profile_manager')

        permission_profile = Permission.objects.get(codename="view_profile")
        permission_logentry = Permission.objects.get(codename="view_logentry")

        # Add permissions to the group
        group.permissions.add(permission_profile)
        group.permissions.add(permission_logentry)

        # Add the user to the group
        user.groups.add(group)

        # Assign permission directly to the user
        user.user_permissions.add(permission_logentry)

        # Save the changes
        group.save()
        user.save()
