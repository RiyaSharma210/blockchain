from flask import Flask, render_template, request
from blockchain import Blockchain
import os
import qrcode

app = Flask(__name__)

blockchain = Blockchain()

# Ensure QR folder exists (IMPORTANT for Render)
os.makedirs("static/qrcodes", exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_product', methods=['POST'])
def add_product():

    product_name = request.form['product_name']
    manufacturer = request.form['manufacturer']

    previous_block = blockchain.get_previous_block()

    blockchain.create_block(
        {
            'product_name': product_name,
            'manufacturer': manufacturer
        },
        previous_block['hash']
    )

    # QR Verification Link
    verification_link = f"https://blockchain-0kt1.onrender.com/verify_product_qr/{product_name}"

    # Generate QR Code
    qr = qrcode.make(verification_link)

    # Save QR Image
    qr_path = f"static/qrcodes/{product_name}.png"
    qr.save(qr_path)

    return render_template(
        'success.html',
        product_name=product_name,
        qr_image=f"{product_name}.png"
    )


@app.route('/verify')
def verify_page():
    return render_template('verify.html')


@app.route('/verify_product', methods=['POST'])
def verify_product():

    product_name = request.form['product_name']

    result = blockchain.verify_product(product_name)

    return render_template(
        'result.html',
        result=result,
        product_name=product_name
    )


@app.route('/verify_product_qr/<product_name>')
def verify_product_qr(product_name):

    result = blockchain.verify_product(product_name)

    return render_template(
        'result.html',
        result=result,
        product_name=product_name
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)