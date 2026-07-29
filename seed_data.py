"""
seed_data.py  –  Populate grocery.db with realistic sample data
Run: python seed_data.py
"""
import sqlite3, hashlib, random
from datetime import datetime, timedelta

DB = 'grocery.db'
conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# ── Helper ────────────────────────────────────────────────────────────────────
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def ts(days_ago=0, hr=10, mn=0):
    d = datetime.now() - timedelta(days=days_ago)
    return d.replace(hour=hr, minute=mn, second=0, microsecond=0).isoformat()

# ── 1. Suppliers ──────────────────────────────────────────────────────────────
suppliers = [
    ('FreshMart Wholesale', '9876543210', 'freshmart@example.com', 'Mumbai, MH', 'GST22AAAAA0000A1Z5'),
    ('DairyBest Co.',       '9123456780', 'dairybest@example.com', 'Pune, MH',   'GST27BBBBB1111B2Z6'),
    ('GrainHouse Pvt Ltd',  '9001234567', 'grainhouse@example.com','Nagpur, MH', 'GST27CCCCC2222C3Z7'),
    ('BevTech Imports',     '9988776655', 'bevtech@example.com',   'Delhi, DL',  'GST07DDDDD3333D4Z8'),
    ('SnackWorld Dist.',    '9765432100', 'snackworld@example.com','Hyderabad, TS','GST36EEEEE4444E5Z9'),
    ('HomeEssentials Ltd',  '9654321099', 'homeessentials@example.com','Bengaluru, KA','GST29FFFFF5555F6Z0'),
]
c.executemany(
    'INSERT OR IGNORE INTO supplier(name,contact,email,address,gst_no) VALUES(?,?,?,?,?)',
    suppliers
)
sup_ids = [r[0] for r in c.execute('SELECT id FROM supplier ORDER BY id').fetchall()]
print(f"Suppliers: {len(sup_ids)} ready")

# ── 2. Staff ──────────────────────────────────────────────────────────────────
staff = [
    ('Admin User',   'admin',    sha('admin123'),   'admin',   '9000000001', 'admin@store.com'),
    ('Priya Sharma', 'cashier1', sha('cash123'),    'cashier', '9000000002', 'priya@store.com'),
    ('Rahul Mehta',  'cashier2', sha('cash456'),    'cashier', '9000000003', 'rahul@store.com'),
    ('Sneha Joshi',  'manager1', sha('mgr123'),     'manager', '9000000004', 'sneha@store.com'),
]
for s in staff:
    c.execute(
        'INSERT OR IGNORE INTO staff(name,username,password,role,phone,email) VALUES(?,?,?,?,?,?)', s
    )
staff_ids = [r[0] for r in c.execute('SELECT id FROM staff ORDER BY id').fetchall()]
print(f"Staff: {len(staff_ids)} ready")

# ── 3. Customers ──────────────────────────────────────────────────────────────
customers = [
    ('Amit Verma',    '9800001111', 'amit@gmail.com',   '12 MG Road, Pune'),
    ('Sunita Patel',  '9800002222', 'sunita@gmail.com', '45 FC Road, Mumbai'),
    ('Deepak Rao',    '9800003333', 'deepak@gmail.com', '7 Hill St, Nagpur'),
    ('Meena Gupta',   '9800004444', 'meena@gmail.com',  '22 Park Ave, Delhi'),
    ('Karan Singh',   '9800005555', 'karan@gmail.com',  '88 Lake View, Pune'),
    ('Lakshmi Iyer',  '9800006666', 'lakshmi@gmail.com','3 Temple Rd, Chennai'),
    ('Farhan Khan',   '9800007777', 'farhan@gmail.com', '60 Station Rd, Hyderabad'),
    ('Neha Desai',    '9800008888', 'neha@gmail.com',   '15 Senapati Rd, Pune'),
    ('Walk-in Customer','',         '',                 ''),
]
c.executemany(
    'INSERT OR IGNORE INTO customer(name,phone,email,address) VALUES(?,?,?,?)',
    customers
)
cust_ids = [r[0] for r in c.execute('SELECT id FROM customer ORDER BY id').fetchall()]
print(f"Customers: {len(cust_ids)} ready")

