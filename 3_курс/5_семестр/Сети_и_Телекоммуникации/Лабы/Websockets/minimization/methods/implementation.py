from sympy import symbols, Expr, diff, plotting, plot, Interval, minimum, maximum
import numpy as np
from matplotlib import style
from imageio import imread, mimsave
from math import sqrt
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, parse_expr

x = symbols('x')
ITERATIONS = 50


class Expression:
    def __init__(self, filename='', **kwargs) -> None:
        if filename != '':
            with open(filename, "rt") as file:
                expression = file.readline()
                self.__start, self.__end, self.__eps = [parse_expr(num).evalf() for num in file.readline().split()]
                transformations = (standard_transformations + (implicit_multiplication_application,))
                self.__function: Expr = parse_expr(expression, transformations=transformations)
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.__diff1: Expr = diff(self.__function, x, 1)
        self.__diff2: Expr = diff(self.__function, x, 2)
        self.__diff3: Expr = diff(self.__function, x, 3)
        self.__x_min = 0.0
        self.__y_min = 0.0
        self.__x_max = 0.0
        self.__y_max = 0.0
        self.__x_approx_min: np.array = None
        self.__y_val_approx_min: np.array = None
        self.__y_diff_val_approx_min: np.array = None

        self.__plot_0: plotting = plot(self.__function, show=True, #xlim=(self.__start, self.__end),
                                      # ylim=(minimum(self.__function, x, Interval(self.__start, self.__end)),
                                       #      maximum(self.__function, x, Interval(self.__start, self.__end))),
                                       markers=[],
                                       line_color='xkcd:light purple', legend=True, xlabel=None, ylabel=None)
        self.__plot_1: plotting = plot(self.diff1, show=False,# xlim=(self.__start, self.__end),
                                     #  ylim=(minimum(self.__diff1, x, Interval(self.__start, self.__end)),
                                     #        maximum(self.__diff1, x, Interval(self.__start, self.__end))),
                                       markers=[],
                                       line_color='xkcd:bright red', legend=True, xlabel=None, ylabel=None)
        self.__plot_grid = plotting.PlotGrid(1, 2, self.__plot_0, self.__plot_1, show=False, size=(8., 8.5))
        style.use('dark_background')
        self.show_plot()

    # region Property
    @property
    def min(self) -> {float: float}:
        return {self.__x_min: self.__y_min}

    @property
    def func(self) -> Expr:
        return self.__function

    @property
    def diff1(self) -> Expr:
        return self.__diff1

    @property
    def diff2(self) -> Expr:
        return self.__diff2

    @property
    def diff3(self) -> Expr:
        return self.__diff3

    @property
    def eps(self) -> float:
        return self.__eps

    def show_plot(self) -> None:
        self.__plot_grid.show()

    # endregion

    # region StaticMethods
    @staticmethod
    def border_shift(function, start, end, **kwargs):
        f_x = {'x_left': [0, 0], 'x_right': [0, 0]}
        for name, value in kwargs.items():
            f_arg = [value, function.subs(x, value).evalf()]
            if name == 'x_center':
                if f_arg[1] > 0:
                    return start, value
                else:
                    return value, end
            elif name == 'x_left':
                f_x['x_left'] = f_arg
            elif name == 'x_right':
                f_x['x_right'] = f_arg
        if f_x['x_left'][1] < f_x['x_right'][1]:
            return start, f_x['x_right'][0]
        else:
            return f_x['x_left'][0], end


    @staticmethod
    def initial_approximation(diff1, diff3, left, right):
        """Начальное приближение минимума функции"""
        # критерий сходимости: f'(x_k) * f'''(x_k) > 0
        if diff1.subs(x, left) * diff3.subs(x, left) > 0:  # левая граница подходит?
            return left
        elif diff1.subs(x, right) * diff3.subs(x, right) > 0:  # правая граница подходит?
            return right
        elif diff1.subs(x, (left + right) / 2) * diff3.subs(x, (left + right) / 2) > 0:  # тогда может середина?
            return (left + right) / 2
        else:
            return None

    is_stop_criterion = lambda self, x_prev, x_curr, counter: \
        (abs(x_curr - x_prev) <= self.__eps and abs(self.__diff1.subs(x, x_curr).evalf()) <= (2 * self.__eps)) \
        or (counter >= ITERATIONS) \
        or (x_curr < self.__start or x_curr > self.__end)


    is_min_extremum = lambda diff1_func, diff2_func, argument, eps: \
        (abs(diff1_func.subs(x, argument).evalf()) <= eps) and diff2_func.subs(x, argument).evalf() >= 0

    is_max_extremum = lambda diff1_func, diff2_func, argument, eps: \
        (abs(diff1_func.subs(x, argument).evalf()) <= eps) and diff2_func.subs(x, argument).evalf() <= 0

    is_inflection = lambda diff1_func, diff2_func, argument, eps: \
        (abs(diff1_func.subs(x, argument).evalf()) <= (2 * eps)) and abs(diff2_func.subs(x, argument).evalf()) <= eps

    def append_approximation(self, x_next):
        np.append(self.__x_approx_min, x_next)
        np.append(self.__y_val_approx_min, self.__function.subs(x, x_next).evalf())
        self.__plot_0.markers.append({'args': [x_next, self.__function.subs(x, x_next).evalf(), 'o'],
                                      'color': 'xkcd:cyan', 'ms': 5})
        np.append(self.__y_diff_val_approx_min, self.__diff1.subs(x, x_next).evalf())
        self.__plot_1.markers.append({'args': [x_next, self.__diff1.subs(x, x_next).evalf(), 'o'],
                                      'color': 'xkcd:pale yellow', 'ms': 5})
        return x_next

    # endregion

    # region Simple Methods
    def dichotomy(self):
        x_curr = (self.__start + self.__end) / 2
        start_curr, end_curr = self.__start, self.__end
        self.__x_approx_min: np.array = None
        self.__y_val_approx_min: np.array = None
        self.__y_diff_val_approx_min: np.array = None
        counter = 0
        images = []
        while True:
            x_prev = x_curr
            self.append_approximation(x_curr)
            x_left = x_curr - (self.__eps / 2).evalf()
            x_right = x_curr + (self.__eps / 2)
            start_curr, end_curr = Expression.border_shift(self.__function, start_curr, end_curr,
                                                           x_left=x_left, x_right=x_right)
            x_curr = (start_curr + end_curr) / 2
            print(x_curr)
            self.__plot_grid.save(f'../minimization_of_a_unimodal_function/Plots/dichotomy/dichotomy{counter}.png')
            images.append(
                imread(f'../minimization_of_a_unimodal_function/Plots/dichotomy/dichotomy{counter}.png'))
            counter += 1
            if abs(end_curr - start_curr) / 2 < self.__eps \
                    and abs(self.__function.subs(x, x_curr).evalf()
                            - self.__function.subs(x, x_prev).evalf()) < self.__eps:
                break
        self.__x_min = x_curr
        self.__y_min = self.__function.subs(x, x_curr).evalf()
        mimsave('../minimization_of_a_unimodal_function/gifs/dichotomy.gif', images, duration=0.5)
        return (self.__x_min, self.__y_min), counter

    def golden_ratio(self):
        harmonic_division = (1 + sqrt(5)) / 2
        x_curr = (self.__start + self.__end) / 2
        start_curr, end_curr = self.__start, self.__end
        self.__x_approx_min: np.array = np.empty(1)
        self.__y_val_approx_min: np.array = np.empty(1)
        self.__y_diff_val_approx_min: np.array = np.empty(1)
        counter = 0
        images = []
        while True:
            x_prev = x_curr
            self.append_approximation(x_curr)
            delta = end_curr - start_curr
            x_left = start_curr + (delta / (harmonic_division ** 2))
            x_right = start_curr + (delta / harmonic_division)
            start_curr, end_curr = Expression.border_shift(self.__function, start_curr, end_curr, x_left=x_left, x_right=x_right)
            x_curr = (start_curr + end_curr) / 2
            print(x_curr)
            self.__plot_grid.save(
                f'../minimization_of_a_unimodal_function/Plots/golden_ratio/golden_ratio{counter}.png')
            images.append(
                imread(f'../minimization_of_a_unimodal_function/Plots/golden_ratio/golden_ratio{counter}.png'))
            counter += 1
            # self.show_plot()
            if abs(end_curr - start_curr) / 2 < self.__eps \
                    and abs(self.__function.subs(x, x_curr).evalf()
                            - self.__function.subs(x, x_prev).evalf()) < self.__eps:
                break
        self.__x_min = x_curr
        self.__y_min = self.__function.subs(x, x_curr).evalf()
        mimsave('../minimization_of_a_unimodal_function/gifs/golden_ratio.gif', images, duration=0.5)
        return (self.__x_min, self.__y_min), counter

    # endregion

    # region Newton
    def newton_get_method(self, type=0):
        if type == 0:
            print('NEWTON RAPHSON METHOD')
            return self.newton_raphson, 'newton_raphson'
        elif type == 1:
            print('NEWTON SIMPLE METHOD')
            return self.newton_simple, 'newton_simple'
        elif type == 2:
            print('NEWTON SECANT METHOD')
            return self.newton_secant, 'newton_secant'
        elif type == 3:
            print('NEWTON STEPHENSEN METHOD')
            return self.newton_stephensen, 'newton_stephensen'
        elif type == 4:
            print('NEWTON WALL METHOD')
            return self.newton_wall, 'newton_wall'
        else:
            return -1, ''

    def newton_init(self, type=0, x_curr=None):
        self.__x_approx_min: np.array = None
        self.__y_val_approx_min: np.array = None
        self.__y_diff_val_approx_min: np.array = None

        #  Проверка критерия сходимости - определение начального приближения
        if not x_curr:
            x_curr = self.initial_approximation(self.__diff1, self.__diff3, self.__start, self.__end)
        method, type_str = self.newton_get_method(type)
        self.__plot_0.title = type_str
        self.__plot_0.markers.append({'args': [x_curr, self.__function.subs(x, x_curr).evalf(), '*'],
                                      'color': 'xkcd:yellow', 'ms': 6})
        self.__plot_0.annotations = [{'xy': (x_curr, self.__function.subs(x, x_curr).evalf()),
                                      'text': 'x_0 \n= ({0:.2e}, {1:.2e})'.format(x_curr, self.__function.subs(x, x_curr).evalf()),
                                      'ha': 'left', 'va': 'bottom', 'color': 'yellow'}]
        x_prev = None
        if method == self.newton_secant:
            x_prev = self.initial_approximation(self.__diff1, self.__diff3, self.__start, self.__end - self.__eps)
        x_curr, counter, images = self.newton_get_approx_by_method(method, type_str, x_curr, x_prev)
        self.__plot_0.annotations.append({'xy': (x_curr, self.__function.subs(x, x_curr).evalf()),
                                      'text': 'x* \n= ({0:.2e}, {1:.2e})'.format(x_curr,
                                                                              self.__function.subs(x, x_curr).evalf()),
                                      'ha': 'left', 'va': 'bottom', 'color': 'yellow'})
        eps = str(self.__eps).rfind('1')
        print('Calculation error along the abscissa of the {0}  method: {1:.{2}e}'.format(
            type_str, minimum(self.__function, x, Interval(self.__start, self.__end)) - x_curr, eps))
        mimsave(f'../minimization_of_a_unimodal_function/gifs/{type_str}.gif', images, duration=0.5)
        return (self.classification(x_curr)), counter

    def newton_get_approx_by_method(self, method, method_str, x_curr, x_prev=None):
        counter = 0
        images = []
        alpha = None
        if method == self.newton_simple:
            alpha = self.diff2.subs(x, x_curr) if self.diff2.subs(x, x_curr) != 0 else None
        if x_prev is None:
            x_prev = x_curr
        temp_secant = 0.0
        while Rrue:
            counter += 1
            if method == self.newton_secant:
                temp_secant = x_curr
                x_curr = method(x_curr, x_prev, alpha)
                x_prev = temp_secant
            else:
                x_prev = x_curr
                x_curr = method(x_curr, x_prev, alpha)
            print(x_curr)
            self.append_approximation(x_curr)
            self.__plot_grid.save(
                f'../minimization_of_a_unimodal_function/Plots/newton/{method_str}/{method_str}{counter}.png')
            images.append(imread(
                f'../minimization_of_a_unimodal_function/Plots/newton/{method_str}/{method_str}{counter}.png'))
            if self.is_stop_criterion(x_prev, x_curr, counter):
                return (x_curr, counter, images)

    def classification(self, x_curr):
        #  Классификация найденной точки
        if Expression.is_min_extremum(self.__diff1, self.__diff2, x_curr, self.__eps):
            self.__x_min = x_curr
            self.__y_min = self.__function.subs(x, x_curr).evalf()
            return (self.__x_min, self.__y_min, 'min')
        elif Expression.is_max_extremum(self.__diff1, self.__diff2, x_curr, self.__eps):
            self.__x_max = x_curr
            self.__y_max = self.__function.subs(x, x_curr).evalf()
            return (self.__x_max, self.__y_max, 'max')
        elif Expression.is_inflection(self.__diff1, self.__diff2, x_curr, self.__eps):
            return (x_curr, self.__function.subs(x, x_curr).evalf(), 'inflection')
        else:
            print(f'diff1 of x_curr is {abs(self.__diff1.subs(x, x_curr).evalf())}')
            print(f'diff1 of x_curr is {abs(self.__diff2.subs(x, x_curr).evalf())}')
            return (x_curr, self.__function.subs(x, x_curr).evalf(), 'diverged')

    # region Methods
    newton_raphson = lambda self, x_curr, x_prev=0.0, alpha=0.0: \
        x_curr - self.__diff1.subs(x, x_curr) / self.__diff2.subs(x, x_curr)

    newton_simple = lambda self, x_curr, x_prev, alpha: \
        x_curr - (self.__diff1.subs(x, x_curr) / alpha)

    newton_secant = lambda self, x_curr, x_prev, alpha=0.0: \
        x_curr - (x_curr - x_prev) \
        / (self.__diff1.subs(x, x_curr) - self.__diff1.subs(x, x_prev)) * self.__diff1.subs(x, x_curr)

    newton_stephensen = lambda self, x_curr, x_prev=0.0, alpha=0.0: \
        x_curr - ((self.__diff1.subs(x, x_curr) ** 2) \
                  / (self.__diff1.subs(x, x_curr + self.__diff1.subs(x, x_curr))
                     - self.__diff1.subs(x, x_curr)))

    newton_wall = lambda self, x_curr, x_prev=0.0, alpha=0.0: \
        x_curr - self.__diff1.subs(x, x_curr) \
        / (self.__diff2.subs(x, x_curr) - ((self.__diff1.subs(x, x_curr) * self.__diff3.subs(x, x_curr))
                                           / (2 * self.__diff2.subs(x, x_curr))))
    # endregion
    # endregion

    # region Bolzano
    def bolzano(self):
        print("METHOD BOLZANO")
        x_curr = (self.__start + self.__end) / 2
        print(f'Start approximation: {x_curr}')
        self.__x_approx_min: np.array = None
        self.__y_val_approx_min: np.array = None
        self.__y_diff_val_approx_min: np.array = None
        start_curr, end_curr = self.__start, self.__end
        counter = 0
        images = []
        while True:
            x_prev = x_curr
            self.append_approximation(x_curr)
            x_curr = (start_curr + end_curr) / 2
            start_curr, end_curr = Expression.border_shift(self.__diff1, start_curr, end_curr, x_center=x_curr)
            print(x_curr)
            self.__plot_grid.save(f'../minimization_of_a_unimodal_function/Plots/bolzano/bolzano{counter}.png')
            images.append(
                imread(f'../minimization_of_a_unimodal_function/Plots/bolzano/bolzano{counter}.png'))
            counter += 1
            if abs(end_curr - start_curr) / 2 < self.__eps \
                    and abs(self.__function.subs(x, x_curr).evalf()
                            - self.__function.subs(x, x_prev).evalf()) < self.__eps:
                break
        self.__x_min = x_curr
        self.__y_min = self.__function.subs(x, x_curr).evalf()
        mimsave('../minimization_of_a_unimodal_function/gifs/bolzano.gif', images, duration=0.5)
        return self.__x_min, self.__y_min, counter

    #endregion
