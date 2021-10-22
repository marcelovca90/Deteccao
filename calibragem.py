import cv2
import math
import numpy as np
import os
import pandas as pd
import subprocess
import sys
import time
from gaze_tracking import GazeTracking
import seaborn as sns
sns.set_theme()
import plotly.express as px
import plotly.graph_objects as go
import tkinter as tk
from tkinter import filedialog as fd

# create the root window
root = tk.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
root.withdraw()

print(f'Initializing calibration.')
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

start_delay = 3 # seconds
duration = 12000 # milliseconds
print(f'Calibration will start in {start_delay} seconds.')
time.sleep(start_delay)

coords = []
time_results = []
res = 0
contador = 0
temp_ini = time.time()  # tempo que começa o programa
contadorRight = 0
contadorLeft = 0
menor_x = 5000
maior_x = -5000
lista_tempo = []
lista_gaze_x = []
lista_gaze_y = []

start_time = time.time()
print('Main loop started.')

def calibragem():    
    while True:

        current_time = time.time()
        elapsed_time = current_time - start_time

        ini = time.time()  # inicia tempo dentro do while
        res = ini - temp_ini  # diferença do tempo inicial e o tempo dentro do while
        time_results.append(res)  # colocar res no vetor
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
            contadorRight += 1
        elif gaze.is_left():
            text = "Looking left"
            contadorLeft += 1
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        gaze_x = gaze.horizontal_ratio()
        gaze_y = gaze.vertical_ratio()

        if res >= 0.1:
            contador = contador + 100
            if gaze_x != None and gaze_y != None:

                # +-------------+
                # |             |
                # |             |
                # |             |
                # +-------------+

                if contador < 3000:
                    cv2.putText(frame, "*", (0, SCREEN_HEIGHT/2), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) # esq
                elif contador < 6000:
                    cv2.putText(frame, "*", (SCREEN_WIDTH/2, 0), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) # cima
                elif contador < 9000:
                    cv2.putText(frame, "*", (SCREEN_WIDTH, SCREEN_HEIGHT/2), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) # dir
                else
                    cv2.putText(frame, "*", (SCREEN_WIDTH/2, SCREEN_HEIGHT), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1) # baixo

                lista_gaze_x.append(gaze_x)
                lista_gaze_y.append(gaze_y)

                print(f'x = {gaze_x:.3f} (min = {menor_x:.3f}, max = {maior_x:.3f})\ty = {gaze_y:.3f}')
                coords.append([pd.Timedelta(milliseconds=contador), gaze_x, gaze_y])

            if elapsed_time > duration:
                print(f'Main loop finished after {str(int(elapsed_time))} seconds.')
                break

    # ordenar os x de forma crescente
    # x_min = media dos 10 primeiros gaze_x
    # x_max = media dos 10 ultimos gaze_x

    # ordenar os y de forma crescente
    # y_min = media dos 10 primeiros gaze_y
    # y_max = media dos 10 ultimos gaze_y

    return [x_min, x_max, y_min, y_max]

 # apenas para testes
if __name__ == '__main__':
    calibragem()
