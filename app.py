from flask import Flask, render_template, request
from blockchain import Blockchain
import os
import qrcode

app = Flask(__name__)

# Initialize Blockchain
blockchain = Blockchain()

# Ensure QR folder exists
os.makedirs("static/qrcodes", exist_ok=True)


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# ADD PRODUCT
@app.route('/add_product', methods=['POST'])
def add_product():

    product_name = request.form['product_name']
    manufacturer = request.form['manufacturer']

    # Get previous block
    previous_block = blockchain.get_previous_block()

    # Create new blockchain block
    blockchain.create_block(
        {
            'product_name': product_name,
            'manufacturer': manufacturer
        },
        previous_block['hash']
    )

    # QR Verification Link
    verification_link = (
        f"https://blockchain-0kt1.onrender.com/"
        f"verify_product_qr/{product_name}"
    )

    # Generate QR Code
    qr = qrcode.make(verification_link)

    # Save QR Image
    qr_path = f"static/qrcodes/{product_name}.png"
    qr.save(qr_path)

    # Show success page
    return render_template(
        'success.html',
        product_name=product_name,
        qr_image=f"{product_name}.png"
    )


# VERIFY PAGE (Manual Verification)
@app.route('/verify')
def verify_page():
    return render_template('verify.html')


# VERIFY PRODUCT USING FORM
@app.route('/verify_product', methods=['POST'])
def verify_product():

    product_name = request.form['product_name']

    result = blockchain.verify_product(product_name)

    return render_template(
        'result.html',
        result=result,
        product_name=product_name
    )


# VERIFY PRODUCT USING QR
@app.route('/verify_product_qr/<product_name>')
def verify_product_qr(product_name):

    result = blockchain.verify_product(product_name)

    return render_template(
        'result.html',
        result=result,
        product_name=product_name
    )


# RUN APPLICATION
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )