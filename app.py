from flask import Flask, render_template, jsonify, request
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_songs_list')
def get_songs_list():
    data = request.args.get('id', 1)
    content = main.find_by_song(data)
    print("content:",content)
    return jsonify({'content': content})

@app.route('/get_cover')
def get_cover():
    data = request.args.get('id', 1)
    content = main.get_cover(data)
    # content = "https://coverartarchive.org/release/37347c11-dd53-4d52-aade-078ddb7c32f3/42166269002-250.jpg"
    print("content:",content)
    return jsonify({'content': content})

@app.route('/get_local_songs')
def get_local_songs():
    content = main.get_local_songs()
    print("content:",content)
    return jsonify({'content': content})

@app.route('/apply_metadata')
def apply_metadata():
    data = request.args.get('id')
    songname = request.args.get('name')
    content = main.final(data, songname)
    print("content:",content)
    return jsonify({'content': content})  

if __name__ == '__main__':
    app.run(debug=True)