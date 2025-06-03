import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

def crear_carpeta(destino):
    if not os.path.exists(destino):
        os.makedirs(destino)

def generar_qr(nombre, carpeta_destino):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(nombre)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Añadir el nombre debajo del QR
    ancho, alto = img.size
    nuevo_alto = alto + 40
    imagen_con_texto = Image.new("RGB", (ancho, nuevo_alto), "white")
    imagen_con_texto.paste(img, (0, 0))

    draw = ImageDraw.Draw(imagen_con_texto)
    try:
        fuente = ImageFont.truetype("arial.ttf", 20)
    except:
        fuente = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), nombre, font=fuente)
    texto_ancho = bbox[2] - bbox[0]
    texto_alto = bbox[3] - bbox[1]
    draw.text(((ancho - texto_ancho) / 2, alto + 10), nombre, fill="black", font=fuente)    

    ruta_archivo = os.path.join(carpeta_destino, f"{nombre}.png")
    imagen_con_texto.save(ruta_archivo)

def generar_pdf(carpeta, archivo_pdf):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=10)

    imagenes = sorted(os.listdir(carpeta))
    imagenes = [img for img in imagenes if img.endswith(".png")]

    for i, imagen in enumerate(imagenes):
        ruta_img = os.path.join(carpeta, imagen)
        pdf.add_page()
        pdf.image(ruta_img, x=30, y=30, w=150)  # Tamaño y centrado

    pdf.output(archivo_pdf)
    print(f"\n✅ PDF generado: {archivo_pdf}")

def main():
    print("Introduce un nombre por línea (deja una línea vacía para terminar):")
    nombres = []
    while True:
        nombre = input().strip()
        if nombre == "":
            break
        nombres.append(nombre)

    if not nombres:
        print("No se ingresaron nombres.")
        return

    carpeta = "codigos_qr"
    crear_carpeta(carpeta)

    for nombre in nombres:
        generar_qr(nombre, carpeta)

    print(f"\n🖼️ Se generaron {len(nombres)} imágenes QR en la carpeta '{carpeta}'.")
    generar_pdf(carpeta, "codigos_qr_guarderia.pdf")

if __name__ == "__main__":
    main()
