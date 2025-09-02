from django.shortcuts import render

from django.utils.translation import gettext as _

def home_view(request):
    context = {
        'page_title': _('Bienvenu sur Spataro'),
        'welcome_text': _('Ceci est une page de bienvenue.')
    }
    return render(request, 'core/home.html', context)
