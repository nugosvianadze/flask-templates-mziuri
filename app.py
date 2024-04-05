from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'Nugo', 'Svianadze'
    title = 'Home Page'
    return render_template('index.html', first_name=first_name,
                           last_name=last_name, title=title)


@app.route('/features')
def features():
    return render_template('features.html')


if __name__ == '__main__':
    app.run(debug=True)