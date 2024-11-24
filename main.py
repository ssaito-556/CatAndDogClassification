import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

classes = ["dog", "cat"]
image_size = 64

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = 'abcdefzyxdls'  # シークレットキーを設定

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


model = load_model('./model.h5')  # 学習済みモデルをロード
#model = None


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            # 画像を読み込み、np形式に変換
            img = image.load_img(filepath,
                                 target_size=(image_size, image_size))
            img = image.img_to_array(img)
            data = np.array([img])

            # 予測
            result = model.predict(data)[0]
            print(result)
            predicted = (result[0] > 0.5).astype("int32")
            print(predicted)
            pred_answer = "これは " + classes[predicted] + " です"

            return render_template("index.html", answer=pred_answer)
        else:
            flash('許可されていない拡張子です')
            return redirect(request.url)

    return render_template("index.html", answer="")


if __name__ == "__main__":
    app.run()
