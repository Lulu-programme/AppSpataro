from deep_translator import GoogleTranslator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from appSpataro.tools import emojis, convert_date, sector_list_signup, format_phone_number
from authentication.models import Account, Truck

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
    truck = truck_list.filter(license=request.user.truck).first() if request.user.truck else None

    # Initialisation du context
    context = {
        'title': 'Tableau de bord',
        'drivers': drivers_list if drivers_list else None,
        'trucks': truck_list if truck_list else None,
        'name_user': name,
        'truck_user': truck,
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

@user_passes_test(lambda user: user.is_staff)
def signup_page(request):

    data = {
        'username': '',
        'password': '',
        'first_name': '',
        'last_name': '',
        'sector': '',
        'truck': '',
        'drive_license': '',
        'adr_license': '',
        'driver_card': '',
        'email': '',
        'phone': '',
        'city': '',
        'is_staff': '',
    }

    context = {
        'title': 'Ajouter un chauffeur',
        'trucks': Truck.objects.all(),
        'sectors': sector_list_signup,
    }

    if request.method == 'POST':

        if request.POST['password1'] == request.POST['password2']:

            try:
                data['username'] = request.POST.get('username')
                data['password'] = request.POST.get('password1')
                data['first_name'] = request.POST.get('first_name').capitalize()
                data['last_name'] = request.POST.get('last_name').capitalize()
                data['sector'] = request.POST.get('sector')
                data['truck'] = request.POST.get('truck')
                data['drive_license'] = convert_date(request.POST.get('drive_license'))
                data['adr_license'] = convert_date(request.POST.get('adr_license'))
                data['driver_card'] = convert_date(request.POST.get('card_drive'))
                data['email'] = request.POST.get('email')
                data['phone'] = format_phone_number(request.POST.get('phone'), 'Belgique')
                data['city'] = request.POST.get('city').capitalize()
                data['is_staff'] = bool(int(request.POST.get('is_staff')))

                # Création du camion
                Account.objects.create_user(**data)

                messages.success(request, f'L\'utilisateur {data.get('first_name')} {data.get('last_name')} à bien été créé {emojis.get('worker')}')

                return redirect('profile')

            except ValueError as e:

                # Gestion des erreurs de conversion
                error = GoogleTranslator(source='auto', target='fr').translate(str(e))
                messages.error(request, f'{emojis.get('wrong')} Erreur lors de l\'inscription : {error}')
        else:
            messages.error(request, f'{emojis.get('wrong')} Les mots de passe ne correspondent pas')

    return render(request, 'authentication/signup.html', context)

@login_required
def change_date(request, to_modify):
    user = Account.objects.get(username=request.user.username)
    truck = None
    if user.truck:
        truck = Truck.objects.filter(license=user.truck).first()

    mapping_modify = {
        'drive_license': 'du permis de conduire',
        'adr_license': 'du permis ADR',
        'driver_card': 'de la carte chauffeur',
        'technical': 'du contrôle technique',
        'tachograph': 'du contrôle tachygraphe',
        'maintenance': 'de l\'entretien',
        'adr': 'du contrôle ADR',
    }

    if request.method == 'POST':
        new_value_str = request.POST.get(to_modify)

        new_value = convert_date(new_value_str)

        user_modifiable_fields = ['drive_license', 'adr_license', 'driver_card']
        truck_modifiable_fields = ['technical', 'tachograph', 'maintenance', 'adr']

        if to_modify in user_modifiable_fields:
            setattr(user, to_modify, new_value)
            user.save()
        elif to_modify in truck_modifiable_fields:
            if truck:
                setattr(truck, to_modify, new_value)
                truck.save()
            else:
                messages.error(request, f"Avertissement : Camion non trouvé pour la mise à jour du champ '{mapping_modify.get(to_modify)}'.")
        else:
            messages.error(request, f"Avertissement : Le champ '{mapping_modify.get(to_modify)}' n'est pas reconnu ou non modifiable.")

        messages.success(request, f'Date {mapping_modify.get(to_modify)} à bien été modifié {emojis.get("good")}.')
        return redirect('profile')

    context = {
        'title': f'Modifier la date {mapping_modify.get(to_modify)}.',
        'user': user,
        'truck': truck,
        'to_modify': to_modify,
    }

    return render(request, 'authentication/change_date.html', context)

