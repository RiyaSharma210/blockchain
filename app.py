from flask import Flask, render_template, request
from blockchain import Blockchain
from urllib.parse import quote, unquote
import os
import qrcode

app = Flask(__name__)

# =========================
# PRODUCT IMAGE FOLDER
# =========================
UPLOAD_FOLDER = 'static/product_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# QR CODE FOLDER
# =========================
os.makedirs("static/qrcodes", exist_ok=True)

# =========================
# INITIALIZE BLOCKCHAIN
# =========================
blockchain = Blockchain()

# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    stats = blockchain.get_statistics()
    history = blockchain.get_history()

    return render_template(
        'index.html',
        stats=stats,
        history=history
    )

# =========================
# ADD PRODUCT
# =========================
@app.route('/add_product', methods=['POST'])
def add_product():

    product_name = request.form['product_name']
    manufacturer = request.form['manufacturer']
    product_id = request.form['product_id']
    manufacturing_date = request.form['manufacturing_date']
    product_image = request.files['product_image']

    # CHECK DUPLICATE
    if blockchain.product_exists(product_id):
        return render_template('duplicate.html', product_id=product_id)

    # SAVE IMAGE
    image_filename = product_image.filename
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    product_image.save(image_path)

    # GET PREVIOUS BLOCK
    previous_block = blockchain.get_previous_block()

    # CREATE BLOCK
    blockchain.create_block(
        {
            'product_name': product_name,
            'manufacturer': manufacturer,
            'product_id': product_id,
            'manufacturing_date': manufacturing_date,
            'image': image_filename
        },
        previous_block['hash']
    )

    # =========================
    # FIXED QR LINK (IMPORTANT)
    # =========================
    verification_link = (
        f"https://blockchain-0kt1.onrender.com/"
        f"verify_product_qr?product_id={quote(product_id)}"
    )

    # GENERATE QR
    qr = qrcode.make(verification_link)

    qr_filename = f"{product_id}.png"
    qr_path = f"static/qrcodes/{qr_filename}"
    qr.save(qr_path)

    return render_template(
        'success.html',
        product_name=product_name,
        qr_image=qr_filename
    )

# =========================
# VERIFY PAGE
# =========================
@app.route('/verify')
def verify_page():
    return render_template('verify.html')

# =========================
# SCAN PAGE
# =========================
@app.route('/scan')
def scan_product():
    return render_template('scan.html')

# =========================
# MANUAL VERIFY
# =========================
@app.route('/verify_product', methods=['POST'])
def verify_product():

    product_id = request.form['product_id']

    result = blockchain.verify_product(product_id)

    return render_template('result.html', result=result)

# =========================
# QR VERIFY (FIXED)
# =========================
@app.route('/verify_product_qr')
def verify_product_qr():

    product_id = request.args.get('product_id')

    if not product_id:
        return render_template('result.html', result="INVALID QR")

    product_id = unquote(product_id)

    result = blockchain.verify_product(product_id)

    return render_template('result.html', result=result)

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )