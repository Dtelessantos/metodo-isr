from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulação de banco de dados em memória
transactions = []

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Rota principal (Home)
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html', transactions=transactions)

# Adicionar uma transação
@app.route('/add', methods=('GET', 'POST'))
def add_transaction():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        transaction = {
            'date': request.form['date'],
            'name': request.form['name'],
            'investment': float(request.form['investment']),
            'return_amount': float(request.form['return_amount']),
            'produced_accounts': int(request.form['produced_accounts']),
            'payment_per_account': float(request.form['payment_per_account']),
            'payment': float(request.form['produced_accounts']) * float(request.form['payment_per_account']),
        }
        transactions.append(transaction)
        return redirect(url_for('index'))
    return render_template('add_transaction.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    total_investment = sum(t['investment'] for t in transactions)
    total_return = sum(t['return_amount'] for t in transactions)
    total_payment = sum(t['payment'] for t in transactions)
    
    lucro = total_return - (total_payment + total_investment)

    return render_template('dashboard.html', total_investment=total_investment, total_return=total_return, total_payment=total_payment, lucro=lucro)

@app.route('/dashboard_data')
def dashboard_data():
    receitas = sum(t['return_amount'] for t in transactions)
    despesas = sum(t['payment'] for t in transactions)
    return jsonify([receitas, despesas])

if __name__ == '__main__':
    app.run(debug=True)
