from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar_123'
app.config['SERVER_NAME'] = 'sdiscord.site'  # Domain adınızı buraya yazın
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'jpg', 'jpeg', 'png'}

db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    videolar = db.relationship('Video', backref='yayinci', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(200), nullable=False)
    thumbnail_url = db.Column(db.String(200), nullable=False, default='static/img/thumbnail.jpg')
    sure = db.Column(db.String(10), nullable=False, default='00:00')
    yuklenme_tarihi = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    goruntuleme = db.Column(db.Integer, default=0)
    kullanici = db.Column(db.String(20), nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def ana_sayfa():
    videolar = Video.query.order_by(Video.yuklenme_tarihi.desc()).all()
    return render_template('index.html', videolar=videolar)

@app.route('/trendler')
def trendler():
    trendler = Video.query.order_by(Video.goruntuleme.desc()).limit(10).all()
    return render_template('trendler.html', videolar=trendler)

@app.route('/izle/<int:video_id>')
def izle(video_id):
    video = Video.query.get_or_404(video_id)
    video.goruntuleme += 1
    db.session.commit()
    return render_template('izle.html', video=video)

@app.route('/yukle', methods=['GET', 'POST'])
def yukle():
    if 'user_id' not in session:
        flash('Video yüklemek için giriş yapmalısınız.')
        return redirect(url_for('giris'))
        
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        flash('Oturum süresi dolmuş. Lütfen tekrar giriş yapın.')
        return redirect(url_for('giris'))
        
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('Video dosyası seçilmedi.')
            return redirect(request.url)
            
        video = request.files['video']
        if video.filename == '':
            flash('Video dosyası seçilmedi.')
            return redirect(request.url)
            
        if not allowed_file(video.filename):
            flash('Bu dosya türü desteklenmiyor.')
            return redirect(request.url)
            
        if video:
            filename = secure_filename(video.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            video.save(video_path)
            
            thumbnail = request.files.get('thumbnail')
            thumbnail_url = 'static/img/thumbnail.jpg'
            if thumbnail and allowed_file(thumbnail.filename):
                thumbnail_filename = secure_filename(thumbnail.filename)
                thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename)
                thumbnail.save(thumbnail_path)
                thumbnail_url = os.path.join('static/uploads', thumbnail_filename)
            
            new_video = Video(
                baslik=request.form['baslik'],
                aciklama=request.form['aciklama'],
                video_url=os.path.join('uploads', filename),
                thumbnail_url=thumbnail_url,
                sure=request.form.get('sure', '00:00'),
                kullanici=user.username,
                kullanici_id=user.id
            )
            
            db.session.add(new_video)
            db.session.commit()
            
            flash('Video başarıyla yüklendi!')
            return redirect(url_for('izle', video_id=new_video.id))
            
    return render_template('yukle.html')

@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Başarıyla giriş yaptınız!')
            return redirect(url_for('ana_sayfa'))
            
        flash('Kullanıcı adı veya şifre hatalı.')
        return redirect(url_for('giris'))
        
    return render_template('giris.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten alınmış.')
            return redirect(url_for('kayit'))
            
        if User.query.filter_by(email=email).first():
            flash('Bu email adresi zaten kayıtlı.')
            return redirect(url_for('kayit'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Başarıyla kayıt oldunuz!')
        return redirect(url_for('giris'))
        
    return render_template('kayit.html')

@app.route('/cikis')
def cikis():
    session.pop('user_id', None)
    flash('Başarıyla çıkış yaptınız.')
    return redirect(url_for('ana_sayfa'))

# Veritabanını başlat ve örnek veri ekle
def init_db():
    with app.app_context():
        # Upload klasörünü oluştur
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Tabloları oluştur
        db.create_all()
        
        # Örnek kullanıcı ekle
        if not User.query.first():
            admin = User(username='admin', email='admin@sdiscord.site')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
            # Örnek video ekle
            if not Video.query.first():
                ornek_video = Video(
                    baslik='Hoş Geldiniz',
                    aciklama='SitWatch\'a hoş geldiniz!',
                    video_url='static/video/ornek.mp4',
                    kullanici='admin',
                    kullanici_id=admin.id
                )
                db.session.add(ornek_video)
                db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
