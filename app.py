from flask import Flask, render_template, request
from blockchain import Blockchain
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

    # FORM DATA

    product_name = request.form['product_name']

    manufacturer = request.form['manufacturer']

    product_id = request.form['product_id']

    manufacturing_date = request.form['manufacturing_date']

    product_image = request.files['product_image']

    # CHECK DUPLICATE PRODUCT

    if blockchain.product_exists(product_id):

        return render_template(

            'duplicate.html',

            product_id=product_id
        )

    # SAVE PRODUCT IMAGE

    image_filename = product_image.filename

    image_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        image_filename
    )

    product_image.save(image_path)

    # GET PREVIOUS BLOCK

    previous_block = blockchain.get_previous_block()

    # CREATE NEW BLOCK

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

    # QR VERIFICATION LINK

    verification_link = (
    f"https://blockchain-0kt1.onrender.com/"
    f"verify_product_qr/{product_name}"
)

    # GENERATE QR CODE

    qr = qrcode.make(verification_link)

    # SAVE QR IMAGE

    qr_path = f"static/qrcodes/{product_name}.png"

    qr.save(qr_path)

    # SHOW SUCCESS PAGE

    return render_template(

        'success.html',

        product_name=product_name,

        qr_image=f"{product_name}.png"
    )


# =========================
# VERIFY PAGE
# =========================

@app.route('/verify')
def verify_page():

    return render_template('verify.html')


# =========================
# SCAN PRODUCT PAGE
# =========================

@app.route('/scan')
def scan_product():

    return render_template('scan.html')


# =========================
# VERIFY PRODUCT MANUALLY
# =========================

@app.route('/verify_product', methods=['POST'])
def verify_product():

    product_name = request.form['product_name']

    result = blockchain.verify_product(product_name)

    return render_template(

        'result.html',

        result=result
    )


# =========================
# VERIFY PRODUCT USING QR
# =========================

@app.route('/verify_product_qr/<product_name>')
def verify_product_qr(product_name):

    result = blockchain.verify_product(product_name)

    return render_template(

        'result.html',

        result=result
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(

        host="0.0.0.0",

        port=port,

        debug=True
    )