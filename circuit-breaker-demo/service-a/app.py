#Librerias
from flask import Flask, jsonify, render_template_string
import requests
from circuitbreaker import circuit
import time

app = Flask(__name__)

# Configuración del Circuit Breaker
CB_CONFIG = {
    'failure_threshold': 3,
    'recovery_timeout': 10,
    'name': 'ServiceB_Circuit'
}

#Interfaz Web Principal
@app.route('/')
def dashboard():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Circuit Breaker Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .container { display: flex; gap: 20px; }
                .panel { border: 1px solid #ccc; padding: 20px; border-radius: 5px; width: 300px; }
                button { padding: 10px; margin: 5px; cursor: pointer; }
                .healthy { color: green; }
                .degraded { color: orange; }
                .unhealthy { color: red; }
                #status { font-weight: bold; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>Circuit Breaker Demo</h1>
            <div class="container">
                <div class="panel">
                    <h2>Service A (Client)</h2>
                    <button onclick="callServiceB()">Call Service B</button>
                    <button onclick="toggleCircuit()">Toggle Circuit</button>
                    <div id="status">Status: Ready</div>
                    <div id="result"></div>
                </div>
                
                <div class="panel">
                    <h2>Service B Controls</h2>
                    <button onclick="setServiceB('normal')">Normal Mode</button>
                    <button onclick="setServiceB('slow')">Slow Mode (+2s)</button>
                    <button onclick="setServiceB('error')">Error Mode (50%)</button>
                    <button onclick="setServiceB('down')">Down Service</button>
                </div>
            </div>

            <script>
                async function callServiceB() {
                    document.getElementById('status').textContent = "Status: Calling Service B...";
                    try {
                        const response = await fetch('/call-b');
                        const data = await response.json();
                        document.getElementById('result').innerHTML = 
                            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                        document.getElementById('status').className = 
                            response.ok ? 'healthy' : 'degraded';
                        document.getElementById('status').textContent = 
                            `Status: ${response.ok ? 'Success' : 'Fallback'}`;
                    } catch (error) {
                        document.getElementById('status').className = 'unhealthy';
                        document.getElementById('status').textContent = 'Status: Error';
                        document.getElementById('result').textContent = error;
                    }
                }

                async function toggleCircuit() {
                    await fetch('/toggle-circuit');
                    alert("Circuit state toggled!");
                }

                async function setServiceB(mode) {
                    await fetch(`http://localhost:5001/set-mode?mode=${mode}`);
                    alert(`Service B set to ${mode} mode`);
                }
            </script>
        </body>
        </html>
    ''')

#Se llama al servicio B con circuit
@circuit(**CB_CONFIG)
def call_service_b():
    response = requests.get('http://service-b:5001/api', timeout=2)
    response.raise_for_status()
    return response.json()

#Invoca el servicio B
@app.route('/call-b')
def invoke_service_b():
    try:
        start_time = time.time()
        data = call_service_b()
        latency = time.time() - start_time
        return jsonify({
            "status": "success",
            "data": data,
            "latency": f"{latency:.2f}s",
            "circuit_state": "closed"
        })
    except Exception as e:
        return jsonify({
            "status": "fallback",
            "message": "Service B unavailable",
            "error": str(e),
            "circuit_state": "open"
        }), 503

#Control del Circuit
@app.route('/toggle-circuit')
def toggle_circuit():
    # Implementación básica para demostración
    CB_CONFIG['failure_threshold'] = 1 if CB_CONFIG['failure_threshold'] == 3 else 3
    return jsonify({"new_threshold": CB_CONFIG['failure_threshold']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)