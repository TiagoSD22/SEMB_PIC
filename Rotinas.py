import numpy as np

#Salva imagem no formato .pgm P5
def setImagem(array, nome):
    newImage = open(str(nome),"w")
    newImage.write("P5\n")
    newImage.write(str(np.size(array,0)) + ' ' + str(np.size(array,1)) + '\n')
    newImage.write('255\n')
    array.tofile(newImage)
    newImage.close()
    print("Imagem gerada com sucesso!")

#Retorna largura e altura da imagem
def getResolucao(nome):
    with open(nome, 'rb') as imagem:
        imagem.readline()
        largura, altura = imagem.readline().decode('utf-8').split(' ')
        altura = altura.replace('\n', '')
        return largura,altura

#Retorna um array bidimencional contendo pixels da imagem
def getPixels(nome, largura, altura):
    with open(nome, 'rb') as imagem:
        for i in range(3):
            print(imagem.readline().decode('utf-8'))
                  
        array = np.fromfile(imagem, dtype=np.uint8)
        array.shape = (int(altura),int(largura))
        return array
    
#Verifica os parâmetros do cabeçalho que definem uma imagem .pgm P5 padrão
def validarImagem(nome):
    with open(nome, 'rb') as imagem:
        try:
            if imagem.readline() != 'P5\n'.encode('utf-8'):
                print('A imagem deve estar no formato .pgm P5!')
                return False
            else:
                imagem.readline()
                intensidade = int(imagem.readline().decode('utf-8'))
                if intensidade > 255:
                    print('A imagem deve ser 8 bits!')
                    return False
                else:
                    return True
        except:
            raise ValueError("ERRO NA LEITURA DO ARQUIVO")


