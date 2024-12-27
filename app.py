from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

VIDEOS = [
    {
        'id': 1,
        'baslik': 'Örnek Video 1',
        'aciklama': 'Bu bir örnek videodur',
        'video_url': 'https://example.com/video1.mp4',
        'goruntuleme': 100
    },
    {
        'id': 2,
        'baslik': 'Örnek Video 2',
        'aciklama': 'Bu başka bir örnek videodur',
        'video_url': 'https://example.com/video2.mp4',
        'goruntuleme': 200
    }
]

@app.route('/')
def index():
    return render_template('index.html', videolar=VIDEOS)

@app.route('/trendler')
def trendler():
    return render_template('trendler.html', videolar=VIDEOS)

@app.route('/izle/<int:video_id>')
def izle(video_id):
    video = next((v for v in VIDEOS if v['id'] == video_id), None)
    if video:
        return render_template('izle.html', video=video)
    return redirect(url_for('index'))

@app.route('/yukle', methods=['GET', 'POST'])
def yukle():
    if request.method == 'POST':
        flash('Video yükleme şu anda devre dışı')
        return redirect(url_for('index'))
    return render_template('yukle.html')

if __name__ == '__main__':
    app.run()
