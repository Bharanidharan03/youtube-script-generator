from flask import Flask, render_template, request
import pakka

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    categories = pakka.get_youtube_categories()
    return render_template('index.html', categories=categories)

@app.route('/trending', methods=['POST'])
def trending():
    category_id = request.form['category_id']
    trending_videos = pakka.get_trending_videos(category_id)
    if trending_videos:
        return render_template('trending.html', trending_videos=trending_videos)
    else:
        all_trends = pakka.get_all_trending()
        return render_template('all_trends.html', all_trends=all_trends)

@app.route('/generate_script', methods=['POST'])
def generate_script():
    topic = request.form['topic']
    script = pakka.generate_script(topic)
    return render_template('result.html', script=script)

if __name__ == '__main__':
    app.run(debug=True)