from flask import Flask, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLiteデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///balance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデル定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False, default=10000)
    password = db.Column(db.String(255), nullable=False, default="password123")  # デフォルトパスワード

# 初期化処理
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(balance=10000, password="password123"))
        db.session.commit()

@app.route('/')
def index():
    """残額と金額入力フォームのページ"""
    user = User.query.first()
    return render_template('index.html', balance=user.balance)

@app.route('/payment', methods=['POST'])
def payment():
    """支払処理"""
    user = User.query.first()
    amount = int(request.form['amount'])

    if amount <= 0:
        return render_template('index.html', balance=user.balance, error="正しい金額を入力してください")
    if amount > user.balance:
        return render_template('index.html', balance=user.balance, error="残額が不足しています")

    user.balance -= amount
    db.session.commit()
    return render_template('result.html', input_amount=amount, new_balance=user.balance)

@app.route('/charge', methods=['GET'])
def charge_page():
    """チャージページの表示"""
    user = User.query.first()
    return render_template('charge.html', balance=user.balance)

@app.route('/process_charge', methods=['POST'])
def process_charge():
    """チャージ処理"""
    user = User.query.first()
    amount = int(request.form['charge_amount'])
    input_password = request.form['password']

    if input_password != user.password:
        return render_template('charge.html', balance=user.balance, charge_error="パスワードが一致しません")

    if amount <= 0:
        return render_template('charge.html', balance=user.balance, charge_error="正しい金額を入力してください")

    user.balance += amount
    db.session.commit()
    return render_template('charge.html', balance=user.balance, charge_success=f"{amount}円をチャージしました！")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run()@app.route('/sw.js')
