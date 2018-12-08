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
def envia4(array, largura, altura,ser):
    roberts = np.zeros(shape = (int(altura),int(largura)), dtype=np.int8, order = 'F')
    totalPixels = largura * altura
    pixelsRecebidos = 0
    inicio = time.time()
    for i in range(altura):
        for j in range(largura):
            '''
            if(i != altura-1 and j != largura-1):
                ser.write(struct.pack('>B',array[i,j]))
                ser.write(struct.pack('>B',array[i+1,j]))
                ser.write(struct.pack('>B',array[i,j+1]))
                ser.write(struct.pack('>B',array[i+1,j+1]))
            else:
                if(i != altura-1):
                    ser.write(struct.pack('>B',array[i,j]))   
                    ser.write(struct.pack('>B',0))
                    ser.write(struct.pack('>B',array[i+1,j])) 
                    ser.write(struct.pack('>B',0))
                else:
                    if(j != largura-1):
                        ser.write(struct.pack('>B',array[i,j]))   
                        ser.write(struct.pack('>B',array[i,j+1])) 
                        ser.write(struct.pack('>B',0))
                        ser.write(struct.pack('>B',0))
                    else:
                        ser.write(struct.pack('>B',array[i,j]))    
                        ser.write(struct.pack('>B',0))
                        ser.write(struct.pack('>B',0)) 
                        ser.write(struct.pack('>B',0))
                        if(i > 1 && j > 1){
                Gx += pixels[i - 1 + x][j - 1 + y] * robertX[x][y];
                Gy += pixels[i - 1 + x][j - 1 + y] * robertY[x][y];
            }
            else{
                Gx += pixels[i + x][j + y] * robertX[x][y];
                Gy += pixels[i + x][j + y] * robertY[x][y];
            }
            '''
            if(i > 0 and j > 0):
                if(i != altura-1 and j != largura-1):
                    ser.write(struct.pack('>B',array[i,j-1]))
                    ser.write(struct.pack('>B',array[i,j]))
                    ser.write(struct.pack('>B',array[i+1,j-1]))
                    ser.write(struct.pack('>B',array[i+1,j]))
                else:
                    if(i != altura-1):
                        ser.write(struct.pack('>B',array[i,j-1]))   
                        ser.write(struct.pack('>B',array[i,j]))
                        ser.write(struct.pack('>B',array[i+1,j-1])) 
                        ser.write(struct.pack('>B',array[i+1,j]))
                    else:
                        if(j != largura-1):
                            ser.write(struct.pack('>B',array[i,j-1]))   
                            ser.write(struct.pack('>B',array[i,j])) 
                            ser.write(struct.pack('>B',0))
                            ser.write(struct.pack('>B',0))
                        else:
                            ser.write(struct.pack('>B',array[i,j-1]))    
                            ser.write(struct.pack('>B',array[i,j]))
                            ser.write(struct.pack('>B',0)) 
                            ser.write(struct.pack('>B',0))
            else:
                if(i != altura-1):
                    ser.write(struct.pack('>B',array[i,j-1]))   
                    ser.write(struct.pack('>B',array[i,j]))
                    ser.write(struct.pack('>B',array[i+1,j-1])) 
                    ser.write(struct.pack('>B',array[i+1,j]))
                else:
                    if(j != largura-1):
                        ser.write(struct.pack('>B',array[i,j-1]))   
                        ser.write(struct.pack('>B',array[i,j])) 
                        ser.write(struct.pack('>B',0))
                        ser.write(struct.pack('>B',0))
                    else:
                        ser.write(struct.pack('>B',array[i,j-1]))    
                        ser.write(struct.pack('>B',array[i,j]))
                        ser.write(struct.pack('>B',0)) 
                        ser.write(struct.pack('>B',0))
            flag = True
            while(flag):
                p = ser.read(1)
                if(p != b''):
                    roberts[i,j] = ord(p)
                    pixelsRecebidos += 1
                    print(chr(27) + "[2J")
                    print("Progresso: ",pixelsRecebidos * 100/totalPixels,'%')
                    flag = False
    fim = time.time()       
    roberts = roberts.reshape((largura,altura))
    print("Tempo de conclusão(s): ",fim - inicio)
    return roberts
'''
def enviar_imagem(array, largura, altura):
    roberts = np.empty((largura,altura), dtype=np.int8)
    for i in range(altura):
        if i == 1:
            continue
        for j in range(largura):
            if i > 1:
                ser.write(struct.pack('>B',str(array[i][j]))
                if j > 0:
                    roberts[i-1][j] = ord(ser.read(1))            
            else:
                ser.write(struct.pack('>B',str(array[i][j]))
                ser.write(struct.pack('>B',str(array[i+1][j]))
                if j > 0:
                    roberts[i][j-1] = ord(ser.read(1))
        roberts[i][largura-1] = ord(ser.read(1))
    return roberts
'''
def processar(nome):
    ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200, timeout = 0)
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

