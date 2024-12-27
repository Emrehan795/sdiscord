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
        return render_template('index.html', videolar=VIDEOS)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/test')
def test():
    return "Test page works!"

app.jinja_env.globals.update(url_for=lambda *args, **kwargs: '/')
