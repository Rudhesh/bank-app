from flask import Flask, render_template, request, redirect, url_for, session, flash
from bank import BankAccount
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for session and flash messages

# In-memory storage for bank accounts. Keys are usernames, values are BankAccount objects
accounts = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        action = request.form.get('action')
        name = request.form.get('name')
        pin = request.form.get('pin')
        
        if action == 'login':
            if name in accounts:
                if accounts[name].verify_pin(pin):
                    session['username'] = name
                    return redirect(url_for('dashboard'))
                else:
                    flash('Incorrect PIN.', 'error')
            else:
                flash('Account not found.', 'error')
                
        elif action == 'create':
            if not name or not pin:
                flash('Please provide both name and PIN.', 'error')
            elif len(pin) != 4 or not pin.isdigit():
                flash('PIN must be exactly 4 digits.', 'error')
            elif name in accounts:
                flash('An account with this name already exists.', 'error')
            else:
                accounts[name] = BankAccount(name, pin)
                session['username'] = name
                flash('Account created successfully!', 'success')
                return redirect(url_for('dashboard'))
                
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    account = accounts[session['username']]
    return render_template('dashboard.html', account=account)

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    account = accounts[session['username']]
    try:
        amount = float(request.form.get('amount'))
        if amount > 0:
            account.deposit(amount)
            flash(f'Successfully deposited ${amount:.2f}', 'success')
        else:
            flash('Deposit amount must be positive.', 'error')
    except ValueError:
        flash('Invalid amount entered.', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    account = accounts[session['username']]
    try:
        amount = float(request.form.get('amount'))
        if amount > 0:
            if account.balance >= amount:
                account.withdraw(amount)
                flash(f'Successfully withdrew ${amount:.2f}', 'success')
            else:
                flash(f'Insufficient funds. Current balance: ${account.balance:.2f}', 'error')
        else:
            flash('Withdrawal amount must be positive.', 'error')
    except ValueError:
        flash('Invalid amount entered.', 'error')
        
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
