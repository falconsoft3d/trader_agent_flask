from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from analysis import StockAnalyzer
import secrets
import concurrent.futures
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(16))
APP_PASSWORD = os.getenv("APP_PASSWORD")
REQUIRE_LOGIN = os.getenv("REQUIRE_LOGIN", "true").lower() == "true"

# In-memory cache for analysis results to avoid cookie size limits
RESULTS_CACHE = {}

def is_authenticated():
    if not REQUIRE_LOGIN:
        return True
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
            flash('Contraseña incorrecta', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not is_authenticated():
        return redirect(url_for('login'))
    
    popular_stocks = [
        "TSLA", "NVDA", "AMD", "AAPL", "AMZN", "MSFT", "META", "GOOGL", "NFLX", "COIN",
        "MARA", "RIOT", "PLTR", "SOFI", "LCID", "RIVN", "NIO", "BABA", "PDD", "JD",
        "TQQQ", "SQQQ", "SPY", "QQQ", "IWM", "UVXY", "LABU", "SOXL", "SOXS", "F",
        "BAC", "DIS", "PYPL", "SQ", "ROKU", "DKNG", "UBER", "LYFT", "HOOD", "GME",
        "AMC", "BB", "NOK", "SNDL", "TLRY", "CGC", "CRSP", "MRNA", "PFE", "XOM",
        "CVX", "OXY", "MRO", "HAL", "SLB", "JPM", "GS", "MS", "C", "WFC",
        "BA", "AAL", "DAL", "UAL", "LUV", "CCL", "RCL", "NCLH", "MGM", "LVS",
        "WYNN", "INTC", "MU", "QCOM", "TXN", "AVGO", "ADBE", "CRM", "ORCL", "IBM",
        "SNOW", "DDOG", "NET", "TEAM", "ZM", "DOCU", "TWLO", "SPOT", "PINS", "SNAP",
        "BIDU", "TCEHY", "XPEV", "LI", "FUTU", "TIGR", "UPST", "AFRM", "AI", "CVNA"
    ]

    # Forex pairs (Yahoo Finance format: EURUSD=X)
    forex = [
        "EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X", "GBPJPY=X",
        "EURGBP=X", "EURCAD=X", "EURSEK=X", "EURCHF=X", "CHF=X", "CAD=X", "HKD=X", "SEK=X"
    ]

    # Crypto (Yahoo Finance format: BTC-USD)
    crypto = [
        "BTC-USD", "ETH-USD", "USDT-USD", "BNB-USD", "SOL-USD", "XRP-USD", "USDC-USD", "ADA-USD",
        "AVAX-USD", "DOGE-USD", "TRX-USD", "LINK-USD", "DOT-USD", "MATIC-USD", "LTC-USD", "SHIB-USD",
        "UNI7083-USD", "OKB-USD", "ATOM-USD", "XLM-USD", "XMR-USD", "ETC-USD", "FIL-USD", "HBAR-USD"
    ]

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if ticker:
            return redirect(url_for('result', ticker=ticker))
        
        selected_tickers = request.form.getlist('selected_tickers')
        if selected_tickers:
            results = []
            
            def analyze_one(t):
                try:
                    a = StockAnalyzer(t)
                    if a.fetch_data():
                        return a.analyze()
                except:
                    pass
                return None

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_ticker = {executor.submit(analyze_one, t): t for t in selected_tickers}
                for future in concurrent.futures.as_completed(future_to_ticker):
                    try:
                        res = future.result()
                        if res and "error" not in res:
                            results.append(res)
                    except:
                        pass
            
            if not results:
                flash("No se pudieron obtener datos para las acciones seleccionadas.", "error")
                return redirect(url_for('dashboard'))

            # Sort by "Clarity" (Confidence)
            results.sort(
                key=lambda x: abs(x['summary']['up_votes'] - x['summary']['down_votes']), 
                reverse=True
            )
            
            # Save to CACHE
            analysis_id = str(uuid.uuid4())
            RESULTS_CACHE[analysis_id] = results
            
            return redirect(url_for('multi_result', analysis_id=analysis_id, page=0))
            
    return render_template('index.html', stocks=popular_stocks, forex=forex, crypto=crypto)

@app.route('/multi_result/<analysis_id>/<int:page>')
def multi_result(analysis_id, page):
    if not is_authenticated():
        return redirect(url_for('login'))
        
    results = RESULTS_CACHE.get(analysis_id)
    if not results:
        flash("La sesión de análisis ha expirado o no existe.", "error")
        return redirect(url_for('dashboard'))
    
    if page < 0: page = 0
    if page >= len(results): page = len(results) - 1
    
    current_data = results[page]
    
    return render_template(
        'result.html', 
        data=current_data, 
        is_multi=True, 
        current_page=page, 
        total_pages=len(results),
        analysis_id=analysis_id
    )

@app.route('/result/<ticker>')
def result(ticker):
    if not is_authenticated():
        return redirect(url_for('login'))
        
    analyzer = StockAnalyzer(ticker)
    if analyzer.fetch_data():
        res = analyzer.analyze()
        if "error" in res:
            flash(res['error'], "error")
            return redirect(url_for('dashboard'))
        return render_template('result.html', data=res)
    
    flash("Error obteniendo datos.", "error")
    return redirect(url_for('dashboard'))

@app.route('/health')
def health():
    return {"status": "ok", "service": "trader-agent"}, 200

if __name__ == '__main__':
    print("Starting Trader Agent Flask App...")
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', debug=True, port=port)
