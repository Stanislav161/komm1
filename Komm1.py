class UtilityPaymentsTracker:
    def __init__(self):
        self.payments = {}

    def add_payment(self, service, amount, date):
        if service not in self.payments:
            self.payments[service] = []
        self.payments[service].append((amount, date))
        print(f"Добавлен платеж: {service} - {amount} руб. ({date})")

    def show_payments(self, service=None):
        if not self.payments:
            print("Платежей пока нет.")
            return

        if service:
            if service in self.payments:
                print(f"\nПлатежи за {service}:")
                for i, (amount, date) in enumerate(self.payments[service], 1):
                    print(f"{i}. {amount} руб. - {date}")
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
            print("2. Показать все платежи")
            print("3. Показать платежи по услуге")
            print("4. Общая сумма платежей")
            print("5. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                service = input("Введите название услуги (электричество, вода и т.д.): ")
                amount = float(input("Введите сумму платежа: "))
                date = input("Введите дату платежа (дд.мм.гггг): ")
                self.add_payment(service, amount, date)
            elif choice == "2":
                self.show_payments()
            elif choice == "3":
                service = input("Введите название услуги: ")
                self.show_payments(service)
            elif choice == "4":
                self.total_spent()
            elif choice == "5":
                print("Выход из программы.")
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")


if __name__ == "__main__":
    tracker = UtilityPaymentsTracker()
    tracker.menu()