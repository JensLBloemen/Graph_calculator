## calculate new y given y= (y0, y1, y2, y3)
def f(q, y):
    return 1 + q / (y - 1)


def effectiveInteractionTriangle(y0: tuple[complex, complex, complex, complex],
                         y1: tuple[complex, complex, complex, complex],
                         q: complex) -> tuple[complex, ...]:
    Delta = q - 3 + y0[1] + y1[2] + y0[2] * y1[1]
    
    new_y_111 = (q - 1) * y0[0] * y1[0] + y0[3] * y1[3]
    new_y_112 = (q - 1) * y0[0] * y1[1] + y0[3] * y1[2] + y0[3] * (q - 2)
    new_y_121 = (q - 1) * y0[2] * y1[0] + y0[1] * y1[3] + y1[3] * (q - 2)
    new_y_122 = q - 2 + y0[2] * y1[1] + y0[1] * y1[2]
    return (new_y_111 / Delta, new_y_112 / Delta, new_y_121 / Delta, new_y_122 / Delta)



def effectiveInteractionStar(y0: tuple[complex, complex, complex, complex],
                         y1: tuple[complex, complex, complex, complex],
                         q: complex) -> tuple[complex, ...]:
    Delta = q - 3 + y0[3] + y1[3] + y0[2] * y1[1]
    
    new_y_111 = (q - 1) * y0[0] * y1[0] + y0[1] * y1[2]
    new_y_112 = (q - 1) * y0[0] * y1[1] + y0[1] * y1[3] + y0[1] * (q - 2)
    new_y_121 = (q - 1) * y0[2] * y1[0] + y0[3] * y1[2] + y1[2] * (q - 2)
    new_y_122 = q - 2 + y0[2] * y1[1] + y0[3] * y1[3]


    return (new_y_111 / Delta, new_y_112 / Delta, new_y_121 / Delta, new_y_122 / Delta)



def square_proj(y0, y1, q) -> complex:
    p1 = (q - 1) * y0[0] * y1[0] + y0[3] * y1[3]
    p2 = y0[1] * y1[1] + y0[2] * y1[2] + q - 2
    return (q - 1) * p1 / p2


def IsDense(y, q):
    tot = 0
    denum = y[2]+y[3]+q-2
    if denum.real * denum.real + denum.imag * denum.imag < 0.000001:
        return 0

    # fractionSU = (y[0]+y[1]) / (y[2]+y[3]+q-2) * (q - 1)
    # if fractionSU.real * fractionSU.real + fractionSU.imag * fractionSU.imag > 1:
    #     return 1
    # fractionSU = f(q, fractionSU)
    # if fractionSU.real * fractionSU.real + fractionSU.imag * fractionSU.imag > 1:
    #     return 1
    # return 0
    fractionTU = (y[0] + y[3]) / (y[1] + y[2] + q-2)* (q - 1)
    if fractionTU.real * fractionTU.real + fractionTU.imag * fractionTU.imag > 1:
        return 1
    fractionTU = f(q, fractionTU)
    if fractionTU.real * fractionTU.real + fractionTU.imag * fractionTU.imag > 1:
        return 1
    return 0
    # except ZeroDivisionError:
    #     if y[0]+y[1] == 0 and y[2]+y[3]+q-2 == 0:
    #         return 0
    #     if y[2]+y[3]+q-2 == 0:
    #         return 1
    #     if y[0] + y[3] == y[1] + y[2] + q-2 == 0:
    #         return 0
    #     if  y[1] + y[2] + q-2 == 0:
    #         return 1

    #     return 2
