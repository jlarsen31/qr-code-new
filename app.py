from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import io


from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        image = request.files['image']

        # Save image to disk
        image.save(image.filename)

        # Generate vCard QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Generate image buffer
        img_buffer = BytesIO()
        qr_img.save('contact.png')
        img_buffer.seek(0)

        # Open the two images
        image1 = Image.open("contact.png").convert("RGBA")
        image2 = Image.open(image.filename).convert("RGBA")
        #image2 = Image.open("fedora.jpg").convert("RGBA")

        # Resize the second image to match the first image
        image2 = image2.resize(image1.size)

        # Get the dimensions of the two images
        width1, height1 = image1.size
        width2, height2 = image2.size

        # Get the maximum height between the two images
        max_height = max(height1, height2)

        # Combine the two images
        combined_image = Image.new('RGB', (width1 + width2, max_height))

        # Paste the two images into the new image side by side
        combined_image.paste(image1, (0, 0))
        combined_image.paste(image2, (width1, 0))

        #rotate 90 degrees
        combined_image = combined_image.rotate(-90, expand=True)

        # Save the combined image
        combined_image.save("static/combined_image.png")

        #combined_image.show()

        # Render template with QR code image
        #return send_file(combined_image, mimetype='image/png')
        return render_template('qr_code.html')
        #return render_template('qr_code.html', qr_img_data=base64.b64encode(img_buffer.getvalue()))

    # Render form template for GET requests
    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
