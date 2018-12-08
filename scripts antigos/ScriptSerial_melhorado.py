import serial
from serial import Serial
import array
import struct

def recebe_pixels():
    nPixels = 0
    pixel = ser.read(1)
    pixels = array.array('B')
    totalPixelsEsperado = 3010
    print("Recebendo pixels")
    
    while nPixels < totalPixelsEsperado:
        pixel = ser.read(1)
        if(pixel != b''):
            nPixels += 1
            pixels.append(ord(pixel))
    print("Transferência concluída!")
    return pixels


if __name__ == "__main__":
    ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 115200, timeout = 2)
    '''
    ser.write(b'ROB$')

    pixels = recebe_pixels()
    imageFile = open("RobertPIC.PGM","w")
    imageFile.write("P5\n70 43\n255\n")
    
    imageFile = open("RobertPIC.PGM","ab")
    pixels.tofile(imageFile)
    print("Imagem .pgm P5 gerada com sucesso!")
    imageFile.close()
    '''
    
    ser.write(b'SYN$')
    '''
    while(True):
        resp = ser.read(3)
        if(resp != b''):
            print(resp)
    '''
    while(ser.read(3) != b'ACK'):
        pass
    print("conexao iniciada")
    res = '12x7$'
    ser.write(res.encode())
    while(ser.read(3) != b'ACK'):
        pass
    flag = True
    while(flag):
        l = ser.read(1)
        if(l != b''):
            print("largura: ", ord(l))
            flag = False
    flag = True
    while(flag):
        a = ser.read(1)
        if(a != b''):
            print("altura: ", ord(a))
            flag = False
    print("resolucao recebida pelo pic")
    ser.write(struct.pack('>B', 70))
    while(True):
        pixel = ser.read(1)
        if(pixel != b''):
            print(ord(pixel))
    
    
