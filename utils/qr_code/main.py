import qrcode

from base.pydrive.google_drive import subir_archivo


def crear_codigo_qr(link, ruta_file):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(ruta_file)


def crear_svg_qr(method=''):
    import qrcode
    import qrcode.image.svg

    if method == 'basic':
        # Simple factory, just a set of rects.
        factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
        # Fragment factory (also just a set of rects)
        factory = qrcode.image.svg.SvgFragmentImage
    else:
        # Combined path factory, fixes white space that may occur when zooming
        factory = qrcode.image.svg.SvgPathImage

    img = qrcode.make('https://www.youtube.com', image_factory=factory)
    img.save(r'C:\Users\isaac\Desktop\desarrollos_flask\app_modular\utils\qr_code\prueba3.svg')
    # ruta = subir_archivo(r'C:\Users\isaac\Desktop\desarrollos_flask\app_modular\utils\qr_code\prueba.svg',
    #                      '1uyQLufNG2wgzF06JJPmguN2uvyI56mPI')
    # return ruta


if __name__ == '__main__':
    # crear_codigo_qr('https://www.youtube.com',r'C:\Users\isaac\Desktop\desarrollos_flask\app_modular\utils\qr_code\prueba.png')
    crear_svg_qr(method='fragment')
