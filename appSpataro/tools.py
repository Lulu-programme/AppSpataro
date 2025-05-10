import datetime

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


def convert_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d') if date else None


def convert_hour(hour):
    return datetime.datetime.strptime(hour, '%H:%M') if hour else None