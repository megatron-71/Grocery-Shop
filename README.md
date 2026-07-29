# 🛒 GroceryPro — Smart Shop Management System
## SY B.Sc. Computer Science Project — 2025–26


---

## 📌 Project Overview
A complete web-based Grocery Shop Management System built with:
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Single Page Application)
- **Backend:** Python 3 + Flask (REST API)
- **Database:** SQLite3 (file-based, no setup needed)

---

## 🗂️ Entities & ER Diagram
| Entity     | Attributes                                      |
|------------|-------------------------------------------------|
| Product    | id, name, category, price, stock, unit, supplier_id, min_stock |
| Customer   | id, name, phone, email, address                |
| Bill       | id, bill_no, customer_id, staff_id, total, discount, tax, payment_mode |
| Staff      | id, name, username, password (hashed), role    |
| Supplier   | id, name, contact, email, address, gst_no      |

**Relationships (Diamonds):**
- Customer **generates** Bill
- Bill **contains** Product  
- Product **purchase_from** Supplier
- Staff **creates** Bill

---

## 🚀 Setup & Run

### Step 1: Install Python dependencies
```bash
pip install flask
```

### Step 2: Run the server
```bash
python app.py
```

### Step 3: Open browser
```
http://localhost:5000
```

---

## 🔐 Login Credentials (Role-Based)
| Role     | Username | Password    | Access                        |
|----------|----------|-------------|-------------------------------|
| Admin    | admin    | admin123    | Full access to all pages      |
| Manager  | manager  | manager123  | All pages except staff mgmt   |
| Cashier  | cashier  | cashier123  | Billing and bill history only |

---

## 📄 Pages & Features

### 1. Login Page
- Role-based authentication (Admin / Manager / Cashier)
- Password hashing with SHA-256
- Session management with Flask

### 2. Dashboard
- Live stats: Products, Low Stock, Customers, Today's Bills & Revenue
- Recent bills table
- Low stock alerts

### 3. Billing Page
- Search & add products to bill
- Auto-calculate subtotal, discount %, GST tax %
- Print bill functionality
- Multiple payment modes (Cash, UPI, Card, Credit)

### 4. Stock Management
- Add / Edit / Delete products
- Category filter & search
- Stock level alerts (green=OK, red=Low)
- Purchase stock from supplier (stock-in)
- Purchase history log

### 5. Wholesaler Management
- Add / Edit / Delete suppliers
- GST number, contact, address
- Relationship with products

### 6. Customer Management
- Customer directory with CRUD
- Linked to billing

### 7. Staff Management (Admin only)
- Add staff with role assignment
- Passwords stored securely (SHA-256 hash)

### 8. Bill History
- View all past bills
- Drill-down to see bill items

### 9. ER Diagram
- Visual Entity-Relationship diagram
- Shows all entities, attributes, and relationship diamonds

---

## 🗃️ Database Schema (SQLite)
```sql
staff(id, name, username, password, role, phone, email)
supplier(id, name, contact, email, address, gst_no)
product(id, name, category, price, stock, unit, supplier_id, min_stock)
customer(id, name, phone, email, address)
bill(id, bill_no, customer_id, staff_id, subtotal, discount, tax, total, payment_mode)
bill_item(id, bill_id, product_id, qty, price, total)
purchase(id, supplier_id, product_id, qty, price, total)
```

---

## 📁 Project Structure
```
grocery/
├── app.py              ← Flask backend (Python)
├── grocery.db          ← SQLite database (auto-created)
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── static/
    └── index.html      ← Full frontend (HTML/CSS/JS)
```

---

## 🔗 API Endpoints
| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| POST   | /api/login            | Authenticate user        |
| POST   | /api/logout           | Logout                   |
| GET    | /api/me               | Current session info     |
| GET    | /api/dashboard        | Dashboard statistics     |
| GET/POST | /api/products       | List / Add products      |
| PUT/DELETE | /api/products/:id | Update / Delete product  |
| GET/POST | /api/customers      | List / Add customers     |
| GET/POST | /api/suppliers      | List / Add suppliers     |
| GET/POST | /api/staff          | List / Add staff         |
| GET/POST | /api/bills          | List / Create bills      |
| GET    | /api/bills/:id        | Get bill details         |
| GET/POST | /api/purchase       | Purchase history / Add   |

---

*GroceryPro 
