import sys
import serial
from serial import Serial
import numpy as np
import Rotinas
import struct
import time
import os

'''
#SYN$ ->  vai iniciar conexão
#ACK  -> PIC recebeu informação
'''


def lerPixel(roberts, i, j, ser):
    flag = True
    while(flag):
        p = ser.read(1)
        if(p !=b''):
            roberts[i,j] = ord(p)            
            flag = False
    return roberts

def work(array, largura, altura, ser):
    roberts = np.zeros(shape = (int(altura),int(largura)), dtype=np.int8)
    pixelsRecebidos = 0
    totalPixels = largura * altura
    inicio = time.time()
    for i in range(altura):
        for j in range(largura):
            pixelsRecebidos += 1
            print(chr(27) + "[2J")
            print('\n\n\nProgresso: {} %'.format(round((pixelsRecebidos * 100/totalPixels), 2)))
            if i == 0 or j == 0:
                if j == largura-1:
                    ser.write(struct.pack('>B',array[i][j-1]))    
                    ser.write(struct.pack('>B', array[i][j]))
                    ser.write(struct.pack('>B',array[i+1][j-1])) 
                    ser.write(struct.pack('>B', array[i+1][j]))
                    roberts = lerPixel(roberts, i, j, ser)
                    continue
                if i == altura-1:
                    ser.write(struct.pack('>B',array[i-1][j]))   
                    ser.write(struct.pack('>B',array[i-1][j+1]))
                    ser.write(struct.pack('>B', array[i][j])) 
                    ser.write(struct.pack('>B', array[i][j+1]))
                    roberts = lerPixel(roberts, i, j, ser)
                    continue
                ser.write(struct.pack('>B',array[i][j]))
                ser.write(struct.pack('>B',array[i][j+1]))
                ser.write(struct.pack('>B',array[i+1][j]))
                ser.write(struct.pack('>B',array[i+1][j+1]))
                roberts= lerPixel(roberts, i, j, ser)
            else:
                ser.write(struct.pack('>B',array[i-1][j-1]))   
                ser.write(struct.pack('>B', array[i-1][j]))
                ser.write(struct.pack('>B', array[i][j-1])) 
                ser.write(struct.pack('>B', array[i][j]))
                roberts = lerPixel(roberts, i, j, ser)

            
    fim = time.time()       
    roberts = roberts.reshape((largura,altura))
    print("Tempo de conclusão {} segundos ".format(round((fim - inicio), 2)))
    return roberts

def processar(nome):
    ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200, timeout = 2)
    ser.write(b'SYN$')
    print("syn enviado")
    while(ser.read(3) != b'ACK'):
        pass
    print("Conexão iniciada com o PIC")
    
    if Rotinas.validarImagem(nome):#Verifica se imagem é válida
        largura, altura = Rotinas.getResolucao(nome)
        res = str(largura) + 'x' + str(altura) + '$'
        ser.write(res.encode()) #envia resolução pro PIC

        while ser.read(3) != b'ACK': #esperando confirmação de recebimento da resolução
            pass
        print('PIC recebeu resolução.')
        array = Rotinas.getPixels(nome, largura, altura)
        roberts = work(array, int(largura), int(altura), ser)
        return roberts
