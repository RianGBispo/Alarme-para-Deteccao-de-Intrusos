import cv2
import numpy as np
import logging
import copy
import pygame
import time
import win32com.client as win32
from io import BytesIO
import base64

# Configurando o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FRAME_START = 30  # Frame inicial para iniciar a detecção de objetos


def send_email(subject, body, attachment=None):
    try:
        outlook = win32.Dispatch('outlook.application')
        email = outlook.CreateItem(0)
        email.To = 'your.email@email.com'
        email.Subject = subject
        email.HTMLBody = body

        if attachment is not None:
            _, img_encoded = cv2.imencode('.jpg', attachment, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')
            img_tag = f'<img src="data:image/jpeg;base64,{img_base64}" alt="Detected Frame">'
            email.HTMLBody += f'<p>{img_tag}</p>'

        email.Send()
        logging.info('Email enviado.')
    except Exception as e:
        logging.error(f'Erro ao enviar e-mail: {str(e)}')

# Configurações de Texto
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 1
font_color = (0, 0, 255)  # Cor

def draw_bounded_label(frame, label, x, y, w, h, font, font_scale, font_color, font_thickness, background_color):
    text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]

    # Coordenadas para posicionar o rótulo no centro da caixa delimitadora
    text_x = int(x)
    text_y = int(y - 5)

    # Desenha o retângulo de fundo para o rótulo
    cv2.rectangle(frame, (text_x - 5, text_y - text_size[1] - 5), (text_x + text_size[0] + 5, text_y + 5), background_color, -1)

    # Adiciona o texto sobre o fundo
    cv2.putText(frame, label, (text_x, text_y), font, font_scale, font_color, font_thickness)
###


# Inicializando o mixer do pygame
pygame.mixer.init()

# Carregando o som do alarme
alarm_sound = pygame.mixer.Sound("data/alarm.wav")

def stack_images(img_list, cols, scale=1):
    """
    Empilha imagens juntas para exibir em uma única janela.
    """
    img_list = copy.deepcopy(img_list)

    width = img_list[0].shape[1]
    height = img_list[0].shape[0]
    img_blank = np.zeros((height, width, 3), np.uint8)

    rows = -(-len(img_list) // cols)  # Calcula ceil da divisão
    img_list.extend([img_blank] * (cols * rows - len(img_list)))

    for i in range(len(img_list)):
        if img_list[i].shape[:2] != (height, width) or scale != 1:
            img_list[i] = cv2.resize(img_list[i], (0, 0), None, scale, scale)
        if len(img_list[i].shape) == 2:
            img_list[i] = cv2.cvtColor(img_list[i], cv2.COLOR_GRAY2BGR)

    ver_images = [np.vstack(img_list[i:i + cols]) for i in range(0, len(img_list), cols)]
    return np.hstack(ver_images)


def main():
    logging.info("Iniciando a transmissão da câmera de vigilância.")

    video_source = "data/intruso02.mp4"
    cap = cv2.VideoCapture(video_source)
    bg_sub = cv2.createBackgroundSubtractorKNN(history=200)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    wait_time = int(1000 / fps)

    ksize = (5, 5)
    frame_count = 0
    intruder_detected = False
    cooldown_time = 5  # Tempo de cooldown em segundos
    last_alarm_time = time.time() - cooldown_time  # Inicializando o tempo do último alarme
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("Finalizando a transmissão da câmera de vigilância.")
            break

        frame_count += 1

        # Fase 1 - Criar uma máscara para isolar o fundo
        fg_mask = bg_sub.apply(frame)

        # Fase 2 - Aplicar a máscara no frame com erosão para reduzir ruído
        fg_mask_eroded = cv2.erode(fg_mask, np.ones(ksize, np.uint8))

        # Fase 3 - Detecção de movimento após FRAME_START
        if frame_count > FRAME_START:
            motion_area = cv2.findNonZero(fg_mask_eroded)
            if motion_area is not None:
                x, y, w, h = cv2.boundingRect(motion_area)
                intruder_detected = True
                if w > 100 and h > 100:

                    logging.info("Intruso detectado!")

                    # Adiciona o rótulo à imagem
                    draw_bounded_label(frame, "Intruso", x, y, w, h, font, 0.5, (255, 2558, 255), 2, (0, 0, 255))

                    # Adiciona texto à imagem
                    cv2.putText(frame, "Intruso Detectado!", (10, 20), font, font_scale, font_color, font_thickness)

                    # Fase 4 - Detecção de contornos
                    contours, hierarchy = cv2.findContours(fg_mask_eroded, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

                    fg_mask_eroded = cv2.cvtColor(fg_mask_eroded, cv2.COLOR_GRAY2BGR)

                    if len(contours) > 0:
                        cv2.drawContours(fg_mask_eroded, contours, -1, (0, 255, 0), 2)

                    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

                    top_3_contours = sorted_contours[:3]

                    rects = [cv2.boundingRect(contour) for contour in top_3_contours]

                    x1s, y1s, x2s, y2s = zip(*[(x, y, x + w, y + h) for x, y, w, h in rects])

                    x1 = min(x1s)
                    y1 = min(y1s)
                    x2 = max(x2s)
                    y2 = max(y2s)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

                    # Verificar o cooldown antes de acionar o alarme
                    current_time = time.time()
                    if current_time - last_alarm_time >= cooldown_time:
                        alarm_sound.play()
                        last_alarm_time = current_time

                        # Definindo o assunto e enviando o email
                        email_subject = 'Intruso Detectado!!!'
                        email_body = '<p>Detectamos uma possível invasão, por favor verifique.</p>'
                        send_email(email_subject, email_body, frame)
                elif w <= 100 or h <= 100:
                    intruder_detected = False

        stacked_img = stack_images([frame, fg_mask_eroded], 2, 1)

        cv2.imshow("Camera de Vigilancia", stacked_img)

        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
