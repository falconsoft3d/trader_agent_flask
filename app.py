from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from analysis import StockAnalyzer
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(16))
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Middleware to check auth
def is_authenticated():
    return session.get('authenticated') is True

@app.route('/', methods=['GET', 'POST'])
def login():
    if is_authenticated():
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        if password == APP_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if ticker:
            return redirect(url_for('result', ticker=ticker))
            
    return render_template('index.html')

@app.route('/result/<ticker>')
def result(ticker):
    if not is_authenticated():
        return redirect(url_for('login'))
        
    analyzer = StockAnalyzer(ticker)
    fetched = analyzer.fetch_data()
    
    if not fetched:
        flash(f"Could not fetch data for {ticker}. Is it a valid symbol?", "error")
        return redirect(url_for('dashboard'))
        
    analysis_result = analyzer.analyze()
    
    if "error" in analysis_result:
        flash(analysis_result['error'], "error")
        return redirect(url_for('dashboard'))
        
    return render_template('result.html', data=analysis_result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
