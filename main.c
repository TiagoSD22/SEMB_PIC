/*
 *  Sobre este código:
 *  O arquivo main.c configura os registradores e bits de configuração do pic 16f18875 e aqui encontra-se a rotina 
 *  principal da aplicação. O MCU fica a espera de um comando enviado pela porta serial, e executa o algorito de
 *  Roberts Cross para detecção de bordas na imagem armazenada no arquivo image.h. Os valores dos novos pixels são
 *  enviados para a interface serial onde podem ser lidos por um pc através de um adaptador usb/serial(ttl).

 *  Autores : Tiago Dionizio e Lucas Magalhães

 *  Copyright (C) 2018 Tiago Siqueira Dionizio  <tiagosdionizio@gmail.com>

 *  Copyright (C) 2018 Lucas Magalhães de Sousa <lucasmag97@gmail.com> 

 *  Data de Atualização : 20 de Novembro de 2018

 *  Modo de uso:
 *  A aplicação é controlada por comandos enviados para a entrada serial EUSART (RX - RC7, TX - RC6) do MCU, essas 
 *  entradas podem ser enviadas por um script em python usando o módulo pySerial, por meio desse script é possível
 *  ordenar a execução do algoritmo de Roberts e gerar a imagem resultante com os pixels calculados e enviados pelo
 *  MCU. 

 *  Restrição de uso:
 *  Necessita-se de um interpretador python ( >= 2.7) instalado na máquina que se comunicará com a aplicação,
 *  bem como o módulo pySerial. Além disso, é necessário um adaptador usb/serial(ttl), como o pl2303, de modo que 
 *  que possa haver um canal de comunicação entre o computador e a aplicação embarcada. A imagem gerada é em formato
 *  .pgm binário (P5).

 *  Referência para o algoritmo: 
 *  MARQUES FILHO, Ogê; VIEIRA NETO, Hugo. Processamento Digital de Imagens, Rio de Janeiro: Brasport, 1999, pg: 97.
*/


// Production -> Set Configuration Bits;
// PIC16F18875 Configuration Bit Settings
// 'C' source line config statements

// CONFIG1
#pragma config FEXTOSC  = OFF       // External Oscillator mode selection bits (Oscillator not enabled)
#pragma config RSTOSC   = HFINT32   // Power-up default value for COSC bits (HFINTOSC with OSCFRQ= 32 MHz and CDIV = 1:1)
#pragma config CLKOUTEN = OFF       // Clock Out Enable bit (CLKOUT function is disabled; i/o or oscillator function on OSC2)
#pragma config CSWEN    = ON        // Clock Switch Enable bit (Writing to NOSC and NDIV is allowed)
#pragma config FCMEN    = ON        // Fail-Safe Clock Monitor Enable bit (FSCM timer enabled)

// CONFIG2
#pragma config MCLRE    = ON        // Master Clear Enable bit (MCLR pin is Master Clear function)
#pragma config PWRTE    = OFF       // Power-up Timer Enable bit (PWRT disabled)
#pragma config LPBOREN  = OFF       // Low-Power BOR enable bit (ULPBOR disabled)
#pragma config BOREN    = ON        // Brown-out reset enable bits (Brown-out Reset Enabled, SBOREN bit is ignored)
#pragma config BORV     = LO        // Brown-out Reset Voltage Selection (Brown-out Reset Voltage (VBOR) set to 1.9V on LF, and 2.45V on F Devices)
#pragma config ZCD      = OFF       // Zero-cross detect disable (Zero-cross detect circuit is disabled at POR.)
#pragma config PPS1WAY  = ON        // Peripheral Pin Select one-way control (The PPSLOCK bit can be cleared and set only once in software)
#pragma config STVREN   = ON        // Stack Overflow/Underflow Reset Enable bit (Stack Overflow or Underflow will cause a reset)

// CONFIG3
#pragma config WDTCPS   = WDTCPS_31 // WDT Period Select bits (Divider ratio 1:65536; software control of WDTPS)
#pragma config WDTE     = OFF       // WDT operating mode (WDT Disabled, SWDTEN is ignored)
#pragma config WDTCWS   = WDTCWS_7  // WDT Window Select bits (window always open (100%); software control; keyed access not required)
#pragma config WDTCCS   = SC        // WDT input clock selector (Software Control)

