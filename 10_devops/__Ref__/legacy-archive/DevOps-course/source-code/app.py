"""
The Counter App - Ứng dụng đếm số đơn giản
Dùng Flask (Web Framework) + Redis (Database)
"""

from flask import Flask, render_template_string
import redis
import os

app = Flask(__name__)

# Kết nối Redis (mặc định localhost:6379)
# Nếu chạy trong Docker, sẽ dùng biến môi trường REDIS_HOST
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

try:
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    r.ping()  # Test kết nối
    print(f"✅ Đã kết nối Redis tại {redis_host}:{redis_port}")
except Exception as e:
    print(f"❌ Không thể kết nối Redis: {e}")
    r = None

# HTML Template đơn giản
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>The Counter App</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 {
            color: #667eea;
            margin-bottom: 30px;
        }
        .counter {
            font-size: 80px;
            font-weight: bold;
            color: #764ba2;
            margin: 30px 0;
        }
        .info {
            color: #666;
            font-size: 14px;
            margin-top: 20px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            margin: 10px;
            transition: all 0.3s ease;
        }
        button:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 The Counter App</h1>
        <div class="counter">{{ count }}</div>
        <div>
            <button onclick="window.location.href='/increment'">➕ Tăng</button>
            <button onclick="window.location.href='/reset'">🔄 Reset</button>
        </div>
        <div class="info">
            Server: {{ hostname }}<br>
            Redis: {{ redis_status }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Trang chủ - Hiển thị số đếm hiện tại"""
    if r is None:
        count = "❌ Redis offline"
        redis_status = "Disconnected"
    else:
        try:
            # Lấy số đếm từ Redis (nếu chưa có thì mặc định là 0)
            count = r.get('counter')
            if count is None:
                r.set('counter', 0)
                count = 0
            redis_status = "Connected ✅"
        except Exception as e:
            count = f"Error: {e}"
            redis_status = "Error"
    
    hostname = os.getenv('HOSTNAME', 'localhost')
    
    return render_template_string(HTML_TEMPLATE, 
                                   count=count, 
                                   hostname=hostname,
                                   redis_status=redis_status)

@app.route('/increment')
def increment():
    """Tăng số đếm lên 1"""
    if r:
        try:
            r.incr('counter')
        except Exception as e:
            print(f"Error incrementing: {e}")
    return index()

@app.route('/reset')
def reset():
    """Reset số đếm về 0"""
    if r:
        try:
            r.set('counter', 0)
        except Exception as e:
            print(f"Error resetting: {e}")
    return index()

@app.route('/health')
def health():
    """Health check endpoint cho monitoring"""
    if r:
        try:
            r.ping()
            return {"status": "healthy", "redis": "connected"}, 200
        except:
            return {"status": "unhealthy", "redis": "disconnected"}, 503
    return {"status": "unhealthy", "redis": "not_configured"}, 503

if __name__ == '__main__':
    # Chạy Flask server
    # host='0.0.0.0' để có thể truy cập từ bên ngoài container
    app.run(host='0.0.0.0', port=5000, debug=True)
