/*
 *  Esta biblioteca pode ser usada para configurar a interface EUSART do MCU pic16f18875 e implementar rotinas de
 *  leitura e escrita de dados serialmente.

 *  Autores : Tiago Dionizio e Lucas Magalhães

 *  Copyright (C) 2018 Tiago Siqueira Dionizio  <tiagosdionizio@gmail.com>

 *  Copyright (C) 2018 Lucas Magalhães de Sousa <lucasmag97@gmail.com> 

 *  Data de Atualização : 20 de Novembro de 2018
*/

#ifndef UART_H
#define	UART_H

/*
 * Esta função configura os registradores para usar a interface EUSART do MCU, configurando os pinos 
 * RC6 como TX e RC7 como RX. O baudrate é fixo de 9600bps.
 */
void UART_iniciar(){
    ANSELCbits.ANSC7 = 0;   //Desativa função analógica no pino RC7
    ANSELCbits.ANSC6 = 0;   //Desativa função analógica no pino RC6
    RC6PPS = 0x10;          //Configura pino RC6 como TX
    RXPPSbits.RXPPS = 0x17; //Configura pino RC7 como RX
    TX1STAbits.BRGH = 1;    //Necessário para configurar o baud rate da EUSART
    BAUDCON1bits.BRG16 = 0; //Configura registrado BAUDCON1 como 8 bits
    SPBRG = 16;              //Configura baud rate para 115200bps
    RC1STAbits.SPEN = 1;    //Habilita EUSART
    RC1STAbits.CREN = 1;    //Habilita recebimento EUSART (RX)
    TX1STAbits.TXEN = 1;    //Habilita transmissão EUSART (TX)
    TX1STAbits.SYNC = 0;    //Configura EUSART para modo assíncrono
}

//Esta função serve para ler um simples byte na pino RC7 (RX).
char UART_Ler(){
    while(!RCIF);
    return RCREG;
}

void UART_Ler_Pixel(unsigned char* p){
    while(!RCIF);
    *p = (unsigned char)RCREG;
}

/*
 * Esta função pode ler um conjunto de caracteres enviados serialmente para o pino RC7, serve para ler os comandos
 * enviados pelo computador através do script em python. A regra é que cada comando contenha um caractere '$' 
 * ao final, representando que o comando acabou.
 */
void UART_Ler_Texto(char* saida){
    short index = 0;
    char c;
    while(c != '$'){
       c = UART_Ler(); 
       saida[index] = c;
       index++;
    }
    saida[index - 1] = '\0';
}

//Esta função serve para escrever um byte no pino RC6 (TX) do MCU.
void UART_Escrever(char c){
    while(!TX1STAbits.TRMT);
    TXREG = c;
}

/*
 * Esta função serve para enviar os pixels da imagem armazenada no arquivo image.h,
 * bem como os novos valores de pixels calculados no filtro de Roberts Cross.
 */
void UART_Escrever_Pixel(unsigned char p){
    while(!TX1STAbits.TRMT);
    TXREG = p;
}

/*
 * Esta função serve para escrever um conjunto de caracteres no pino RC6 (TX), não foi usada na aplicação,
 * entretanto pode ser útil para outras aplicações.
 */
void UART_Escrever_Texto(char* texto){
    int index;
    for(index=0; texto[index]!='\0'; index++)
        UART_Escrever(texto[index]);
}

#endif	/* UART_H */
