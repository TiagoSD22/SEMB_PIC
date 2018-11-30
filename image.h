/*
 *  Esta biblioteca serve para armazenar os pixels da imagem de teste e define o algoritmo de Roberts Cross.

 *  Autores : Tiago Dionizio e Lucas Magalh�es

 *  Copyright (C) 2018 Tiago Siqueira Dionizio  <tiagosdionizio@gmail.com>

 *  Copyright (C) 2018 Lucas Magalh�es de Sousa <lucasmag97@gmail.com> 

 *  Data de Atualiza��o : 20 de Novembro de 2018
*/

#ifndef IMAGE_H
#define	IMAGE_H

#include <math.h>

#define imgALTURA 4
#define imgLARGURA 4

/*
 * Esses valores s�o referentes aos pixels da imagem de teste, imagem com 43 linhas e 70 colunas.
 * Entretanto, a imagem armazenada � composta tamb�m da t�cnica de padding, logo, a estrutura de dados para comportar
 * a imagem deve ter duas linhas e duas colunas adicionais, referentes �s bordas do padding. Por isso os valors 0x0 
 * nas primeiras e �ltimas linhas e colunas.
 */
const unsigned char pixels[imgALTURA][imgLARGURA] = {1, 10, 20, 30,
                                                     1, 10, 20, 30,
                                                     1, 10, 20, 30,
                                                     1, 10, 20, 30,};

//M�scaras de convolu��o do filtro de Roberts Cross.
short robertX[2][2] = {{1,0},{0,-1}};
short robertY[2][2] = {{0,1},{-1,0}};

/*
 * Pela defini��o do algoritmo de Roberts, para um pixel em x,y dado por P(x,y) = p, 
 * seu novo valor, p' dado por P'(x,y) ser�:
    Gx = (P(x,y) - P(x + 1, y + 1))  (Convolu��o por robertX, define a varia��o horizontal)
    Gy = (P(x, y + 1) - P(x + 1, y)) (Convolu��o por robertY, define a varia��o vertical)
    P'(x,y) = sqrt(Gx^2 + Gy^2)
 * essa convolu��o � realizada pelos la�os for(x de 0 a 2) e for(y de 0 a 2).
 * Observe que o pixel � um dado do tipo unsigned char, por a imagem manipulada est� em formato .pgm bin�rio(P5),
 * em que os pixels podem assumir intensidades de 0 a 255, logo, s�o necess�rios 8 bits (1 byte) para armazenar 
 * cada pixel, aliado ao fato de que esses valores n�o podem ser negativos, 
 * o tipo unsigned char � o mais apropriado.
 */
unsigned char RobertsCross(short i, short j){
    int Gx = 0;
    int Gy = 0;
    short x,y;
    unsigned char novo_pixel;
    for(x = 0; x < 2; x++){
        for(y = 0; y < 2; y++){
            if(i > 1 && j > 1){
                Gx += pixels[i - 1 + x][j - 1 + y] * robertX[x][y];
                Gy += pixels[i - 1 + x][j - 1 + y] * robertY[x][y];
            }
            else{
                Gx += pixels[i + x][j + y] * robertX[x][y];
                Gy += pixels[i + x][j + y] * robertY[x][y];
            }
        }
    }
    novo_pixel = sqrt((float)(Gx*Gx) + (float)(Gy*Gy));
    return novo_pixel;
}

#endif	/* IMAGE_H */