// CONFIG4
#pragma config WRT      = OFF       // UserNVM self-write protection bits (Write protection off)
#pragma config SCANE    = available // Scanner Enable bit (Scanner module is available for use)
#pragma config LVP      = ON        // Low Voltage Programming Enable bit (Low Voltage programming enabled. MCLR/Vpp pin function is MCLR.)

// CONFIG5
#pragma config CP       = OFF       // UserNVM Program memory code protection bit (Program Memory code protection disabled)
#pragma config CPD      = OFF       // DataNVM code protection bit (Data EEPROM code protection disabled)

#include <xc.h>
#include <string.h>
#include "image.h"
#include "uart.h"

/*
 * LEDs para indicar,respectivamente, que está havendo comunicação de dados entre o MCU e o computador e
 * que o filtro de Roberts está sendo processado pelo MCU.
 */
#define comunicacaoLED  LATAbits.LATA7
#define robertsLED      LATAbits.LATA6

/*
 *  Esta função configura alguns registradores do MCU pic16f18875, os pinos dos bloco A e B configurados como saída,
 *  enquanto o bloco C tem o pino RC7 como entrada e os demais como saída.
 */
void ConfigurarPIC(void){
    TRISA = 0x00;
    TRISB = 0x00;
    TRISC = 0x80;
}

/*
 * Esta função é chamada quando o comando GET é recebido na interface serial EUSART e envia os pixels referentes 
 * à imagem de teste armazenada no arquivo image.h, serve para checar se a imagem foi armazenada corretamente.
 */
void EnviarImagem(void){
    short i,j;
    comunicacaoLED = 1;
    for(i = 1; i < imgALTURA - 1; i++){
        for(j = 1; j < imgLARGURA - 1; j++){
            UART_Escrever_Pixel(pixels[i][j]);
        }
    }
    comunicacaoLED = 0;
}

/*
 * Esta função é chamada quando o comando ROB é recebido na interface serial EUSART e serve para aplicar o 
 * algoritmo de Roberts Cross para todos os pixels da imagem. Foi necessário adaptar o algoritmo, pois a imagem
 * foi armazenada como const, pois, ao contrário, não seria possível armazenar os 3010 pixels referentes a esta.
 * Assim sendo, para cada novo pixel calculado, este valor é imediatamente enviado para a interface serial, para que
 * o computador, rodando o script em python possa receber esses valores e gerar a imagem resultante(bordas). 
 * O laço que percorre a imagem inicia da primeira linha e primeira coluna e vai até a penúltima linha e penúltima 
 * coluna, pois a imagem armazenada no arquivo image.h é o resultado da imagem original adicionada de um padding, uma
 * borda feita apenas de pixels com intensidade 0 (preto) colocados ao redor de toda a imagem, 
 * adicionando, assim, duas linhas e duas colunas a mais, que devem ser ignoradas do conjunto de pixels a se aplicar
 * o filtro de Roberts.
 */
void RobertsCrossSerial(void){
    //robertsLED = 1;
    short i,j;
    unsigned char novo_pixel;
    for(i = 1; i < imgALTURA - 1; i++){
        for(j = 1; j < imgLARGURA - 1; j++){
            novo_pixel = RobertsCross(i,j);
            //comunicacaoLED = 1;
            //UART_Escrever_Pixel(novo_pixel);
            //comunicacaoLED = 0;
        }
    }
    //robertsLED = 0;
}

/*
 * A rotina principal configura os pinos de I/O e os registradores EUSART do MCU, acende o LED conectado ao pino
 * RA7 para indicar funcionamento da rotina e, em seguida, coloca o MCU em modo de espera de um comando na interface
 * serial EUSART. Caso o comando recebido seja GET, os pixels da imagem no arquivo image.h são enviados serialmente
 * para o computador. Caso o comando o seja ROB, o MCU executa o filtro de Roberts Cross.
 */
int main(void) {
    //char entrada[4];
    
    ConfigurarPIC();
    //UART_iniciar();  
    LATA = 0x10;
    
    while (1) {
        /*UART_Ler_Texto(entrada);
        if(strcmp(entrada,"GET") == 0){
            EnviarImagem();
        }
        else if(strcmp(entrada,"ROB") == 0){
            RobertsCrossSerial();
        }*/
        LATBbits.LATB0 = 1;
        RobertsCrossSerial();
        LATBbits.LATB0 = 0;
        RobertsCrossSerial();
    }
    
    return EXIT_SUCCESS;
}
