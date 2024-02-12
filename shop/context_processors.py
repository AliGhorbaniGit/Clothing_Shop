from .models import AdminAwareness


def admin_awareness(request):
    admin_awareness = AdminAwareness.objects.filter(is_checked=False)
    return {'admin_awareness': admin_awareness}
