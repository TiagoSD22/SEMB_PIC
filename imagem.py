import sys
import serial
from serial import Serial
import numpy as np
from rotinas import imagem
import struct
import time

'''
#SYN$ ->  vai iniciar conexão
#ACK  -> PIC recebeu informação
'''

def lerPixel(roberts, i, j, pixelsRecebidos, totalPixels,ser):
    flag = True
    while(flag):
        p = ser.read(1)
        if(p !=b''):
            roberts[i,j] = ord(p)
            pixelsRecebidos += 1
            print(chr(27) + "[2J")
            print("Progresso: ",pixelsRecebidos * 100/totalPixels,'%')
            flag = False
    return roberts
            
def envia4(array, largura, altura,ser):
    roberts = np.zeros(shape = (int(altura),int(largura)), dtype=np.int8)
    totalPixels = largura * altura
    pixelsRecebidos = 0
    inicio = time.time()
    for i in range(altura):
        for j in range(largura):
            if i == 0 or j == 0:
                if j == largura-1:
                    ser.write(struct.pack('>B',array[i][j-1]))    
                    ser.write(struct.pack('>B', array[i][j]))
                    ser.write(struct.pack('>B',array[i+1][j-1])) 
                    ser.write(struct.pack('>B', array[i+1][j]))
                    roberts = lerPixel(roberts, i, j, pixelsRecebidos, totalPixels, ser)
                    continue
                if i == altura-1:
                    ser.write(struct.pack('>B',array[i-1][j]))   
                    ser.write(struct.pack('>B',array[i-1][j+1]))
                    ser.write(struct.pack('>B', array[i][j])) 
                    ser.write(struct.pack('>B', array[i][j+1]))
                    roberts = lerPixel(roberts, i, j, pixelsRecebidos, totalPixels, ser)
                    continue
                ser.write(struct.pack('>B',array[i][j]))
                ser.write(struct.pack('>B',array[i][j+1]))
                ser.write(struct.pack('>B',array[i+1][j]))
                ser.write(struct.pack('>B',array[i+1][j+1]))
                roberts = lerPixel(roberts, i, j, pixelsRecebidos, totalPixels, ser)
            else:
                ser.write(struct.pack('>B',array[i-1][j-1]))   
                ser.write(struct.pack('>B', array[i-1][j]))
                ser.write(struct.pack('>B', array[i][j-1])) 
                ser.write(struct.pack('>B', array[i][j]))
                roberts = lerPixel(roberts, i, j, pixelsRecebidos, totalPixels, ser)
                
    fim = time.time()       
    roberts = roberts.reshape((largura,altura))
    print("Tempo de conclusão(s): ",fim - inicio)
    return roberts

def processar(nome):
    ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200, timeout = 2)
    ser.write(b'SYN$')
    print("syn enviado")
    while(ser.read(3) != b'ACK'):
        pass
    print("Conexão iniciada com o PIC")
    

    if imagem.validarImagem(nome):#Verifica se imagem é válida
        largura, altura = imagem.getResolucao(nome)
        res = str(largura) + 'x' + str(altura) + '$'
        ser.write(res.encode()) #envia resolução pro PIC

        while ser.read(3) != b'ACK': #esperando confirmação de recebimento da resolução
            pass
        print('PIC recebeu resolução.')
        
        array = imagem.getPixels(nome, largura, altura)
        return envia4(array, int(largura), int(altura),ser)
        
if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        processar(input('Digite o nome do arquivo .pgm: '))
        
    elif len(sys.argv) == 2:
        imagem.setImagem(processar(sys.argv[1]), 'saida_Roberts.pgm')

    elif len(sys.argv) == 3:
        imagem.setImagem(processar(sys.argv[1]), sys.argv[2])

