import csv
import os
import platform
import urllib.request
from datetime import datetime
from pathlib import Path
import time

import cv2
import numpy as np
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core.image import Image, ImageFormat
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode
from mediapipe.tasks.python.vision.holistic_landmarker import HolisticLandmarker, HolisticLandmarkerOptions

MODEL_URL = 'https://storage.googleapis.com/mediapipe-assets/holistic_landmarker.task'
MODEL_NAME = 'holistic_landmarker.task'


def list_cameras(max_devices=10):
    system = platform.system()
    devices = []
    for i in range(max_devices):
        if system == "Windows":
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(i)
        if not cap or not cap.isOpened():
            if cap:
                cap.release()
            continue
        ret, _ = cap.read()
        cap.release()
        if ret:
            devices.append(i)
    return devices


def get_model_path():
    model_dir = Path(__file__).resolve().parent / 'models'
    model_dir.mkdir(exist_ok=True)
    return model_dir / MODEL_NAME


def download_model(model_path: Path):
    print(f"Descargando modelo de MediaPipe: {MODEL_URL}")
    urllib.request.urlretrieve(MODEL_URL, model_path)
    print(f"Modelo guardado en: {model_path}")


def ensure_model():
    model_path = get_model_path()
    if not model_path.exists():
        try:
            download_model(model_path)
        except Exception as exc:
            raise RuntimeError(
                f"No se pudo descargar el modelo. Coloca '{MODEL_NAME}' en '{model_path.parent}' o verifica tu conexión.\nError: {exc}"
            )
    return model_path


def ensure_csv_header(path):
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            header = ['label', 'timestamp', 'frame']
            for hand_no in range(1, 3):
                for i in range(21):
                    header += [f'hand{hand_no}_x{i}', f'hand{hand_no}_y{i}']
            header += ['face_cx', 'face_cy', 'face_w', 'face_h']
            writer.writerow(header)


def flatten_hand(landmarks):
    coords = []
    for lm in landmarks:
        coords.append(float(lm.x))
        coords.append(float(lm.y))
    return coords


def compute_face_bbox(landmarks):
    if not landmarks:
        return [0.0, 0.0, 0.0, 0.0]
    xs = [float(lm.x) for lm in landmarks]
    ys = [float(lm.y) for lm in landmarks]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    return [cx, cy, xmax - xmin, ymax - ymin]


def create_holistic_landmarker(model_path):
    options = HolisticLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model_path)),
        running_mode=VisionTaskRunningMode.VIDEO,
        min_face_detection_confidence=0.5,
        min_face_landmarks_confidence=0.5,
        min_pose_detection_confidence=0.5,
        min_pose_landmarks_confidence=0.5,
        min_hand_landmarks_confidence=0.5,
    )
    return HolisticLandmarker.create_from_options(options)


def draw_results(image, result):
    if result.left_hand_landmarks:
        mp_vision.drawing_utils.draw_landmarks(
            image,
            result.left_hand_landmarks,
            mp_vision.HandLandmarksConnections.HAND_CONNECTIONS,
        )
    if result.right_hand_landmarks:
        mp_vision.drawing_utils.draw_landmarks(
            image,
            result.right_hand_landmarks,
            mp_vision.HandLandmarksConnections.HAND_CONNECTIONS,
        )
    if result.face_landmarks:
        mp_vision.drawing_utils.draw_landmarks(
            image,
            result.face_landmarks,
            mp_vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
        )


def detect_landmarks(frame, landmarker, timestamp_ms):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image(ImageFormat.SRGB, rgb)
    return landmarker.detect_for_video(image, timestamp_ms)


def open_camera(index):
    backend = cv2.CAP_DSHOW if platform.system() == "Windows" else 0
    cap = cv2.VideoCapture(index, backend) if backend != 0 else cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"No se pudo abrir la cámara {index}")
        return

    model_path = ensure_model()
    landmarker = create_holistic_landmarker(model_path)

    detection_on = True
    recording = False
    csv_path = os.path.join(os.getcwd(), 'landmarks.csv')
    frame_idx = 0
    current_label = ''

    print("Controles: 'q' salir, 's' guardar imagen, 'd' alternar overlay, 'r' iniciar/detener grabación")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error leyendo frame")
            break

        timestamp_ms = int(time.time() * 1000)
        result = detect_landmarks(frame, landmarker, timestamp_ms)

        if detection_on:
            draw_results(frame, result)
            cv2.putText(frame, "Deteccion: ON", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Deteccion: OFF", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if recording:
            left_hand = result.left_hand_landmarks or []
            right_hand = result.right_hand_landmarks or []
            face_box = compute_face_bbox(result.face_landmarks or [])
            timestamp = datetime.utcnow().isoformat()
            row = [current_label, timestamp, frame_idx]
            row += flatten_hand(left_hand) + flatten_hand(right_hand)
            row += face_box
            with open(csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            cv2.putText(frame, f"REC: {current_label}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            frame_idx += 1

        cv2.imshow(f"Cámara {index}", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            fname = f"snapshot_cam_{index}.png"
            cv2.imwrite(fname, frame)
            print(f"Guardada imagen: {fname}")
        if key == ord('d'):
            detection_on = not detection_on
        if key == ord('r'):
            recording = not recording
            if recording:
                current_label = input('Etiqueta para esta grabación (ej: letra_o_palabra): ')
                ensure_csv_header(csv_path)
                print(f"Grabando con etiqueta: {current_label}")
            else:
                print(f"Detenido grabación. Archivo: {csv_path}")

    landmarker.close()
    cap.release()
    cv2.destroyAllWindows()


def main():
    print("Buscando dispositivos de cámara...")
    devices = list_cameras(10)
    if not devices:
        print("No se encontraron cámaras.")
        return
    print("Cámaras encontradas:")
    for d in devices:
        print(f"  [{d}] Cámara {d}")
    while True:
        choice = input("Selecciona el número de dispositivo (o 'q' para salir): ")
        if choice.lower() == 'q':
            print("Saliendo.")
            return
        try:
            idx = int(choice)
        except ValueError:
            print("Entrada no válida. Intenta de nuevo.")
            continue
        if idx in devices:
            print(f"Abriendo cámara {idx}...")
            open_camera(idx)
            return
        else:
            print("Índice no listado. Elige uno de la lista.")


if __name__ == '__main__':
    main()
