'''
 *  Este script é responsável pela recepção dos bytes da imagem gerados pela MCU, logo após a aplicação do filtro. 
 *  A medida em que os bytes são recebidos, eles são guardados em um array. Quando a imagem estiver completa, o script gera
 *  um arquivo .PGM P5, contendo a imagem já pronta para teste.
 *  Autores : Tiago Dionizio e Lucas Magalhães
 *  Copyright (C) 2018 Tiago Siqueira Dionizio  <tiagosdionizio@gmail.com>
 *  Copyright (C) 2018 Lucas Magalhães de Sousa <lucasmag97@gmail.com> 
 *  Data de Atualização : 21 de Novembro de 2018
'''

import serial
from serial import Serial
import array
import time

'''
 * Esta função define que a recepção será feita byte a byte, define o número total de pixels a serem recebidos e inicia a espera
 * dos bytes. Quando todos os bytes forem recebidos é retornado um bytearray contendo a imagem.
'''
def recebe_pixels():
    nPixels = 0
    pixel = ser.read(1)
    pixels = array.array('B')
    totalPixelsEsperado = 3010
    print("Recebendo pixels")
    inicio = time.time()
    while nPixels < totalPixelsEsperado:
        pixel = ser.read(1)
        if(pixel != b''):
            nPixels += 1
            pixels.append(ord(pixel))
    fim = time.time()  
    print("Transferência concluída!")
    print("Tempo de conclusão(s): ",fim - inicio)
    return pixels
'''
 * Quando o script é executado são definidas a porta de recepção e a taxa de transmissão. O comando ROB é enviado à MCU, para que se inicie
 * a execução do filtro e logo em seguida é iniciada a espera dos pixels convertidos. Depois a função cria um arquivo .PGM, escreve o 
 * cabeçalho e os bytes do bytearray, e por fim gera como saída a imagem .PGM com o filtro já aplicado.
'''
if __name__ == "__main__":
    ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200, timeout = 0)
    ser.write(b'ROB$')

    pixels = recebe_pixels()
    imageFile = open("RobertPIC.PGM","w")
    imageFile.write("P5\n70 43\n255\n")
    
    imageFile = open("RobertPIC.PGM","ab")
    pixels.tofile(imageFile)
    print("Imagem .pgm P5 gerada com sucesso!")
imageFile.close()
