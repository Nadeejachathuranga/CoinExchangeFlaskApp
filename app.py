from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated wallet balance and transaction records for demo
wallet_balance = 1000.0
transactions = []  # List to store all transaction records

# Get wallet balance (no user_id needed)
def get_wallet_balance():
    print(f"Fetching wallet balance: {wallet_balance}")
    return wallet_balance

# Update wallet balance (no user_id needed)
def update_wallet_balance(new_balance):
    global wallet_balance
    wallet_balance = new_balance
    print(f"Updated wallet balance: {wallet_balance}")

# Add transaction to the list (no DB interaction)
def add_transaction(user_id, coin_type, amount, transaction_type, price):
    transaction = {
        'user_id': user_id,
        'coin_type': coin_type,
        'amount': amount,
        'transaction_type': transaction_type,
        'price': price
    }
    transactions.append(transaction)
    print(f"Added transaction: {transaction}")

# Buy coins API
@app.route('/buy', methods=['POST'])
def buy_coin():
    data = request.json
    coin_type = data['coin_type']
    amount = data['amount']
    current_price = data['current_price']
    total_cost = amount * current_price

    print(f"Received request to buy coins: coin_type={coin_type}, amount={amount}, current_price={current_price}")
   
    # Check wallet balance
    current_balance = get_wallet_balance()
    if current_balance < total_cost:
        return jsonify({'status': 'error', 'message': 'Insufficient wallet balance'}), 400

    # Deduct total cost and update wallet balance
    new_balance = current_balance - total_cost
    update_wallet_balance(new_balance)

    # Simulate transaction (add to transactions list)
    add_transaction('demo_user', coin_type, amount, 'buy', current_price)

    return jsonify({'status': 'success', 'message': 'Coin bought successfully', 'new_balance': new_balance}), 200

# Sell coins API
@app.route('/sell', methods=['POST'])
def sell_coin():
    data = request.json
    coin_type = data['coin_type']
    amount = data['amount']
    current_price = data['current_price']
    total_value = amount * current_price

    print(f"Received request to sell coins: coin_type={coin_type}, amount={amount}, current_price={current_price}")

    # Add total value to wallet balance
    current_balance = get_wallet_balance()
    new_balance = current_balance + total_value
    update_wallet_balance(new_balance)

    # Simulate transaction (add to transactions list)
    add_transaction('demo_user', coin_type, amount, 'sell', current_price)

    return jsonify({'status': 'success', 'message': 'Coin sold successfully', 'new_balance': new_balance}), 200

# Add money to wallet API (no user_id needed)
@app.route('/add_money', methods=['POST'])
def add_money():
    data = request.json
    amount = data['amount']

    print(f"Received request to add money: amount={amount}")
   
    # Add the amount to wallet balance
    current_balance = get_wallet_balance()
    new_balance = current_balance + amount
    update_wallet_balance(new_balance)
   
    return jsonify({'status': 'success', 'message': 'Money added successfully', 'new_balance': new_balance}), 200

# Withdraw money from wallet API (no user_id needed)
@app.route('/withdraw_money', methods=['POST'])
def withdraw_money():
    data = request.json
    amount = data['amount']

    print(f"Received request to withdraw money: amount={amount}")
   
    # Get current balance and deduct the amount
    current_balance = get_wallet_balance()
    if current_balance < amount:
        return jsonify({'status': 'error', 'message': 'Insufficient balance to withdraw'}), 400

    new_balance = current_balance - amount
    update_wallet_balance(new_balance)
   
    return jsonify({'status': 'success', 'message': 'Money withdrawn successfully', 'new_balance': new_balance}), 200

# API to get all transactions (buy and sell records)
@app.route('/transactions', methods=['GET'])
def get_transactions():
    print("Fetching all transactions")
    return jsonify({'status': 'success', 'transactions': transactions}), 200

# Test route to ensure the API is running
@app.route('/test', methods=['GET'])
def test():
    print("Test route called.")
    return jsonify({'status': 'success', 'message': 'API is running!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
