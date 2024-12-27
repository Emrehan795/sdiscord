from app import app

app.config['SERVER_NAME'] = None  # Remove server name constraint for Vercel

if __name__ == '__main__':
    app.run()