# ── 4. Products ───────────────────────────────────────────────────────────────
# (name, category, price, stock, unit, supplier_idx, barcode, min_stock)
products = [
    # Fruits & Vegetables  → supplier 0 (FreshMart)
    ('Apple',             'Fruits & Vegetables',  60.0,  80, 'kg',  0, 'BAR001', 10),
    ('Banana',            'Fruits & Vegetables',  30.0, 120, 'dz',  0, 'BAR002', 15),
    ('Tomato',            'Fruits & Vegetables',  25.0,  60, 'kg',  0, 'BAR003', 10),
    ('Onion',             'Fruits & Vegetables',  20.0, 100, 'kg',  0, 'BAR004', 15),
    ('Potato',            'Fruits & Vegetables',  18.0, 150, 'kg',  0, 'BAR005', 20),
    ('Spinach',           'Fruits & Vegetables',  15.0,  40, 'bunch',0,'BAR006',  8),
    ('Carrot',            'Fruits & Vegetables',  35.0,  70, 'kg',  0, 'BAR007', 10),
    ('Mango',             'Fruits & Vegetables',  80.0,  50, 'kg',  0, 'BAR008', 10),

    # Dairy  → supplier 1 (DairyBest)
    ('Milk 1L',           'Dairy',               55.0, 200, 'pcs', 1, 'BAR009', 30),
    ('Butter 500g',       'Dairy',              120.0,  60, 'pcs', 1, 'BAR010', 10),
    ('Paneer 200g',       'Dairy',               90.0,  50, 'pcs', 1, 'BAR011', 10),
    ('Curd 400g',         'Dairy',               45.0,  80, 'pcs', 1, 'BAR012', 15),
    ('Cheese Slice',      'Dairy',              110.0,  40, 'pcs', 1, 'BAR013',  8),

    # Grains & Pulses  → supplier 2 (GrainHouse)
    ('Basmati Rice 5kg',  'Grains & Pulses',    350.0, 100, 'pcs', 2, 'BAR014', 15),
    ('Wheat Flour 5kg',   'Grains & Pulses',    220.0,  80, 'pcs', 2, 'BAR015', 15),
    ('Toor Dal 1kg',      'Grains & Pulses',     95.0,  90, 'pcs', 2, 'BAR016', 10),
    ('Moong Dal 1kg',     'Grains & Pulses',    110.0,  70, 'pcs', 2, 'BAR017', 10),
    ('Chana Dal 1kg',     'Grains & Pulses',     85.0,  65, 'pcs', 2, 'BAR018', 10),

    # Beverages  → supplier 3 (BevTech)
    ('Bisleri Water 1L',  'Beverages',           20.0, 300, 'pcs', 3, 'BAR019', 50),
    ('Coca-Cola 750ml',   'Beverages',           40.0, 120, 'pcs', 3, 'BAR020', 20),
    ('Tropicana 1L',      'Beverages',           90.0,  80, 'pcs', 3, 'BAR021', 10),
    ('Tea Powder 500g',   'Beverages',          130.0,  60, 'pcs', 3, 'BAR022', 10),
    ('Coffee 100g',       'Beverages',          200.0,  40, 'pcs', 3, 'BAR023',  8),

    # Snacks  → supplier 4 (SnackWorld)
    ('Lays Chips',        'Snacks',              20.0, 150, 'pcs', 4, 'BAR024', 20),
    ('Biscuit Pack',      'Snacks',              30.0, 200, 'pcs', 4, 'BAR025', 25),
    ('Maggi 12pk',        'Snacks',             130.0,  80, 'pcs', 4, 'BAR026', 10),
    ('Namkeen 200g',      'Snacks',              45.0,  90, 'pcs', 4, 'BAR027', 15),

    # Household  → supplier 5 (HomeEssentials)
    ('Detergent 1kg',     'Household',           85.0,  70, 'pcs', 5, 'BAR028', 10),
    ('Dish Soap 500ml',   'Household',           65.0,  60, 'pcs', 5, 'BAR029', 10),
    ('Toilet Paper 6pk',  'Household',           90.0,  50, 'pcs', 5, 'BAR030', 10),
    ('Floor Cleaner 1L',  'Household',           80.0,  40, 'pcs', 5, 'BAR031',  8),
]

for p in products:
    name, cat, price, stock, unit, sup_idx, barcode, min_stock = p
    sup_id = sup_ids[sup_idx] if sup_idx < len(sup_ids) else None
    c.execute(
        'INSERT OR IGNORE INTO product(name,category,price,stock,unit,supplier_id,barcode,min_stock) VALUES(?,?,?,?,?,?,?,?)',
        (name, cat, price, stock, unit, sup_id, barcode, min_stock)
    )

prod_rows = c.execute('SELECT id, price FROM product ORDER BY id').fetchall()
price_map = {pid: price for pid, price in prod_rows}
prod_ids  = [r[0] for r in prod_rows]
print(f"Products: {len(prod_ids)} ready")

# ── 5. Billing History (7 days) ───────────────────────────────────────────────
c.execute('DELETE FROM bill_item')
c.execute('DELETE FROM bill')

