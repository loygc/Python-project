__author__ = "susmote"

import qrcode
qr = qrcode.QRCode(
    version=20,
    error_correction=qrcode.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data("hello world")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save('test.jpg')