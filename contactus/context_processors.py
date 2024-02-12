from .models import ContactUs


def contact(request):
    contact = ContactUs.objects.filter(is_new=True)
    return {'contact': contact}
