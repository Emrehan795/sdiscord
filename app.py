from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['DEBUG'] = True

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

@app.route('/')
def index():
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        if not os.path.exists(template_path):
            return f"Template not found at {template_path}"
        return render_template('index.html', videolar=VIDEOS)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/test')
def test():
    return 'Test page works!'

if __name__ == '__main__':
    app.run()
