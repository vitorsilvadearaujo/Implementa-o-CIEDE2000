import numpy as np
from colormath import color_diff_matrix
import os
import sys
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from colormath import color_constants
from colormath import spectral_constants
from colormath.color_objects import (ColorBase,XYZColor,sRGBColor,LCHabColor,LCHuvColor,LabColor,xyYColor,LuvColor,HSVColor,HSLColor,CMYColor,CMYKColor,BaseRGBColor,IPTColor,SpectralColor)
from pyciede2000 import ciede2000
import numpy
#------FUNÇÃO DE TRANSFORMAÇÃO DE CORES NO SISTEMA R,G,B PARA X,Y,Z E POSTERIORMENTE LABCOLOR-----------
def rgb2lab(inputColor):
    print(inputColor)
    num = 0
    RGB = [0,0,0]
    for value in inputColor:

        value = float(value)/255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ];

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805;
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722;
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9504;
    XYZ[0] = round(X, 4);
    XYZ[1] = round(Y, 4);
    XYZ[2] = round(Z, 4);

    # Observer= 2°, Illuminant= D65
    XYZ[0] = float(XYZ[0]) / 95.047;         # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0;          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883;        # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16;
    a = 500 * (XYZ[0] - XYZ[1]);
    b = 200 * (XYZ[1] - XYZ[2]);

    Lab[0] = round(L, 4);
    Lab[1] = round(a, 4);
    Lab[2] = round(b, 4);

    return Lab

#------LER ARQUIVO DE ENTRADA-----------

arquivo = open('RGB.txt', 'r')
linhas = arquivo.readlines()
arquivo.close();
w=len(linhas);
t=0;
somaR=0;
somaG=0;
somaB=0;
soma=0;
valores=np.zeros((w,3));

#------CALCULA A MÉDIA DOS VALORES EM LABCOLOR E CONVERTE A ENTRADAD EM LABCOLOR ORGANIZANDO-A EM UMA MATRIZ-----------
for linha in linhas:
    campos = linha.split();
    campo1=campos[0].replace(",","");
    campo2=campos[1].replace(",","");
    campo3=campos[2].replace(",","");
    valores[t]=rgb2lab([campo1,campo2,campo3]);
    somaR=int(campo1)+ somaR;
    somaG=int(campo2)+ somaG;
    somaB=int(campo3)+ somaB;
    mediaR=somaR/w;
    mediaG=somaG/w;
    mediaB=somaB/w;
    mediaRR=mediaR;
    mediaGG=mediaG;
    mediaBB=mediaB;
    t=t+1;
ValReferenciaRGB= [mediaR,mediaG,mediaB];


def _get_lab_color1_vector(color):
    """
    CConverte uma LabColor em um NumPy vector.

    :param LabColor color:
    :rtype: numpy.ndarray
    # """
    # if not color.__class__.__name__ == 'LabColor':
    #     raise ValueError(
    #         "Funções delta E funcionam apenas para doios objetos LabCollor")
    return numpy.array([color.lab_l, color.lab_a, color.lab_b])

def _get_lab_color2_matrix(color):
    """
    Converte uma LabColor em uma NumPy matrix.

    :param LabColor color:
    :rtype: numpy.ndarray
    # """
    # if not color.__class__.__name__ == 'LabColor':
    #     raise ValueError(
    #         "Funções delta E funcionam apenas para doios objetos LabCollor")
    return numpy.array([(color.lab_l, color.lab_a, color.lab_b)])

def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie2000(
        color1_vector, color2_matrix, Kl=Kl, Kc=Kc, Kh=Kh)[0]
    return numpy.asscalar(delta_e)
    print(delta_e)

#------CALCULA A DIFERENÇA PERCEPTIVA ENTRE AS CORES DE ENTRADA E A MÉDIA RETORNANDO UMA MATRIZ DE RESULTADOS COM A ÚLTIMA COLUNA COMOAS DIFERENÇAS ENTRE AS CORES-----------
t=0;
soma=0;
ValReferencia= rgb2lab(ValReferenciaRGB);
color1= ValReferencia;
color2= [0,0,0];
result=np.zeros((w,4));
myInt=255;
ValReferenciaRGB = [float(i) / myInt for i in ValReferenciaRGB];
for linha in linhas:
    campos = linha.split();
    campo1=campos[0].replace(",","");
    campo2=campos[1].replace(",","");
    campo3=campos[2].replace(",","");
    campoo=[campo1,campo2,campo3];
    campo=[float(i) / myInt for i in campoo]
    for i in valores:
        color2=i;
        color1_rgb = sRGBColor(*ValReferenciaRGB);
        color2_rgb = sRGBColor(*campo);
        color1_lab = convert_color(color1_rgb,LabColor);
        color2_lab = convert_color(color2_rgb, LabColor);
    result[t]=(campo1,campo2,campo3,delta_e_cie2000(color1_lab,color2_lab));
#------CALCULO DO ÍNDICE DE DIFERENÇAS PERCEPTIVAS E APRESNTAÇÃO DOS RESULTADOS-----------
    soma = (result[t,3])+soma;
    t=t+1;

print(result)
índice=soma/w
print(índice)