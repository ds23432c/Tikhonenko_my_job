from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Инициализация данных'

    def handle(self, *args, **kwargs):
        from apps.gamification.models import Achievement, ShopItem

        self.stdout.write('🏆 Создаём достижения...')
        achievements_data = [
            {'title': 'Первый шаг', 'description': 'Выполни первую задачу', 'icon': '👣', 'category': 'tasks', 'condition_type': 'tasks_completed', 'condition_value': 1, 'xp_reward': 20, 'coins_reward': 10},
            {'title': 'Продуктивный день', 'description': 'Выполни 5 задач', 'icon': '⚡', 'category': 'tasks', 'condition_type': 'tasks_completed', 'condition_value': 5, 'xp_reward': 50, 'coins_reward': 25},
            {'title': 'Машина дел', 'description': 'Выполни 25 задач', 'icon': '🤖', 'category': 'tasks', 'condition_type': 'tasks_completed', 'condition_value': 25, 'xp_reward': 100, 'coins_reward': 50},
            {'title': 'Легенда продуктивности', 'description': 'Выполни 100 задач', 'icon': '🏆', 'category': 'tasks', 'condition_type': 'tasks_completed', 'condition_value': 100, 'xp_reward': 300, 'coins_reward': 150},
            {'title': 'Неделя без пропуска', 'description': 'Серия 7 дней', 'icon': '🔥', 'category': 'streak', 'condition_type': 'streak', 'condition_value': 7, 'xp_reward': 70, 'coins_reward': 35},
            {'title': 'Месяц активности', 'description': 'Серия 30 дней', 'icon': '💪', 'category': 'streak', 'condition_type': 'streak', 'condition_value': 30, 'xp_reward': 300, 'coins_reward': 150},
            {'title': 'Помодоро новичок', 'description': 'Заверши 5 помодоро', 'icon': '🍅', 'category': 'pomodoro', 'condition_type': 'pomodoros', 'condition_value': 5, 'xp_reward': 30, 'coins_reward': 15},
            {'title': 'Помодоро мастер', 'description': 'Заверши 50 помодоро', 'icon': '🍅🍅', 'category': 'pomodoro', 'condition_type': 'pomodoros', 'condition_value': 50, 'xp_reward': 150, 'coins_reward': 75},
            {'title': 'Уровень 3', 'description': 'Достигни 3-го уровня', 'icon': '⬆️', 'category': 'special', 'condition_type': 'level', 'condition_value': 3, 'xp_reward': 50, 'coins_reward': 25},
            {'title': 'Уровень 5', 'description': 'Достигни 5-го уровня', 'icon': '🌟', 'category': 'special', 'condition_type': 'level', 'condition_value': 5, 'xp_reward': 100, 'coins_reward': 50},
            {'title': 'Уровень 10', 'description': 'Достигни максимального уровня', 'icon': '👑', 'category': 'special', 'condition_type': 'level', 'condition_value': 10, 'xp_reward': 500, 'coins_reward': 250},
            {'title': 'Первые 100 XP', 'description': 'Набери 100 очков опыта', 'icon': '✨', 'category': 'special', 'condition_type': 'xp', 'condition_value': 100, 'xp_reward': 10, 'coins_reward': 5},
            {'title': '1000 XP', 'description': 'Набери 1000 очков опыта', 'icon': '💎', 'category': 'special', 'condition_type': 'xp', 'condition_value': 1000, 'xp_reward': 50, 'coins_reward': 25},
        ]
        for data in achievements_data:
            Achievement.objects.get_or_create(title=data['title'], defaults=data)

        self.stdout.write('🛍️ Создаём магазин...')
        shop_items = [
            {'name': 'Тема «Океан»', 'description': 'Синие тона, спокойствие', 'item_type': 'theme', 'icon': '🌊', 'price_coins': 50, 'value': 'ocean'},
            {'name': 'Тема «Лес»', 'description': 'Зелёные тона, природа', 'item_type': 'theme', 'icon': '🌲', 'price_coins': 50, 'value': 'forest'},
            {'name': 'Тема «Закат»', 'description': 'Тёплые тона, энергия', 'item_type': 'theme', 'icon': '🌅', 'price_coins': 75, 'value': 'sunset'},
            {'name': 'Тема «Галактика»', 'description': 'Тёмно-фиолетовая, космос', 'item_type': 'theme', 'icon': '🌌', 'price_coins': 100, 'value': 'galaxy'},
            {'name': 'Рамка «Золото»', 'description': 'Золотая рамка для аватара', 'item_type': 'avatar_frame', 'icon': '🥇', 'price_coins': 150, 'value': 'gold_frame'},
            {'name': 'Значок «Звезда»', 'description': 'Звёздочка рядом с именем', 'item_type': 'badge', 'icon': '⭐', 'price_coins': 80, 'value': 'star_badge'},
            {'name': 'Значок «Огонь»', 'description': 'Значок для ценителей серий', 'item_type': 'badge', 'icon': '🔥', 'price_coins': 120, 'value': 'fire_badge'},
        ]
        for item in shop_items:
            ShopItem.objects.get_or_create(name=item['name'], defaults=item)

        self.stdout.write(self.style.SUCCESS('✅ Данные инициализированы!'))
