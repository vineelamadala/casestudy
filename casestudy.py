import csv
import threading
import time


lock = threading.Lock()


class Customer:
    def __init__(self, customer_id, name, account_balance, account_type):
        self.customer_id = customer_id
        self.name = name
        self.account_balance = account_balance
        self.account_type = account_type
        self.transactions = []

    def deposit(self, amount):
        self.account_balance += amount
        self.transactions.append(f'Deposit: {amount}')
        print(f'{amount} deposited. New balance: {self.account_balance}')

    def withdraw(self, amount):
        if amount <= self.account_balance:
            self.account_balance -= amount
            self.transactions.append(f'Withdrawal: {amount}')
            print(f'{amount} withdrawn. New balance: {self.account_balance}')
        else:
            print('Insufficient funds!')

    def view_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def apply_interest(self):
        if self.account_type == 'savings':
            interest = self.account_balance * 0.01  
            self.account_balance += interest
            self.transactions.append(f'Interest: {interest}')
            


def read_customer_data(file_name):
    customers = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            customer_id, name, account_balance = row
            customers.append(Customer(customer_id, name, float(account_balance), 'savings'))
    return customers


def periodic_interest_application(customers):
    while True:
        time.sleep(10)  # Apply interest every 10 seconds
        with lock:
            for customer in customers:
                customer.apply_interest()

# Main function
def main():
    customers = read_customer_data('Data.csv')
    interest_thread = threading.Thread(target=periodic_interest_application, args=(customers,), daemon=True)
    interest_thread.start()

    while True:
        print('1. Deposit')
        print('2. Withdraw')
        print('3. View Transactions')
        print('4. Exit')
        choice = int(input('Enter choice: '))
        
        customer_id = input('Enter customer ID: ')
        customer = next((c for c in customers if c.customer_id == customer_id), None)

        if not customer:
            print('Customer not found!')
            continue

        if choice == 1:
            amount = float(input('Enter amount to deposit: '))
            with lock:
                customer.deposit(amount)
        elif choice == 2:
            amount = float(input('Enter amount to withdraw: '))
            with lock:
                customer.withdraw(amount)
        elif choice == 3:
            customer.view_transactions()
        elif choice == 4:
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()
