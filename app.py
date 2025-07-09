from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from blockchain import Blockchain
import uuid
import time
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'supersecret'
bc = Blockchain()

# Cấu hình upload
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        product = {
            "product_id": str(uuid.uuid4()),
            "name": request.form["name"],
            "farmer": request.form["farmer"],
            "location": request.form["location"],
            "harvest_date": request.form["harvest_date"],
            "certification": request.form["certification"],
            "timeline": [f"🌱 Đăng ký sản phẩm lúc {time.ctime()}"]
        }
        bc.add_block(product)
        flash("🎉 Đã lưu sản phẩm thành công!")
        return redirect(url_for("products"))
    return render_template("register.html")

@app.route("/products")
def products():
    query = request.args.get("q", "").lower()
    all_products = bc.get_all_products()

    if query:
        filtered = [
            p for p in all_products
            if query in p["name"].lower() or query in p["product_id"].lower()
        ]
    else:
        filtered = all_products

    return render_template("products.html", products=filtered, query=query)

@app.route("/product/<pid>")
def detail(pid):
    p = bc.get_product_by_id(pid)
    warning = None
    files = []
    qr_code_base64 = None

    if p:
        # Cảnh báo nếu quá 7 ngày chưa tiêu thụ
        timeline = p.get("timeline", [])
        if not any("🏬 Tiêu thụ" in step for step in timeline):
            try:
                harvest_date = datetime.strptime(p["harvest_date"], "%Y-%m-%d")
                days_passed = (datetime.now() - harvest_date).days
                if days_passed > 7:
                    warning = f"⚠️ Sản phẩm đã thu hoạch {days_passed} ngày trước và chưa được tiêu thụ!"
            except Exception:
                warning = "⚠️ Không thể xác định ngày thu hoạch."

        # Danh sách file PDF nếu có
        folder = os.path.join(app.config["UPLOAD_FOLDER"], pid)
        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

        # Tạo mã QR từ URL hiện tại
        try:
            qr_img = qrcode.make(request.url)
            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            print("❌ Lỗi tạo QR:", e)

    return render_template(
        "product_detail.html",
        product=p,
        files=files,
        pid=pid,
        warning=warning,
        qr_code=qr_code_base64
    )

@app.route("/product/<pid>/update", methods=["POST"])
def update_timeline(pid):
    product = bc.get_product_by_id(pid)
    if not product:
        return "Sản phẩm không tồn tại", 404

    step = request.form.get("step")
    time_string = time.ctime()

    label = {
        "pack": "📦 Đóng gói",
        "ship": "🚚 Vận chuyển",
        "sell": "🏬 Tiêu thụ"
    }.get(step, "🔁 Cập nhật")

    product["timeline"].append(f"{label} lúc {time_string}")
    flash("✅ Cập nhật chuỗi cung ứng thành công!")
    return redirect(url_for("detail", pid=pid))

@app.route("/product/<pid>/upload", methods=["POST"])
def upload_document(pid):
    product = bc.get_product_by_id(pid)
    if not product:
        return "Sản phẩm không tồn tại", 404

    if "file" not in request.files:
        flash("❌ Không có file được chọn.")
        return redirect(url_for("detail", pid=pid))

    file = request.files["file"]
    if file.filename == "":
        flash("❌ Chưa chọn file.")
        return redirect(url_for("detail", pid=pid))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        product_folder = os.path.join(app.config["UPLOAD_FOLDER"], pid)
        os.makedirs(product_folder, exist_ok=True)
        file.save(os.path.join(product_folder, filename))
        flash("✅ Tải lên tài liệu thành công!")
    else:
        flash("❌ Chỉ cho phép file PDF.")
    return redirect(url_for("detail", pid=pid))

@app.route("/uploads/<pid>/<filename>")
def download_document(pid, filename):
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], pid), filename)

if __name__ == "__main__":
    app.run(debug=True)
