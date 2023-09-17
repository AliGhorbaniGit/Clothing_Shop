from django.utils.translation import gettext as _
from django.contrib import messages


class ContactUs:

    def __init__(self, request):
        """    Initialize the cart  """

        self.request = request

        self.session = request.session

        contact = self.session.get('contact')
        self.i = 0

        if not contact:
            contact = self.session['contact'] = {}

        self.contact = contact

    def add(self, user_txt=None, admin_txt=None):
        """    Add the specified product to the cart if it exists     """

        self.contact['user_txt'] = {'user_txt': user_txt}
        self.contact['admin_txt'] = {'admin_txt': admin_txt}

        messages.success(self.request, _('your comment send , be patient to get answer'))

        self.save()

    def save(self):
        """   Mark session as modified to save changes   """

        self.session.modified = True

    def __iter__(self):
        """ make the cart iterable   """
        contact_ids = self.contact.values()

        for item in contact_ids:
            yield item

    def clear(self):
        del self.session['contact']
        self.save()
