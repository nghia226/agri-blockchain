from flask import Flask, request, render_template_string, redirect, url_for
import hashlib
import json
import time
import uuid

app = Flask(__name__)

# ===== Blockchain Setup =====
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"info": "Genesis Block"}, "0")

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, last_block.hash)
        self.chain.append(new_block)

    def get_all_products(self):
        return [block.data for block in self.chain if block.index != 0]

    def get_product_by_id(self, product_id):
        for block in self.chain:
            if block.data.get("product_id") == product_id:
                return block.data
        return None

blockchain = Blockchain()

# ===== HTML Templates =====
TEMPLATE_HOME = """
<!DOCTYPE html>
<html>
<head><title>AgriChain</title></head>
<body>
    <h2>🌾 AgriChain: Theo dõi chuỗi cung ứng nông sản</h2>
    <ul>
        <li><a href="/register">Đăng ký sản phẩm</a></li>
        <li><a href="/products">Xem tất cả sản phẩm</a></li>
    </ul>
</body>
</html>
"""

TEMPLATE_REGISTER = """
<!DOCTYPE html>
<html>
<head><title>Đăng ký sản phẩm</title></head>
<body>
    <h2>📝 Đăng ký sản phẩm nông sản</h2>
    <form method="POST">
        Tên sản phẩm: <input type="text" name="name"><br>
        Nông dân: <input type="text" name="farmer"><br>
        Địa điểm: <input type="text" name="location"><br>
        Ngày thu hoạch: <input type="text" name="harvest_date"><br>
        Chứng nhận chất lượng: <input type="text" name="certification"><br>
        <input type="submit" value="Đăng ký">
    </form>
    <a href="/">⬅ Quay lại</a>
</body>
</html>
"""

TEMPLATE_PRODUCTS = """
<!DOCTYPE html>
<html>
<head><title>Danh sách sản phẩm</title></head>
<body>
    <h2>📦 Danh sách sản phẩm</h2>
    <ul>
    {% for p in products %}
        <li><a href="/product/{{ p['product_id'] }}">{{ p['name'] }}</a> - {{ p['farmer'] }}</li>
    {% endfor %}
    </ul>
    <a href="/">⬅ Quay lại</a>
</body>
</html>
"""

TEMPLATE_DETAIL = """
<!DOCTYPE html>
<html>
<head><title>Chi tiết sản phẩm</title></head>
<body>
    <h2>🔍 Chi tiết sản phẩm</h2>
    {% if product %}
        <p><b>ID:</b> {{ product['product_id'] }}</p>
        <p><b>Tên:</b> {{ product['name'] }}</p>
        <p><b>Nông dân:</b> {{ product['farmer'] }}</p>
        <p><b>Địa điểm:</b> {{ product['location'] }}</p>
        <p><b>Ngày thu hoạch:</b> {{ product['harvest_date'] }}</p>
        <p><b>Chứng nhận:</b> {{ product['certification'] }}</p>
        <p><b>Trạng thái xác thực:</b> Đã ghi trên Blockchain ✅</p>
    {% else %}
        <p>Không tìm thấy sản phẩm.</p>
    {% endif %}
    <a href="/products">⬅ Quay lại danh sách</a>
</body>
</html>
"""

# ===== Web Routes =====
@app.route("/")
def home():
    return TEMPLATE_HOME

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        product = {
            "product_id": str(uuid.uuid4()),
            "name": request.form["name"],
            "farmer": request.form["farmer"],
            "location": request.form["location"],
            "harvest_date": request.form["harvest_date"],
            "certification": request.form["certification"]
        }
        blockchain.add_block(product)
        return redirect(url_for("products"))
    return TEMPLATE_REGISTER

@app.route("/products")
def products():
    all_products = blockchain.get_all_products()
    return render_template_string(TEMPLATE_PRODUCTS, products=all_products)

@app.route("/product/<product_id>")
def product_detail(product_id):
    product = blockchain.get_product_by_id(product_id)
    return render_template_string(TEMPLATE_DETAIL, product=product)

if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
    except OSError:
        print("⚠️ Không thể khởi chạy Flask server. Vui lòng kiểm tra lại cổng hoặc môi trường.")
