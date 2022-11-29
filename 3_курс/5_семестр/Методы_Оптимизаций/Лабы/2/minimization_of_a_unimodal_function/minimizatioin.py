from MinExpression import *

if __name__ == "__main__":
    func = Expression(filename="expression.txt")
    eps = str(func.eps).rfind('1')

    # region Dichotomy
    # print("\n\tDICHOTOMY METHOD\n")
    # (min_f_dich, val_min_f_dich), counter = func.dichotomy()
    # func.show_plot()
    # print(f'Minimal argument of function:{min_f_dich};\nValue of one: {val_min_f_dich};\nIterations: {counter}')
    # print('Calculation error along the abscissa of the dichotomy method: {0:.{1}e}'.format(-1 - min_f_dich, eps))
    # endregion

    # region Golden ratio
    # print("\n\tGOLDEN RATIO METHOD\n")
    # (min_f_gol, val_min_f_gol), counter = func.golden_ratio()
    # func.show_plot()
    # print(f'Minimal argument of function:{min_f_gol};\nValue of one: {val_min_f_gol};\nIterations: {counter}')
    # print('Calculation error along the abscissa of the golden section method: {0:.{1}e}'.format(-1 - min_f_gol, eps))
    # endregion

    # region newton
    init = 95.0
    print(f"\tInitial approximation of the minimum of the function: {init}\n")
    (extr_f, val_extr_f, type), counter = func.newton_init(2, init)
    print(f'Iterations: {counter}')
    if type == 'min':
        print(f'Minimal argument of function: {extr_f};\nValue of one: {val_extr_f}')
    elif type == 'max':
        print(f'Maximum argument of function: {extr_f};\nValue of one: {val_extr_f}')
    elif type == 'dispersed':
        print(f'Inflection point of function: {extr_f};\nValue of one: {val_extr_f}')
    else:
        print(f'The function diverges. Found extremum:  {extr_f};\nValue of one: {val_extr_f}')
    func.show_plot()
    # endregion

    # region bolzabo
    # extr_f, val_extr_f, counter = func.bolzano()
    # print(f'Iterations: {counter}')
    # print(f'Minimal argument of function: {extr_f};\nValue of one: {val_extr_f}')
    # func.show_plot()
    # endregion


