def delta_e_cie2000(color1, color2, Kl=1, Kc=1, Kh=1):
    """
    Calculates the Delta E (CIE2000) of two colors.
    """
import numpy
    color1_vector = _get_lab_color1_vector(color1)
    color2_matrix = _get_lab_color2_matrix(color2)
    delta_e = color_diff_matrix.delta_e_cie2000(
        color1_vector, color2_matrix, Kl=Kl, Kc=Kc, Kh=Kh)[0]
    return numpy.asscalar(delta_e)
    print(delta_e)
