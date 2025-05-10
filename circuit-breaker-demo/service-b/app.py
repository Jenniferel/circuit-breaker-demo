#Librerias
from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)

# Configuración dinámica
SERVICE_CONFIG = {
    'mode': 'normal',  # normal, slow, error, down
    'latency': 0,
    'error_rate': 0
}
#Servicio Principal - Simulacion con diferentes modos de fallos
@app.route('/api')
def api():
    if SERVICE_CONFIG['mode'] == 'down': # Siempre falla con timeout (5 segundos)
        time.sleep(5)  # Timeout excedido
        return jsonify({"error": "Service down"}), 500
        
    if SERVICE_CONFIG['mode'] == 'slow': # Respuesta lenta (+2 segundos)
        time.sleep(2 + SERVICE_CONFIG['latency'])
        
    if SERVICE_CONFIG['mode'] == 'error' or random.random() < SERVICE_CONFIG['error_rate']: #50% de probabilidad de fallo
        return jsonify({"error": "Service error"}), 500
        
    return jsonify({
        "status": "success",
        "service": "B",
        "mode": SERVICE_CONFIG['mode'],
        "data": {"value": random.randint(1, 100)}
    })
#Control del Comportamiento
@app.route('/set-mode')
def set_mode():
    mode = request.args.get('mode', 'normal')
    SERVICE_CONFIG['mode'] = mode
    
    if mode == 'normal':
        SERVICE_CONFIG.update({'latency': 0, 'error_rate': 0})
    elif mode == 'slow': ## Modo "slow" - Latencia artificial
        SERVICE_CONFIG.update({'latency': 2, 'error_rate': 0})
    elif mode == 'error':  # Modo "error" - Fallo aleatorio
        SERVICE_CONFIG.update({'latency': 0, 'error_rate': 0.5})
    elif mode == 'down': # # Modo "down" - Servicio no disponible
        SERVICE_CONFIG.update({'latency': 0, 'error_rate': 1})
    
    return jsonify(SERVICE_CONFIG)

#Health check para verificar disponibilidad del servicio.
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "service": "B"
    }), 200

#Inicializacion del servicio
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)