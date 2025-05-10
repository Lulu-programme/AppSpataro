from deep_translator import GoogleTranslator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from authentication.models import Account, Truck

from appSpataro.tools import emojis, convert_date

data_truck = {
        'license': '',
        'technical': '',
        'tachograph': '',
        'maintenance': '',
        'adr': '',
        'weight': 0,
    }


def login_page(request):
    context = {
        'title': 'Connexion'
    }
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            messages.success(
                request,
                f'Bonjour {user.get_full_name() if user.get_full_name() else "Fantôme As"}, '
                f'bonne journée {emojis.get('good')} {emojis.get('truck')}')
            return redirect('profile')
        else:
            messages.error(request, f'{emojis.get('wrong')} Utilisateur ou mot de passe inconnu au bataillon {emojis.get('dont')}')
    return render(request, 'authentication/login.html', context)


@login_required
def profile(request):

    # Importation des bases de données
    drivers_list = Account.objects.filter(is_superuser=False, deleted=False).order_by('last_name')
    truck_list = Truck.objects.filter(deleted=False).order_by('license')
    name = request.user.get_full_name() if request.user.get_full_name() else 'Fantôme as'

    # Initialisation du context
    context = {
        'title': 'Tableau de bord',
        'drivers': drivers_list if drivers_list else None,
        'trucks': truck_list if truck_list else None,
        'name_user': name,
    }

    return render(request, 'authentication/profile.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, f'À la prochaine {emojis.get('hello')}')
    return redirect('login')

@user_passes_test(lambda user: user.is_staff)
def add_truck(request):

    context = {
        'title': 'Ajouter un camion'
    }

    data = data_truck.copy()

    if request.method == 'POST':

        try:
            data['license'] = request.POST.get('license', '').upper()
            data['technical'] = convert_date(request.POST.get('technical'))
            data['tachograph'] = convert_date(request.POST.get('tachograph'))
            data['maintenance'] = convert_date(request.POST.get('maintenance'))
            data['adr'] = convert_date(request.POST.get('adr'))
            data['weight'] = int(request.POST.get('weight'))

            # Création du camion
            Truck.objects.create(**data)

            messages.success(request, f'Le camion {data.get('license')} à bien été enregistré {emojis.get('delivery')}')

            return redirect('profile')

        except ValueError as e:

            # Gestion des erreurs de conversion
            error = GoogleTranslator(source='auto', target='fr').translate(str(e))
            messages.error(request, f"{emojis.get('wrong')} Erreur lors de l'ajout du camion : {error}")

    return render(request, 'authentication/truck.html', context)
