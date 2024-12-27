from http.server import BaseHTTPRequestHandler

# Örnek videolar
VIDEOS = [
    {
        'id': 1,
        'baslik': 'Örnek Video 1',
        'aciklama': 'Bu bir örnek videodur',
        'video_url': '/static/videos/video1.mp4',
        'goruntuleme': 100
    },
    {
        'id': 2,
        'baslik': 'Örnek Video 2',
        'aciklama': 'Bu başka bir örnek videodur',
        'video_url': '/static/videos/video2.mp4',
        'goruntuleme': 200
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SitWatch</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f9f9f9;
        }
        nav {
            margin-bottom: 20px;
        }
        nav a {
            color: #333;
            text-decoration: none;
            margin-right: 15px;
        }
        .video-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .video-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .video-card h2 {
            margin: 0 0 10px 0;
            font-size: 18px;
        }
        .video-card p {
            margin: 5px 0;
            color: #666;
        }
        .views {
            font-size: 14px;
            color: #888;
        }
    </style>
</head>
<body>
    <h1>SitWatch</h1>
    <nav>
        <a href="/">Ana Sayfa</a>
        <a href="/test">Test</a>
    </nav>
    
    <div class="video-grid">
        {video_cards}
    </div>
</body>
</html>
"""

def generate_video_cards():
    cards = []
    for video in VIDEOS:
        card = f"""
        <div class="video-card">
            <h2>{video['baslik']}</h2>
            <p>{video['aciklama']}</p>
            <p class="views">{video['goruntuleme']} görüntülenme</p>
        </div>
        """
        cards.append(card)
    return '\n'.join(cards)

def handler(request):
    try:
        if request['url'] == '/':
            video_cards = generate_video_cards()
            response = HTML_TEMPLATE.format(video_cards=video_cards)
        elif request['url'] == '/test':
            response = 'Test page works!'
        else:
            response = '404 Not Found'
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8"
            },
            "body": response
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": str(e)
        }