# (days_ago, hour, [(product_id_index, qty), ...], customer_idx, staff_idx, payment, discount%)
bill_templates = [
    (6, 10, [(0,2),(8,3),(13,1)],  0, 1, 'cash',   0),
    (6, 14, [(2,5),(3,3),(9,1)],   1, 2, 'card',   5),
    (5, 11, [(4,3),(5,2),(19,4)],  2, 1, 'cash',   0),
    (5, 16, [(7,2),(10,1),(11,2)], 8, 2, 'upi',    0),
    (4, 9,  [(19,2),(20,4),(23,3)],3, 1, 'cash',   0),
    (4, 13, [(1,6),(10,2),(24,5)], 4, 2, 'upi',   10),
    (3, 10, [(15,2),(16,1),(27,1)],5, 1, 'cash',   0),
    (3, 15, [(7,3),(12,2),(25,2)], 6, 2, 'card',   0),
    (2, 10, [(13,1),(20,3),(23,1)],7, 1, 'cash',   0),
    (2, 17, [(0,2),(8,4),(23,2),(24,3)], 8, 2, 'upi', 0),
    (1, 11, [(3,4),(4,5),(18,6)],  0, 1, 'cash',   0),
    (1, 14, [(9,1),(11,2),(26,2)], 1, 2, 'card',   5),
    (0, 9,  [(0,1),(8,2),(23,2),(24,3)], 2, 1, 'cash', 0),
    (0, 11, [(7,2),(10,1),(20,4)], 3, 2, 'upi',    0),
    (0, 14, [(13,3),(25,5),(27,2)],4, 1, 'cash',   0),
]

tax_rate = 5  # 5% GST
for i, (days_ago, hr, items, cust_idx, staff_idx, pay, disc_pct) in enumerate(bill_templates):
    # resolve real IDs: product index → actual id
    resolved = []
    for p_idx, qty in items:
        if p_idx < len(prod_ids):
            pid   = prod_ids[p_idx]
            price = price_map[pid]
            resolved.append((pid, qty, price))

    subtotal  = sum(price * qty for pid, qty, price in resolved)
    discount  = round(subtotal * disc_pct / 100, 2)
    tax       = round((subtotal - discount) * tax_rate / 100, 2)
    total     = round(subtotal - discount + tax, 2)
    bill_no   = f"BILL{datetime.now().year}{i+1:04d}"
    cust_id   = cust_ids[cust_idx] if cust_idx < len(cust_ids) else None
    staff_id  = staff_ids[staff_idx] if staff_idx < len(staff_ids) else None
    created   = ts(days_ago, hr)

    c.execute(
        'INSERT INTO bill(bill_no,customer_id,staff_id,subtotal,discount,tax,total,payment_mode,created_at) VALUES(?,?,?,?,?,?,?,?,?)',
        (bill_no, cust_id, staff_id, subtotal, discount, tax, total, pay, created)
    )
    bill_id = c.lastrowid

    for pid, qty, price in resolved:
        item_total = round(price * qty, 2)
        c.execute(
            'INSERT INTO bill_item(bill_id,product_id,qty,price,total) VALUES(?,?,?,?,?)',
            (bill_id, pid, qty, price, item_total)
        )

print(f"Bills inserted: {len(bill_templates)}")

# ── 6. Purchase Records ───────────────────────────────────────────────────────
purchases = [
    (0, 0,  500, 45.0,  14),  # supplier 0 → Apple  500qty
    (0, 1,  600, 20.0,  14),  # supplier 0 → Banana
    (1, 8,  300, 40.0,  10),  # supplier 1 → Milk
    (1, 9,  100, 90.0,   7),  # supplier 1 → Butter
    (2, 13, 200, 290.0,  5),  # supplier 2 → Rice
    (2, 15, 120,  70.0,  3),  # supplier 2 → Toor Dal
    (3, 18, 400,  12.0,  2),  # supplier 3 → Water
    (3, 19, 200,  28.0,  1),  # supplier 3 → Coke
    (4, 23, 300,  12.0,  5),  # supplier 4 → Lays
    (4, 25, 100, 100.0,  3),  # supplier 4 → Maggi
    (5, 27, 150,  60.0,  7),  # supplier 5 → Detergent
    (5, 28, 120,  45.0,  4),  # supplier 5 → Dish Soap
]

for sup_idx, prod_idx, qty, price, days_ago in purchases:
    if sup_idx < len(sup_ids) and prod_idx < len(prod_ids):
        total = round(qty * price, 2)
        c.execute(
            'INSERT INTO purchase(supplier_id,product_id,qty,price,total,purchased_at) VALUES(?,?,?,?,?,?)',
            (sup_ids[sup_idx], prod_ids[prod_idx], qty, price, total, ts(days_ago))
        )

print(f"Purchases inserted: {len(purchases)}")

conn.commit()
conn.close()
print("\nDone! grocery.db populated successfully.")
