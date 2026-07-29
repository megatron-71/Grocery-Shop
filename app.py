from flask import Flask, request, jsonify, session, render_template
import sqlite3, hashlib, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "grocery_secret_2025"

# Use absolute path so the DB is always found regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, 'grocery.db')

# ================= DB =================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript('''
    CREATE TABLE IF NOT EXISTS staff(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    );

    CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER,
        min_stock INTEGER DEFAULT 5
    );

    CREATE TABLE IF NOT EXISTS bill(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS bill_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        product_id INTEGER,
        qty INTEGER,
        price REAL
    );
    ''')

    pw = hashlib.sha256("admin123".encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO staff(username,password,role) VALUES(?,?,?)",
              ("admin", pw, "admin"))

    conn.commit()
    conn.close()

# ================= FRONTEND =================

@app.route('/')
def home():
    return render_template('sp.html')

# ================= AUTH =================

@app.route('/api/login', methods=['POST'])
def login():
    d = request.json
    pw = hashlib.sha256(d['password'].encode()).hexdigest()

    conn = get_db()
    user = conn.execute("SELECT * FROM staff WHERE username=? AND password=?",
                        (d['username'], pw)).fetchone()
    conn.close()

    if user:
        session['user'] = dict(user)
        return jsonify({'success': True, 'user': user['username']})
    return jsonify({'success': False}), 401

# ================= PRODUCTS =================

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    data = conn.execute("SELECT * FROM product").fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

@app.route('/api/products', methods=['POST'])
def add_product():
    d = request.json
    conn = get_db()
    conn.execute("INSERT INTO product(name,category,price,stock,min_stock) VALUES(?,?,?,?,?)",
                 (d['name'], d['category'], d['price'], d['stock'], d.get('min_stock',5)))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE product SET name=?,category=?,price=?,stock=? WHERE id=?",
                 (d['name'], d['category'], d['price'], d['stock'], id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db()
    conn.execute("DELETE FROM product WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ================= SEARCH =================

@app.route('/api/search')
def search():
    q = request.args.get('q','')
    conn = get_db()
    rows = conn.execute("SELECT * FROM product WHERE name LIKE ?", (f'%{q}%',)).fetchall()
    conn.close()
    return jsonify([dict(x) for x in rows])

# ================= BILLING =================

@app.route('/api/bill', methods=['POST'])
def create_bill():
    d = request.json
    conn = get_db()

    total = 0
    for item in d['items']:
        total += item['price'] * item['qty']

    cur = conn.cursor()
    cur.execute("INSERT INTO bill(total,created_at) VALUES(?,?)",
                (total, datetime.now().isoformat()))
    bill_id = cur.lastrowid

    for item in d['items']:
        cur.execute("INSERT INTO bill_items(bill_id,product_id,qty,price) VALUES(?,?,?,?)",
                    (bill_id, item['product_id'], item['qty'], item['price']))

        # stock reduce
        cur.execute("UPDATE product SET stock=stock-? WHERE id=?",
                    (item['qty'], item['product_id']))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'bill_id': bill_id, 'total': total})

# ================= BILL HISTORY =================

@app.route('/api/bills')
def get_bills():
    conn = get_db()
    rows = conn.execute("SELECT * FROM bill ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(x) for x in rows])

# ================= DASHBOARD =================

@app.route('/api/dashboard')
def dashboard():
    conn = get_db()

    total_products = conn.execute("SELECT COUNT(*) FROM product").fetchone()[0]
    low_stock = conn.execute("SELECT COUNT(*) FROM product WHERE stock<=min_stock").fetchone()[0]
    total_sales = conn.execute("SELECT COALESCE(SUM(total),0) FROM bill").fetchone()[0]

    conn.close()

    return jsonify({
        "total_products": total_products,
        "low_stock": low_stock,
        "total_sales": total_sales
    })

# ================= MAIN =================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)