import os
import re
import sys
import subprocess
import Rotinas
import Imagem
from ctypes import cdll

def scanUSB():
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i.decode())
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    return devices

def conectar():
    devices = scanUSB()
    for i in devices:
        if i.get('id') == '067b:2303':
            conectado = True
            break
        else:
            conectado = False
    
    if conectado:
        print('\nAdaptador Serial/USB conectado.\n\n')
        
    else:
        print("\nAdaptador Serial/USB não conectado!\n\n")
        print(input('\n\n\n\n\nPressione ENTER para continuar...'))
        return 0
    
    output = subprocess.check_output("dmesg | grep 'pl2303 converter now attached to'; exit 0", stderr=subprocess.STDOUT, shell=True)
    with open('temp.txt', 'wb') as doc:
        doc.write(output)
        
    with open('temp.txt', 'r') as doc:
        for line in doc:
            for part in line.split():
                porta = 'ttyUSB0' if part == 'ttyUSB0' else 'ttyUSB1'
    os.remove('temp.txt')
    try:
        os.chmod('/dev/'+porta, 0o777)
        print('Porta {} habilitada! Conecte a plataforma ao adaptador...')
    except PermissionError:
        print('\nVocê não tem permissões para habilitar porta USB <{}>!\n'.format(porta))
        print('Reinicie o script como superusuário...')

    print(input('\n\n\n\n\nPressione ENTER para continuar...'))
    
    
def roberts():
    print('Atenção: Certifique-se de que a plataforma esteja devidamente conectada ao computador')
    arquivo = input('\nDigite o nome do arquivo .pgm: ')
    #try:
    entrada = Imagem.processar(arquivo)
    #except:
    #print('\nErro na conexão com a plataforma!')
    #print(input('\n\n\n\n\nPressione ENTER para continuar...'))
    #return 0
    saida = input('\n\nDigite o nome que você deseja salvar o arquivo: ')
    Rotinas.setImagem(entrada, saida)
    print(input('\n\n\n\n\nPressione ENTER para continuar...'))
    
def compara():
    libComp = cdll.LoadLibrary("./libCompara.so")
    libComp.Comparar_Imagens()
    print(input('\n\n\n\n\nPressione ENTER para continuar...'))
    
def cabecalho():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('------------------------------------------------')
    print('       ROBERTS CROSS - DETECÇÃO DE BORDAS')
    print('------------------------------------------------')
def menu():

    print('         Digite uma opção e tecle ENTER:')
    print('------------------------------------------------')
    print('')
    print('  a - Habilitar conexão serial')
    print('  b - Aplicar filtro de Roberts Cross')
    print('  c - Comparar imagens')
    print('  d - Sair')
    print('')
    print('')

if __name__ == '__main__':
    fica = True;
    while(fica):
        cabecalho()
        menu()
        opcao = input('>>> ')
        if opcao == 'a':
            cabecalho()
            conectar()
            
        elif opcao == 'b':
            cabecalho()
            roberts()
            
        elif opcao == 'c':
            cabecalho()
            compara()

        elif opcao == 'd':
            os.system('cls' if os.name == 'nt' else 'clear')
            fica = False;
        
