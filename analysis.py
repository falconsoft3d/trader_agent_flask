import yfinance as yf
import pandas as pd
import ta
import numpy as np
from educational import get_slides

class StockAnalyzer:
    def __init__(self, ticker, interval="1d"):
        self.ticker = ticker.upper()
        self.interval = interval
        self.data = None
        self.info = None

    def fetch_data(self):
        try:
            # Adjust period based on interval
            # Hourly data is limited to 730 days by yfinance
            period = "2y" if self.interval == "1h" else "2y" # Using 2y for daily too to be safe, or 5y? 2y is enough for calculations. 
            # Actually for daily we might want more history if SMA200 needs it, but 2y is ~500 candles (crypto 730). It's fine.
            
            stock = yf.Ticker(self.ticker)
            self.data = stock.history(period=period, interval=self.interval)
            self.info = stock.info
            if self.data.empty:
                return False
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False

    def analyze(self):
        if self.data is None or self.data.empty:
            return None

        df = self.data.copy()
        
        # Ensure we have enough data
        if len(df) < 200:
            return {"error": "No hay suficientes datos históricos (se necesitan al menos 200 días)."}

        # Helper to format data for charts (last 100 days to keep it readable)
        display_df = df.iloc[-100:]
        dates = [d.strftime('%Y-%m-%d') for d in display_df.index]
        prices = display_df['Close'].tolist()

        results = []
        
        # 1. RSI
        rsi_series = ta.momentum.RSIIndicator(df['Close']).rsi()
        last_rsi = rsi_series.iloc[-1]
        vote_rsi = "DOWN" if last_rsi > 70 else ("UP" if last_rsi < 30 else "NEUTRAL")
        
        rsi_history = "Desarrollado por J. Welles Wilder Jr. en 1978 y publicado en su libro 'New Concepts in Technical Trading Systems'. Es uno de los indicadores más populares y utilizados por traders técnicos en todo el mundo para identificar puntos de inflexión en el mercado."
        rsi_desc = "Mide la velocidad y el cambio de los movimientos de precios."
        
        results.append({
            "id": "rsi",
            "method": "Índice de Fuerza Relativa (RSI)",
            "value": f"{last_rsi:.2f}",
            "prediction": vote_rsi,
            "desc": rsi_desc,
            "explanation": "El RSI es un oscilador de momento que mide la velocidad y la magnitud de los cambios recientes de precios para evaluar condiciones de sobrevaloración o infravaloración.",
            "methodology": "Se calcula comparando la magnitud de las ganancias recientes con las pérdidas recientes. Un valor > 70 indica sobrecompra (posible bajada) y < 30 indica sobreventa (posible subida).",
            "history": rsi_history,
            "presentation": get_slides("rsi", "RSI", f"{last_rsi:.2f}", vote_rsi, rsi_desc, rsi_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "RSI", "data": rsi_series.iloc[-100:].fillna(0).tolist(), "borderColor": "#3b82f6"},
                    {"label": "Sobrecompra (70)", "data": [70]*100, "borderColor": "#ef4444", "borderDash": [5,5]},
                    {"label": "Sobreventa (30)", "data": [30]*100, "borderColor": "#10b981", "borderDash": [5,5]}
                ]
            }
        })

        # 2. MACD
        macd = ta.trend.MACD(df['Close'])
        macd_line = macd.macd()
        signal_line = macd.macd_signal()
        vote_macd = "UP" if macd_line.iloc[-1] > signal_line.iloc[-1] else "DOWN"
        macd_history = "Creado por Gerald Appel a finales de la década de 1970..."
        macd_desc = "Sigue la tendencia y muestra la relación entre dos medias móviles."
        results.append({
            "id": "macd",
            "method": "MACD",
            "value": f"MACD: {macd_line.iloc[-1]:.2f}",
            "prediction": vote_macd,
            "desc": macd_desc,
            "explanation": "El MACD es un indicador de impulso de seguimiento de tendencia que muestra la relación entre dos medias móviles del precio de un valor.",
            "methodology": "Se resta la EMA de 26 períodos de la EMA de 12 períodos. La decisión se basa en el cruce: si la línea MACD cruza por encima de la señal, es alcista (UP); si cruza por debajo, es bajista (DOWN).",
            "history": macd_history,
            "presentation": get_slides("macd", "MACD", f"{macd_line.iloc[-1]:.2f}", vote_macd, macd_desc, macd_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "MACD", "data": macd_line.iloc[-100:].fillna(0).tolist(), "borderColor": "#3b82f6"},
                    {"label": "Señal", "data": signal_line.iloc[-100:].fillna(0).tolist(), "borderColor": "#f59e0b"}
                ]
            }
        })

        # 3. SMA Cross
        sma50 = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
        sma200 = ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator()
        vote_sma = "UP" if sma50.iloc[-1] > sma200.iloc[-1] else "DOWN"
        sma_desc = "Compara tendencias a corto (50) y largo plazo (200)."
        sma_history = "El uso de medias móviles se popularizó con el análisis técnico computarizado..."
        results.append({
            "id": "sma",
            "method": "Cruce de Medias (SMA 50/200)",
            "value": f"50: {sma50.iloc[-1]:.2f} / 200: {sma200.iloc[-1]:.2f}",
            "prediction": vote_sma,
            "desc": sma_desc,
            "explanation": "El cruce de medias móviles ayuda a identificar la dirección de la tendencia general.",
            "methodology": "Se comparan la Media Móvil Simple (SMA) de 50 días y la de 200 días. Un 'Cruce Dorado' (50 > 200) sugiere una tendencia alcista a largo plazo. Un 'Cruce de la Muerte' (50 < 200) sugiere lo contrario.",
            "history": sma_history,
            "presentation": get_slides("sma", "SMA 50/200", f"50 vs 200", vote_sma, sma_desc, sma_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "Precio", "data": prices, "borderColor": "#94a3b8", "borderWidth": 1, "pointRadius": 0},
                    {"label": "SMA 50", "data": sma50.iloc[-100:].fillna(0).tolist(), "borderColor": "#3b82f6"},
                    {"label": "SMA 200", "data": sma200.iloc[-100:].fillna(0).tolist(), "borderColor": "#ef4444"}
                ]
            }
        })

        # 4. Bollinger Bands
        bb = ta.volatility.BollingerBands(df['Close'])
        bb_high = bb.bollinger_hband()
        bb_low = bb.bollinger_lband()
        current_price = df['Close'].iloc[-1]
        bb_range = bb_high.iloc[-1] - bb_low.iloc[-1]
        
        if current_price < bb_low.iloc[-1] + (bb_range * 0.2):
            vote_bb = "UP"
        elif current_price > bb_high.iloc[-1] - (bb_range * 0.2):
            vote_bb = "DOWN"
        else:
            vote_bb = "NEUTRAL"
            
        bb_desc = "Evalúa la volatilidad y niveles de precios relativos."
        bb_history = "Desarrolladas por John Bollinger en la década de 1980..."
        results.append({
            "id": "bb",
            "method": "Bandas de Bollinger",
            "value": f"P: {current_price:.2f}, Low: {bb_low.iloc[-1]:.2f}",
            "prediction": vote_bb,
            "desc": bb_desc,
            "explanation": "Las Bandas de Bollinger consisten en una banda central (media móvil) y dos bandas externas (desviación estándar).",
            "methodology": "Si el precio toca la banda inferior, se considera barato (sobreventa -> UP). Si toca la superior, se considera caro (sobrecompra -> DOWN).",
            "history": bb_history,
            "presentation": get_slides("bb", "Bandas Bollinger", f"P: {current_price:.2f}", vote_bb, bb_desc, bb_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "Precio", "data": prices, "borderColor": "#f1f5f9"},
                    {"label": "Banda Sup", "data": bb_high.iloc[-100:].fillna(0).tolist(), "borderColor": "#ef4444", "fill": False},
                    {"label": "Banda Inf", "data": bb_low.iloc[-100:].fillna(0).tolist(), "borderColor": "#10b981", "fill": False}
                ]
            }
        })

        # 5. Stochastic
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
        stoch_k = stoch.stoch()
        vote_stoch = "DOWN" if stoch_k.iloc[-1] > 80 else ("UP" if stoch_k.iloc[-1] < 20 else "NEUTRAL")
        stoch_desc = "Compara el precio de cierre con el rango de precios en un periodo."
        stoch_history = "Desarrollado por George Lane a finales de la década de 1950..."
        results.append({
            "id": "stoch",
            "method": "Oscilador Estocástico",
            "value": f"K%: {stoch_k.iloc[-1]:.2f}",
            "prediction": vote_stoch,
            "desc": stoch_desc,
            "explanation": "El oscilador estocástico es un indicador de impulso que compara un precio de cierre particular con un rango de sus precios durante un cierto período de tiempo.",
            "methodology": "Valores por encima de 80 indican que el activo está sobrecomprado (vender). Valores por debajo de 20 indican que está sobrevendido (comprar).",
            "history": stoch_history,
            "presentation": get_slides("stoch", "Estocástico", f"{stoch_k.iloc[-1]:.2f}", vote_stoch, stoch_desc, stoch_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "Stoch K%", "data": stoch_k.iloc[-100:].fillna(0).tolist(), "borderColor": "#8b5cf6"},
                    {"label": "80", "data": [80]*100, "borderColor": "#ef4444", "borderDash": [2,2]},
                    {"label": "20", "data": [20]*100, "borderColor": "#10b981", "borderDash": [2,2]}
                ]
            }
        })

        # 6. EMA Trend
        ema20 = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
        vote_ema = "UP" if current_price > ema20.iloc[-1] else "DOWN"
        ema_desc = "Tendencia a corto plazo usando media móvil exponencial."
        ema_history = "Las medias móviles exponenciales ganaron popularidad..."
        results.append({
            "id": "ema",
            "method": "Tendencia EMA (20)",
            "value": f"P: {current_price:.2f} vs EMA: {ema20.iloc[-1]:.2f}",
            "prediction": vote_ema,
            "desc": ema_desc,
            "explanation": "La Media Móvil Exponencial (EMA) da más peso a los datos de precios recientes que la media móvil simple.",
            "methodology": "Analizamos la EMA de 20 días. Si el precio actual está por encima de la EMA, indica una tendencia alcista a corto plazo. Si está por debajo, bajista.",
            "history": ema_history,
            "presentation": get_slides("ema", "EMA 20", f"{current_price:.2f}", vote_ema, ema_desc, ema_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "Precio", "data": prices, "borderColor": "#94a3b8"},
                    {"label": "EMA 20", "data": ema20.iloc[-100:].fillna(0).tolist(), "borderColor": "#f59e0b"}
                ]
            }
        })

        # 7. CCI
        cci = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close']).cci()
        vote_cci = "DOWN" if cci.iloc[-1] > 100 else ("UP" if cci.iloc[-1] < -100 else "NEUTRAL")
        cci_desc = "Identifica tendencias cíclicas en sus extremos."
        cci_history = "Desarrollado por Donald Lambert en 1980..."
        results.append({
            "id": "cci",
            "method": "CCI (Commodity Channel Index)",
            "value": f"CCI: {cci.iloc[-1]:.2f}",
            "prediction": vote_cci,
            "desc": cci_desc,
            "explanation": "El CCI mide la diferencia entre el precio actual y su media histórica.",
            "methodology": "Se utiliza para identificar sobrecompra/sobreventa. Un valor > 100 implica sobrecompra (posible caída). Un valor < -100 implica sobreventa (posible subida).",
            "history": cci_history,
            "presentation": get_slides("cci", "CCI", f"{cci.iloc[-1]:.2f}", vote_cci, cci_desc, cci_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "CCI", "data": cci.iloc[-100:].fillna(0).tolist(), "borderColor": "#ec4899"},
                    {"label": "100", "data": [100]*100, "borderColor": "#ef4444", "borderDash": [5,5]},
                    {"label": "-100", "data": [-100]*100, "borderColor": "#10b981", "borderDash": [5,5]}
                ]
            }
        })

        # 8. Williams %R
        wr = ta.momentum.WilliamsRIndicator(df['High'], df['Low'], df['Close']).williams_r()
        vote_wr = "UP" if wr.iloc[-1] < -80 else ("DOWN" if wr.iloc[-1] > -20 else "NEUTRAL")
        wr_desc = "Indicador de momento inverso a niveles de 0 a -100."
        wr_history = "Desarrollado por el famoso trader y autor Larry Williams..."
        results.append({
            "id": "wr",
            "method": "Williams %R",
            "value": f"%R: {wr.iloc[-1]:.2f}",
            "prediction": vote_wr,
            "desc": wr_desc,
            "explanation": "Williams %R es un indicador de momento que se mueve entre 0 y -100 y mide niveles de sobrecompra y sobreventa.",
            "methodology": "Si está por encima de -20 (cerca de 0), el activo está sobrecomprado. Si está por debajo de -80, está sobrevendido (oportunidad de compra).",
            "history": wr_history,
            "presentation": get_slides("wr", "Williams %R", f"{wr.iloc[-1]:.2f}", vote_wr, wr_desc, wr_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "Williams %R", "data": wr.iloc[-100:].fillna(0).tolist(), "borderColor": "#14b8a6"},
                    {"label": "-20", "data": [-20]*100, "borderColor": "#ef4444", "borderDash": [2,2]},
                    {"label": "-80", "data": [-80]*100, "borderColor": "#10b981", "borderDash": [2,2]}
                ]
            }
        })

        # 9. ROC
        roc = ta.momentum.ROCIndicator(df['Close'], window=12).roc()
        vote_roc = "UP" if roc.iloc[-1] > 0 else "DOWN"
        roc_desc = "Mide el cambio porcentual en el precio."
        roc_history = "El concepto de Rate of Change (Tasa de Cambio)..."
        results.append({
            "id": "roc",
            "method": "Momentum (Rate of Change)",
            "value": f"ROC: {roc.iloc[-1]:.2f}%",
            "prediction": vote_roc,
            "desc": roc_desc,
            "explanation": "El ROC es un oscilador de momento que mide el cambio porcentual entre el precio actual y el precio de hace n periodos (12 en este caso).",
            "methodology": "Si el ROC es positivo, el momento es alcista (el precio está subiendo aceleradamente). Si es negativo, el momento es bajista.",
            "history": roc_history,
            "presentation": get_slides("roc", "ROC", f"{roc.iloc[-1]:.2f}%", vote_roc, roc_desc, roc_history),
            "chart_type": "bar",
            "chart_data": {
                "labels": dates,
                "datasets": [
                    {"label": "ROC", "data": roc.iloc[-100:].fillna(0).tolist(), "backgroundColor": "#3b82f6"}
                ]
            }
        })

        # 10. Slope
        y = df['Close'].iloc[-10:].values
        x = np.arange(len(y))
        slope, _ = np.polyfit(x, y, 1)
        vote_slope = "UP" if slope > 0 else "DOWN"
        # Create regression line points for chart
        reg_line = [slope * i + (y[0] - slope * 0) for i in range(len(x))]
        slope_desc = "Dirección simple de los últimos 10 días."
        slope_history = "La regresión lineal es una técnica estadística fundamental..."
        
        results.append({
            "id": "slope",
            "method": "Pendiente (Regresión Lineal)",
            "value": f"Pendiente: {slope:.2f}",
            "prediction": vote_slope,
            "desc": slope_desc,
            "explanation": "Calcula la pendiente matemática de la línea de mejor ajuste para los precios de cierre de los últimos 10 días.",
            "methodology": "Usamos regresión lineal (mínimos cuadrados). Una pendiente positiva indica que la tendencia a muy corto plazo es hacia arriba.",
            "history": slope_history,
            "presentation": get_slides("slope", "Pendiente", f"{slope:.2f}", vote_slope, slope_desc, slope_history),
            "chart_type": "line",
            "chart_data": {
                "labels": dates[-10:],
                "datasets": [
                    {"label": "Precio Real", "data": y.tolist(), "borderColor": "#94a3b8"},
                    {"label": "Tendencia Lineal", "data": reg_line, "borderColor": "#3b82f6", "borderDash": [5,5]}
                ]
            }
        })

        # Summary
        up_votes = sum(1 for r in results if r['prediction'] == "UP")
        down_votes = sum(1 for r in results if r['prediction'] == "DOWN")
        
        # Calculate confidence
        total_votes = len(results)
        
        decision = "NEUTRAL"
        if up_votes > down_votes:
            decision = "COMPRAR (BUY)"
        elif down_votes > up_votes:
            decision = "VENDER (SELL)"
        
        return {
            "ticker": self.ticker,
            "interval": self.interval,
            "company_name": self.info.get('longName', self.ticker) if self.info else self.ticker,
            "company_summary": self.info.get('longBusinessSummary', 'No disponible.') if self.info else 'No disponible.',
            "current_price": current_price,
            "results": results,
            "summary": {
                "up_votes": up_votes,
                "down_votes": down_votes,
                "neutral_votes": total_votes - up_votes - down_votes,
                "decision": decision
            }
        }
