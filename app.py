from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/test')
def test():
    return 'Test page works!'

if __name__ == '__main__':
    app.run()
