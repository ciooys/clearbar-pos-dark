
from flask import Flask, g, render_template, request, jsonify, redirect, url_for
import sqlite3, os, uuid, datetime

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "clearbar.db")
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    if not os.path.exists(DB_PATH):
        with open(os.path.join(BASE_DIR, "schema.sql"), "r") as f:
            sql = f.read()
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(sql)
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO employees (username,password,role) VALUES (?,?,?)", ("admin","password123","admin"))
        items = [
            ("BEER-TSINGTAO","青岛纯生 500ml",18.0,10.0,50,1),
            ("BEER-BUD","百威 500ml",20.0,12.0,40,1),
            ("COCK-MOJ","莫吉托（杯）",38.0,12.0,30,1),
            ("COCK-GIN","金汤力（杯）",40.0,15.0,20,1),
            ("SNACK-1","小食拼盘",25.0,8.0,20,0)
        ]
        for sku,name,price,cost,stock,is_alc in items:
            cur.execute("INSERT OR IGNORE INTO inventory (sku,name,price,cost,stock,is_alcohol) VALUES (?,?,?,?,?,?)",
                        (sku,name,price,cost,stock,is_alc))
        conn.commit()
        conn.close()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'clearbar-secret-key'
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def query(sql, args=(), one=False):
    cur = get_db().execute(sql, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur.lastrowid

@app.route("/")
def index():
    return redirect(url_for('admin'))

@app.route("/admin")
def admin():
    return render_template("admin_dark.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    user = query("SELECT * FROM employees WHERE username=? AND password=?", (data.get("username"), data.get("password")), one=True)
    if user:
        return jsonify({"ok": True, "user": {"username": user["username"], "role": user["role"]}})
    return jsonify({"ok": False, "msg":"invalid"})

@app.route("/api/inventory")
def api_inventory():
    rows = query("SELECT * FROM inventory")
    return jsonify([dict(r) for r in rows])

@app.route("/api/members", methods=["POST"])
def api_create_member():
    d = request.json
    try:
        mid = execute("INSERT INTO members (phone,name,balance,points) VALUES (?,?,?,?)",
                     (d.get("phone"), d.get("name"), d.get("balance",0), d.get("points",0)))
        return jsonify({"ok": True, "id": mid})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)})

@app.route("/api/members/phone/<phone>")
def api_get_member_phone(phone):
    m = query("SELECT * FROM members WHERE phone=?", (phone,), one=True)
    if not m: return jsonify({"ok": False})
    return jsonify({"ok": True, "member": dict(m)})

@app.route("/api/orders", methods=["POST"])
def api_create_order():
    d = request.json
    order_no = "ORD" + datetime.datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4())[:4]
    member_id = d.get("member_id")
    items = d.get("items", [])
    total = sum([i["qty"] * i["price"] for i in items])
    oid = execute("INSERT INTO orders (order_no, member_id, total) VALUES (?,?,?)", (order_no, member_id, total))
    for it in items:
        execute("INSERT INTO order_items (order_id, inventory_id, qty, price) VALUES (?,?,?,?)",
                (oid, it["inventory_id"], it["qty"], it["price"]))
        execute("UPDATE inventory SET stock = stock - ? WHERE id=?", (it["qty"], it["inventory_id"]))
    return jsonify({"ok": True, "order_id": oid, "order_no": order_no, "total": total})

@app.route("/api/admin/orders")
def api_admin_orders():
    rows = query("SELECT * FROM orders ORDER BY created_at DESC")
    return jsonify([dict(r) for r in rows])

@app.route("/h5/order")
def h5_order():
    items = query("SELECT * FROM inventory")
    return render_template("h5_dark.html", items=[dict(x) for x in items])

@app.route("/api/stored", methods=["POST"])
def api_store_bottle():
    d = request.json
    label = "BTL-" + datetime.datetime.datetime.now().strftime("%y%m%d%H%M%S") + str(uuid.uuid4())[:4]
    sid = execute("INSERT INTO stored_bottles (member_id, inventory_id, bottle_label, qty, note) VALUES (?,?,?,?,?)",
                  (d.get("member_id"), d.get("inventory_id"), label, d.get("qty",1), d.get("note","")))
    return jsonify({"ok": True, "stored_id": sid, "label": label})

@app.route("/api/stored/member/<int:mid>")
def api_member_stored(mid):
    rows = query("SELECT sb.*, i.name FROM stored_bottles sb JOIN inventory i ON sb.inventory_id=i.id WHERE sb.member_id=?", (mid,))
    return jsonify({"ok": True, "stored": [dict(r) for r in rows]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
