def _get_lab_color1_vector(color):
    """
    Converts an LabColor into a NumPy vector.

    :param LabColor color:
    :rtype: numpy.ndarray
    """
import numpy
    if not color.__class__.__name__ == 'LabColor':
        raise ValueError(
            "Funções delta E funcionam apenas para doios objetos LabCollor")
    return numpy.array([color.lab_l, color.lab_a, color.lab_b])