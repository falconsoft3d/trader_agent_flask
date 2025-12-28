
def get_slides(indicator_id, method_name, value, prediction, desc, history):
    """
    Generates 10 educational slides for a given indicator.
    """
    
    # Common slide structure helper
    def slide(title, content, type="text"):
        return {"title": title, "content": content, "type": type}

    # Define content based on ID
    slides = []

    # 1. Title Slide (Common)
    slides.append(slide(
        f"Introducción a: {method_name}", 
        f"Bienvenido a esta guía paso a paso sobre el indicador {method_name}.<br>Aprenderemos qué es, cómo funciona y qué nos dice sobre el precio actual."
    ))

    if indicator_id == "rsi":
        slides.append(slide("¿Qué es el RSI?", "El Índice de Fuerza Relativa (RSI) es como el velocímetro de un coche. Nos dice qué tan rápido se está moviendo el precio y si el 'motor' (el mercado) se está calentando demasiado."))
        slides.append(slide("La Metáfora", "Imagina una banda elástica. Si la estiras demasiado (precio sube mucho), eventualmente tiene que rebotar hacia atrás. El RSI mide cuánto se ha estirado esa banda."))
        slides.append(slide("La Escala", "El RSI se mueve en una escala del 0 al 100. <br>• 0: Nadie quiere comprar.<br>• 100: Todos quieren comprar."))
        slides.append(slide("Zona de Sobrecompra", "Cuando el RSI supera el 70, decimos que está 'Sobrecomprado'. Es como si la banda elástica estuviera al límite. Es probable que el precio baje pronto."))
        slides.append(slide("Zona de Sobreventa", "Cuando el RSI cae por debajo de 30, está 'Sobrevendido'. La banda está floja. Es probable que el precio suba pronto porque está demasiado barato."))
        slides.append(slide("El Cálculo", "Compara los días que el precio subió con los días que bajó. Si hubo muchos días de subida fuerte, el RSI será alto."))
        slides.append(slide("Análisis Actual", f"Valor actual: <strong>{value}</strong>.<br>Dado este valor, el indicador sugiere: <strong>{prediction}</strong>."))
        slides.append(slide("Señales Falsas", "¡Cuidado! En tendencias muy fuertes, el RSI puede quedarse en 'Sobrecompra' durante mucho tiempo mientras el precio sigue subiendo."))
        slides.append(slide("Origen Histórico", history))

    elif indicator_id == "macd":
        slides.append(slide("¿Qué es el MACD?", "MACD significa Convergencia/Divergencia de Medias Móviles. Es un rastreador de tendencias y de impulso."))
        slides.append(slide("La Metáfora", "Piensa en un corredor (el precio) y su sombra. A veces corren juntos, a veces se separan. El MACD mide esa separación para predecir giros."))
        slides.append(slide("Los Componentes", "Tiene dos líneas principales: <br>1. La línea MACD (rápida).<br>2. La línea de Señal (lenta)."))
        slides.append(slide("El Cruce Alcista", "Cuando la línea rápida cruza por ENCIMA de la lenta, es como si el corredor acelerara. Es una señal de COMPRA."))
        slides.append(slide("El Cruce Bajista", "Cuando la línea rápida cruza por DEBAJO de la lenta, el corredor se cansa. Es una señal de VENTA."))
        slides.append(slide("El Histograma", "A menudo verás barras verticales. Representan la distancia entre las dos líneas. Si las barras crecen, la tendencia se fortalece."))
        slides.append(slide("Análisis Actual", f"Lectura actual: <strong>{value}</strong>.<br>Según el cruce de líneas, la señal es: <strong>{prediction}</strong>."))
        slides.append(slide("Divergencias", "Si el precio sube pero el MACD baja, es una advertencia grave de que la subida es falsa."))
        slides.append(slide("Origen Histórico", history))

    elif indicator_id == "bb":
        slides.append(slide("¿Qué son las Bandas de Bollinger?", "Son 'sobres' alrededor del precio que se expanden y contraen. Nos dicen si el mercado está tranquilo o loco (volátil)."))
        slides.append(slide("La Metáfora", "Imagina una carretera. El precio suele mantenerse en el carril (dentro de las bandas). Si se sale del carril, es un evento excepcional."))
        slides.append(slide("Componentes", "1. Banda Central: El precio promedio.<br>2. Bandas Externas: Límites estadísticos normales."))
        slides.append(slide("Compresión (Squeeze)", "Cuando las bandas se estrechan, el mercado está 'tomando aire'. Generalmente, esto precede a un movimiento explosivo."))
        slides.append(slide("Rebote", "El precio tiende a rebotar en las bandas exteriores y volver al centro, como una pelota en un pasillo."))
        slides.append(slide("Rupturas", "Si el precio rompe una banda con fuerza, puede indicar el inicio de una nueva tendencia, no solo un rebote."))
        slides.append(slide("Análisis Actual", f"Datos actuales: <strong>{value}</strong>.<br>Basado en la posición respecto a las bandas: <strong>{prediction}</strong>."))
        slides.append(slide("Limitaciones", "No predicen la dirección por sí solas, solo la volatilidad y los extremos relativos."))
        slides.append(slide("Origen Histórico", history))

    elif indicator_id == "sma":
        slides.append(slide("¿Qué son las Medias Móviles?", "Son el promedio del precio en el pasado. Suavizan el ruido para ver la tendencia real."))
        slides.append(slide("La Metáfora", "El precio diario es como las olas del mar (caótico). La SMA es como la marea (la dirección real del agua)."))
        slides.append(slide("SMA 50 vs 200", "• SMA 50: Tendencia a medio plazo (trimestral).<br>• SMA 200: Tendencia a largo plazo (anual)."))
        slides.append(slide("Cruce Dorado", "Cuando la línea corta (50) cruza hacia ARRIBA a la larga (200). Es una de las señales alcistas más famosas."))
        slides.append(slide("Cruce de la Muerte", "Cuando la línea corta (50) cruza hacia ABAJO a la larga (200). Señal de peligro a largo plazo."))
        slides.append(slide("Soporte y Resistencia", "Muchas veces, el precio rebota exactamente en la línea de 200 días. Los inversores institucionales vigilan esto."))
        slides.append(slide("Análisis Actual", f"Valores: <strong>{value}</strong>.<br>Relación entre medias: <strong>{prediction}</strong>."))
        slides.append(slide("Retraso (Lag)", "Al basarse en el pasado, las SMA reaccionan lento. No sirven para predecir picos rápidos."))
        slides.append(slide("Origen Histórico", history))

    else:
        # Generic Template based specific textual details passed or generic logic
        slides.append(slide("Concepto Básico", f"El indicador {method_name} es una herramienta matemática utilizada para predecir movimientos futuros basándose en patrones pasados."))
        slides.append(slide("¿Qué mide?", desc))
        slides.append(slide("La Lógica", "Los mercados no son totalmente aleatorios. Tienen memoria ypsicología. Este indicador intenta cuantificar esa psicología en un número."))
        slides.append(slide("Interpretación", "Generalmente buscamos extremos. Si el valor es muy alto o muy bajo, sugiere que el mercado ha ido demasiado lejos y debe corregir."))
        slides.append(slide("Tendencia vs Oscilación", "Algunos indicadores siguen la tendencia (trend-following) y otros oscilan en rangos. Este indicador particular nos da pistas sobre: " + desc))
        slides.append(slide("Lectura del Valor", f"El valor calculado hoy es: <strong>{value}</strong>."))
        slides.append(slide("La Señal Generada", f"Basado en las reglas estándar, la señal es: <strong>{prediction}</strong>."))
        slides.append(slide("¿Es infalible?", "Ningún indicador acierta el 100% de las veces. Siempre debe usarse en combinación con otros para confirmar."))
        slides.append(slide("Origen Histórico", history))

    # 10. Conclusion (Common)
    slides.append(slide(
        "Resumen Final", 
        f"Hemos visto que el {method_name} está indicando actualmente <strong>{prediction}</strong>. Recuerda combinar esto con el análisis fundamental y tu propia gestión de riesgo."
    ))

    # Fill to ensure 10 slides if short
    while len(slides) < 10:
        slides.insert(len(slides)-1, slide("Dato Curioso", "El análisis técnico es una profecía autocumplida: funciona porque mucha gente cree que funciona y actúa en consecuencia."))

    return slides[:10] # Ensure exactly 10 or max 10
