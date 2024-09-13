from flask import Flask, jsonify, request
import mysql.connector 

app = Flask(__name__)

# Database configuration (replace with your actual RDS credentials)
db_config = {
    'user': 'your_db_user',  # Replace with your RDS username
    'password': 'your_db_password',  # Replace with your RDS password
    'host': 'your_db_host',  # Replace with your RDS endpoint
    'database': 'your_db_name'  # Replace with your database name
}

# Connect to RDS MySQL database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)  # Use 'psycopg2.connect' for PostgreSQL
    return conn

# Get wallet balance for a specific user
def get_wallet_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT balance FROM wallet WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return result[0]
    return None

# Update wallet balance
def update_wallet_balance(user_id, new_balance):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE wallet SET balance = %s WHERE user_id = %s"
    cursor.execute(query, (new_balance, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# Buy coins API
@app.route('/buy', methods=['POST'])
def buy_coin():
    data = request.json
    user_id = data['user_id']
    coin_type = data['coin_type']
    amount = data['amount']
    current_price = data['current_price']  # Price sent from the client
    total_cost = amount * current_price
    
    try:
        # Check wallet balance
        current_balance = get_wallet_balance(user_id)
        if current_balance is None or current_balance < total_cost:
            return jsonify({'status': 'error', 'message': 'Insufficient wallet balance'}), 400

        # Deduct total cost from wallet
        new_balance = current_balance - total_cost
        update_wallet_balance(user_id, new_balance)

        # Insert transaction record into the coin table
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO coin (user_id, coin_type, amount, transaction_type, price) VALUES (%s, %s, %s, %s, %s)"
        values = (user_id, coin_type, amount, 'buy', current_price)
        cursor.execute(query, values)
        conn.commit()

        return jsonify({'status': 'success', 'message': 'Coin bought successfully', 'new_balance': new_balance}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Sell coins API
@app.route('/sell', methods=['POST'])
def sell_coin():
    data = request.json
    user_id = data['user_id']
    coin_type = data['coin_type']
    amount = data['amount']
    current_price = data['current_price']  # Price sent from the client
    total_value = amount * current_price
    
    try:
        # Add total value to wallet
        current_balance = get_wallet_balance(user_id)
        new_balance = current_balance + total_value
        update_wallet_balance(user_id, new_balance)

        # Insert transaction record into the coin table
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO coin (user_id, coin_type, amount, transaction_type, price) VALUES (%s, %s, %s, %s, %s)"
        values = (user_id, coin_type, amount, 'sell', current_price)
        cursor.execute(query, values)
        conn.commit()

        return jsonify({'status': 'success', 'message': 'Coin sold successfully', 'new_balance': new_balance}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Add money to wallet API
@app.route('/add_money', methods=['POST'])
def add_money():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    
    try:
        # Get current wallet balance
        current_balance = get_wallet_balance(user_id)
        if current_balance is None:
            return jsonify({'status': 'error', 'message': 'User wallet not found'}), 400
        
        # Add the amount to wallet balance
        new_balance = current_balance + amount
        update_wallet_balance(user_id, new_balance)
        
        return jsonify({'status': 'success', 'message': 'Money added successfully', 'new_balance': new_balance}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
# Test route to ensure the API is running
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'success', 'message': 'API is running!'}), 200


# Withdraw money from wallet API
@app.route('/withdraw_money', methods=['POST'])
def withdraw_money():
    data = request.json
    user_id = data['user_id']
    amount = data['amount']
    
    try:
        # Get current wallet balance
        current_balance = get_wallet_balance(user_id)
        if current_balance is None:
            return jsonify({'status': 'error', 'message': 'User wallet not found'}), 400
        
        if current_balance < amount:
            return jsonify({'status': 'error', 'message': 'Insufficient balance to withdraw'}), 400
        
        # Deduct the amount from wallet balance
        new_balance = current_balance - amount
        update_wallet_balance(user_id, new_balance)
        
        return jsonify({'status': 'success', 'message': 'Money withdrawn successfully', 'new_balance': new_balance}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)