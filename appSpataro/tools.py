import re
import datetime

sector_list_factory = [
    'Parking',
    'Lavage',
    'Chimie',
    'Gaz',
    'Distribution',
]
sector_list_daytime = [
    'Chimie',
    'Gaz',
    'Distribution',
]
sector_list_signup = [
    'Administration',
    'Chimie',
    'Gaz',
    'Distribution',
]
country_list = [
    'Belgique',
    'France',
    'Allemagne',
    'Pays-Bas',
    'Luxembourg',
    'Italie',
    'Suisse',
]
provision_list = [
    'Café',
    'Douche',
    'Toilette',
    'Distributeur',
    'Salle d\'attente',
    'Atelier mécanique',
    'Espace fumeur',
]
language_list = [
    'Français',
    'Anglais',
    'Néerlandais',
    'Allemand',
    'Italien',
    'Espagnol',
    'Polonais',
]
reception_list = [
    'Sympathique',
    'Correct',
    'Inexistant',
]
labels_list = [
    '2.1',
    '2.2',
    '2.3',
    '3',
    '4.1',
    '4.2',
    '4.3',
    '5.1',
    '5.2',
    '6.1',
    '6.2',
    '8',
    '9',
    'Environnement',
    'Température',
    'Pas ADR',
]
months_to_search = [
    'Jan',
    'Fév',
    'Mars',
    'Avr',
    'Mai',
    'Juin',
    'Juil',
    'Août',
    'Sept',
    'Oct',
    'Nov',
    'Déc',
]
months_entries = [
    'Janvier',
    'Février',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
    'Juillet',
    'Août',
    'Septembre',
    'Octobre',
    'Novembre',
    'Décembre',
]
emojis = {
    'truck': '🚛',
    'hello': '👋',
    'dont': '🤷',
    'wrong': '🚧',
    'delivery': '🚚',
    'worker': '👷‍♂️',
    'force': '💪',
    'good': '👍',
    'delete': '🗑️',
    'lets_go': '🚀',
    'arrival': '🏁',
    'gas': '⛽',
}
vowel = [
    "A",
    "E",
    "I",
    "O",
    "U",
    "Y",
]


def convert_seconds(seconds: int, string: bool) -> str | tuple[int, int]:
    """Convertisseur de seconde en minutes"""

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if string:
        return f'{hours:02}h{minutes:02}'
    return hours, minutes


def hours_seconds(hours: int, minutes: int) -> int:
    """On convertit les heures et les minutes en secondes"""

    return (hours * 3600) + (minutes * 60)


def calculate_laps_time(hour_start: int, hour_end: int, minute_start: int, minute_end: int, string: bool) -> str | int:
    """Calcul le temps passé entre 2 heures"""

    if hour_end < hour_start or (hour_end == hour_start and minute_end < minute_start):
        hour_end += 24
    second_start = hours_seconds(hour_start, minute_start)
    second_end = hours_seconds(hour_end, minute_end)
    seconds = second_end - second_start
    if string:
        return convert_seconds(seconds, string)
    return seconds


def description_p(description: str) -> list:
    """Formate le texte en paragraphe et ajoute des balise HTML"""

    paragraphs = description.split('.')
    formatted = []
    for para in paragraphs:
        para = re.sub(r'\((.*?)\)', r'<span class="marked">(\1)</span>', para.strip())
        if para:
            formatted.append(para.capitalize() + '.')
    return formatted


def change_text_to_list(to_change: str, cut: str, ending: str, number: bool) -> list:
    """Change un texte en liste en tenant compte des séparateurs et de la fin du texte"""

    changed = []
    last_modified = 0
    for i in range(len(to_change)):
        if to_change[i] == cut or to_change[i] == ending:
            if number:
                change = int(to_change[last_modified:i])
            else:
                word = to_change[last_modified:i]
                change = word.strip().capitalize()
            changed.append(change)
            last_modified = i + 1
    return changed


def change_list_to_text(to_change: list, ending: str, cut: str) -> str:
    """Change un liste en texte, en lui indiquant un séparateur et la fin"""

    return f'{cut} '.join([change for change in to_change]) + ending


def zip_town(country: str, zip_code: str, city: str) -> str:
    """Permet l'affichage structuré du pays, du code postal et de la ville"""

    country_codes: dict = {
        'PAYS-BAS': 'NL',
        'ITALIE': 'IT',
        'ALLEMAGNE': 'D',
        'SUISSE': 'CH',
    }
    code: str = country_codes.get(country.upper(), country[0])
    return f'{code} - {zip_code} {city}'


def change_weight(weight: int) -> int:
    """Converti un poids inférieur en supérieur"""

    if weight < 0:
        return int(str(weight)[1:])
    return weight


def convert_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d') if date else None


def convert_hour(hour):
    return datetime.datetime.strptime(hour, '%H:%M') if hour else None


def format_phone_number(phone: str, country: str) -> str:
    """Ajoute l'indicatif international au numéro de téléphone s'il n'est pas présent"""

    country_codes = {
        'Belgique': '+32',
        'France': '+33',
        'Allemagne': '+49',
        'Pays-Bas': '+31',
        'Luxembourg': '+352',
        'Italie': '+39',
        'Suisse': '+41',
    }

    phone = phone.strip().replace(' ', '').replace('-', '')

    if not phone.startswith('+'):
        if phone.startswith('0'):
            phone = country_codes.get(country) + phone[1:]
        else:
            phone = country_codes.get(country) + phone

    return phone