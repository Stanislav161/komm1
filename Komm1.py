import datetime
from collections import defaultdict


class PaymentReminder:
    def __init__(self):
        self.reminders = defaultdict(list)

    def add_reminder(self, service, expected_amount, due_date, period_days=None):
        """Добавляет напоминание о платеже"""
        reminder = {
            'service': service,
            'expected_amount': expected_amount,
            'due_date': due_date,
            'period_days': period_days,
            'is_paid': False
        }
        self.reminders[service].append(reminder)
        print(f"Напоминание добавлено: {service} до {due_date}")

    def check_reminders(self):
        """Проверяет и показывает предстоящие платежи"""
        today = datetime.date.today()
        upcoming = []
        overdue = []

        for service, reminders in self.reminders.items():
            for reminder in reminders:
                if reminder['is_paid']:
                    continue

                due_date = reminder['due_date']
                if due_date >= today:
                    upcoming.append(reminder)
                else:
                    overdue.append(reminder)

        return upcoming, overdue

    def mark_as_paid(self, service, date=None):
        """Отмечает платеж как оплаченный"""
        if service in self.reminders:
            for reminder in self.reminders[service]:
                if not reminder['is_paid'] and (date is None or reminder['due_date'] == date):
                    reminder['is_paid'] = True
                    print(f"Платеж {service} отмечен как оплаченный")
                    return
        print(f"Не найдено неоплаченных напоминаний для {service}")


class UtilityPaymentsTracker:
    def __init__(self):
        self.payments = {}
        self.reminder = PaymentReminder()

    def add_payment(self, service, amount, date):
        if service not in self.payments:
            self.payments[service] = []
        payment_date = self._parse_date(date)
        self.payments[service].append((amount, payment_date))

        # Проверяем, есть ли напоминание для этого платежа
        self.reminder.mark_as_paid(service, payment_date)

        print(f"Добавлен платеж: {service} - {amount} руб. ({payment_date.strftime('%d.%m.%Y')})")

    def add_reminder(self, service, expected_amount, due_date, period_days=None):
        """Добавляет напоминание о предстоящем платеже"""
        due_date = self._parse_date(due_date)
        self.reminder.add_reminder(service, expected_amount, due_date, period_days)

    def show_reminders(self):
        """Показывает предстоящие и просроченные платежи"""
        upcoming, overdue = self.reminder.check_reminders()

        print("\n=== Напоминания ===")

        if overdue:
            print("\n⚠️ Просроченные платежи:")
            for reminder in overdue:
                print(f"- {reminder['service']}: {reminder['expected_amount']} руб. "
                      f"(было до {reminder['due_date'].strftime('%d.%m.%Y')})")

        if upcoming:
            print("\nПредстоящие платежи:")
            for reminder in upcoming:
                days_left = (reminder['due_date'] - datetime.date.today()).days
                print(f"- {reminder['service']}: {reminder['expected_amount']} руб. "
                      f"(до {reminder['due_date'].strftime('%d.%m.%Y')}, осталось {days_left} дней)")

        if not upcoming and not overdue:
            print("Нет активных напоминаний.")

    def _parse_date(self, date_str):
        """Преобразует строку даты в объект date"""
        try:
            return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка формата даты. Используйте ДД.ММ.ГГГГ")
            return datetime.date.today()

    def show_payments(self, service=None):
        if not self.payments:
            print("Платежей пока нет.")
            return

        if service:
            if service in self.payments:
                print(f"\nПлатежи за {service}:")
                for i, (amount, date) in enumerate(self.payments[service], 1):
                    print(f"{i}. {amount} руб. - {date.strftime('%d.%m.%Y')}")
            else:
                print(f"Платежей за {service} не найдено.")
        else:
            print("\nВсе платежи:")
            for service, payments in self.payments.items():
                total = sum(amount for amount, date in payments)
                print(f"{service}: {len(payments)} платежей, всего {total} руб.")

    def total_spent(self):
        total = sum(amount for payments in self.payments.values() for amount, date in payments)
        print(f"\nВсего потрачено на коммунальные услуги: {total} руб.")
        return total

    def menu(self):
        while True:
            print("\n=== Учет коммунальных платежей ===")
            print("1. Добавить платеж")
            print("2. Добавить напоминание о платеже")
            print("3. Показать все платежи")
            print("4. Показать платежи по услуге")
            print("5. Показать напоминания")
            print("6. Общая сумма платежей")
            print("7. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                service = input("Введите название услуги (электричество, вода и т.д.): ")
                amount = float(input("Введите сумму платежа: "))
                date = input("Введите дату платежа (дд.мм.гггг): ")
                self.add_payment(service, amount, date)
            elif choice == "2":
                service = input("Введите название услуги: ")
                amount = float(input("Введите ожидаемую сумму: "))
                date = input("Введите дату, до которой нужно оплатить (дд.мм.гггг): ")
                period = input("Периодичность в днях (оставьте пустым, если не повторяется): ")
                period_days = int(period) if period else None
                self.add_reminder(service, amount, date, period_days)
            elif choice == "3":
                self.show_payments()
            elif choice == "4":
                service = input("Введите название услуги: ")
                self.show_payments(service)
            elif choice == "5":
                self.show_reminders()
            elif choice == "6":
                self.total_spent()
            elif choice == "7":
                print("Выход из программы.")
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")


if __name__ == "__main__":
    tracker = UtilityPaymentsTracker()

    # Добавим тестовые данные
    tracker.add_reminder("Электричество", 1500, "10.04.2024")
    tracker.add_reminder("Вода", 800, "05.04.2024")
    tracker.add_reminder("Газ", 700, "15.04.2024")

    tracker.menu()