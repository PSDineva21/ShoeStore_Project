from datetime import datetime
from abc import ABC, abstractmethod


class UserNotification:

    def __init__(self, id, user_id, title, message, notification_type, is_read=False):
        self._id = id
        self._user_id = user_id
        self._title = title
        self._message = message
        self._type = notification_type
        self._is_read = is_read
        self._created_at = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def title(self):
        return self._title

    @property
    def message(self):
        return self._message

    @property
    def type(self):
        return self._type

    @property
    def is_read(self):
        return self._is_read

    @property
    def created_at(self):
        return self._created_at

    def mark_as_read(self):
        self._is_read = True


class NotificationObserver(ABC):
    @abstractmethod
    def update(self, user, message_type, data):
        pass


class EmailNotification(NotificationObserver):
    def update(self, user, message_type, data):
        if message_type == "registration":
            self._send_welcome_email(user)
        elif message_type == "order":
            self._send_order_confirmation(user, data)
        elif message_type == "low_stock":
            self._send_low_stock_alert(user, data)

    def _send_welcome_email(self, user):
        print(f"   Изпращане  на имейл до: {user.email}")
        print(f"   Съдържание: Добре дошли в нашия магазин за обувки!")

    def _send_order_confirmation(self, user, order):
        print(f"   Изпращане на имейл до: {user.email}")
        print(f"   Съдържание: Вашата поръчка #{order.id} е получена!")


class NotificationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationService, cls).__new__(cls)
            cls._instance._observers = []
            cls._instance._notifications = []
            cls._instance._next_id = 1
            cls._instance._initialize_observers()
        return cls._instance

    def _initialize_observers(self):
        self.add_observer(EmailNotification())

    def add_observer(self, observer):
        if isinstance(observer, NotificationObserver):
            self._observers.append(observer)

    def notify(self, user, message_type, data):
        print(f"\n=== СИСТЕМА ЗА ИЗВЕСТЯВАНЕ ===")
        for observer in self._observers:
            observer.update(user, message_type, data)


        if message_type == "registration":
            self.create_user_notification(
                user.id,
                "Добре дошли!",
                "Успешна регистрация в магазина за обувки.",
                "success"
            )
        elif message_type == "order":
            self.create_user_notification(
                user.id,
                "Поръчката ви е приета!",
                f"Поръчка #{data.id} е получена. Обща сума: {data.total:.2f} лв.",
                "info"
            )
        print("=== КРАЙ НА ИЗВЕСТЯВАНЕТО ===\n")

    def create_user_notification(self, user_id, title, message, notification_type="info"):
        notification = UserNotification(self._next_id, user_id, title, message, notification_type)
        self._next_id += 1
        self._notifications.append(notification)
        return notification

    def get_user_notifications(self, user_id, limit=None):
        user_notifications = [n for n in self._notifications if n.user_id == user_id]
        user_notifications.sort(key=lambda x: x.created_at, reverse=True)

        if limit:
            return user_notifications[:limit]
        return user_notifications

    def get_unread_count(self, user_id):
        return len([n for n in self._notifications if n.user_id == user_id and not n.is_read])

    def mark_as_read(self, notification_id, user_id):
        for notification in self._notifications:
            if notification.id == notification_id and notification.user_id == user_id:
                notification.mark_as_read()
                return True
        return False

    def mark_all_as_read(self, user_id):
        for notification in self._notifications:
            if notification.user_id == user_id and not notification.is_read:
                notification.mark_as_read()
        return True


notification_service = NotificationService()