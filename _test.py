import json
from app import app
from patterns.builder import OrderBuilder, save_order

# Create a test order
builder = (
    OrderBuilder()
    .set_items([{"product_id":"p1","name":"Смартфон","price":89990,"quantity":1,"icon":"📦","type":"physical","weight_kg":0.2}])
    .set_customer(name="admin", email="admin@omnify.store")
    .set_delivery(method="courier", cost=300)
    .set_payment(method="card")
)
order = builder.build()
save_order(order)

with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['auth_user_id'] = 'usr_admin'
    
    pages = ['/', '/cart', '/orders', '/admin', '/login', '/register', f'/orders/{order.order_id}']
    for url in pages:
        r = c.get(url, follow_redirects=True)
        body = r.data.decode('utf-8', errors='ignore')
        err = 'jinja2' in body.lower() or 'traceback' in body.lower() or 'internal server error' in body.lower()
        print(url, '->', r.status_code, '[TEMPLATE ERROR]' if err else 'OK')
