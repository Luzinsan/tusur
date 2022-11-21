import plotly.express as px
import plotly.graph_objects as go
import sympy
import numpy as np


# Симплекс в моем случае - треугольник.  Ищем минимум
def Simplex(f, x, eps):
    k = 1
    gamma = np.random.rand()  # Коэффициент сжатия. От 0 до 1
    n = len(x)  # Размер измерения (двумерная)
    L = n + 1  # Размер симплекса
    p = (L / (n * np.sqrt(2))) * (np.sqrt(n + 1) + n - 1)
    q = (L / (n * np.sqrt(2))) * (np.sqrt(n + 1) - 1)
    _x_ = np.zeros((L, n),
                   dtype=x.dtype)  # Нули размера n*l Массив из нулей, с соответствующим типом входных данных (тип
    # подбирается сам, можно написать дробные числа np.float64)
    _x_[1:, :] = q  # все, кроме первой строчки становится q по картинке
    for i in range(n):  # по диагонали становится p
        _x_[i + 1, i] = p
    simpl = np.zeros((L, n), dtype=np.float64)  # Построение самого симплекса
    simpl[0] = x  # Исходная вершина, шаг 1
    simpl = simpl[0] + _x_  # производится по формуле 2.1
    res = [0] * L  # Массив, в который сохраняется значения функции, для второго шага.
    while True:  # Шаг второй. Считает значение функции. ЦФ - целевая функция
        for i in range(L):  # Для каждой точки симплекса
            res[i] = f(*simpl[i])  # Сам подсчет целевой функции
        for i in range(
                n):  # Шаг 3. Если точки достаточно близки друг к другу (Значение функций в этих точках и точки
            # симплекса)
            if abs(res[i + 1] - res[i]) <= eps and np.sqrt(((simpl[i + 1] - simpl[
                i]) ** 2).sum()) <= eps:  # Если значения функции в этих точках достаточно близки друг к другу.
                return (simpl[i] + simpl[i + 1]) / 2, k, (
                        res[i + 1] + res[i]) / 2  # Маленький симплекс, пришли к минимуму
        maxarg = np.argmax(res)  # Шаг 4. Наихудшая вершина - значение максимальное. Номер вершины в симплексе.
        ref = (simpl.sum(axis=0) - simpl[maxarg]) * 2 / n - simpl[
            maxarg]  # Шаг 5. Отражение. Сложили все вершины симплекса (3 вершины) и отняли худшую. Отражаем самую
        # худшую
        if f(*ref) > res[maxarg]:  # Отраженная точка больше или меньше исходной худшей точки Шаг 6. Если больше,
            # то забываем и
            # делаем сжатие относительно лучшей точки
            minarg = np.argmin(res)
            simpl = simpl[minarg] * gamma + (1 - gamma) * simpl
        else:  # Если меньше, то мы ее записываем на место худшей точки
            simpl[maxarg] = ref
        k += 1
    return simpl, k, res


def Hooke(f, x, eps):
    k = 1
    alpha = 1 + np.random.rand() * 10  # Коэффициент почти сжатия
    n = len(x)  # Размер измерения (двумерный)
    delta = x.copy()  # Костыль. Копия размера x. Размер массив размера как x, но со значением 10. Шаг 1 начало
    delta[:] = 10  # Чтоб определить шаги
    best = x.copy()  # Костыль. Копия. Шаг 1 конец
    foundbetter = False
    while True:
        foundbetter = False  # Исследующий поиск.
        for i in range(n):  # В каждом направлении сделать шаг и посмотреть, в сторону увеличения или уменьшения
            newbest = best.copy()
            newbest[i] += delta[i]  # Прибавляем по одной координате
            if f(*best) > f(
                    *newbest):  # Получилось лучше или хуже, если лучше - запоминаем, хуже - пропускаем тот путь.
                best = newbest
                foundbetter = True
                continue
            newbest = best.copy()
            newbest[i] -= delta[i]  # Убавляем по одной координате
            if f(*best) > f(
                    *newbest):  # Получилось лучше или хуже, если лучше - запоминаем, хуже - пропускаем тот путь.
                best = newbest
                foundbetter = True
        if not (
                foundbetter):  # Если не удачный, то мы проверяем, если шаг по оси достаточно маленькие, значит мы в минимуме, если шаги большие, то уменьшаем и повторяем. Шаг 3
            if any(delta < eps):  # Шаг 4. Немного не так написан, но суть та же. Разная суть доноса из методички.
                return best, k, f(*best)
            else:
                delta /= alpha
        k += 1
        while True:
            newbest = best + (best - x)  # Шаг 5. Ведет нас к лучшей точке. Шаг 6 = шаг 2.
            if f(*newbest) < f(
                    *best):  # Если она меньше, значит мы ее запоминаем, ибо она лучшая. Иначе - мы ищем новое направление. Шаг 7
                best = newbest
            else:
                break
    return best, k, f(*best)


def lab3():
    x1 = sympy.Symbol('x1')
    x2 = sympy.Symbol('x2')
    f = x1 ** 3 + x2 ** 3 - 15 * x1 * x2
    print('f(x1,x2)={}'.format(f))

    _x = [0, 0]
    _x0 = [5.23, 4.41]
    print('x={}\nx0={}'.format(_x, _x0))

    eps = 1e-4

    foo = sympy.lambdify([x1, x2], f, 'numpy')
    print("Симплексный метод: x*={}, k={}, f(x*)={}".format(*Simplex(foo, np.array(_x0, dtype=np.float64), eps)))
    print("Метод Хука-Дживса: x*={}, k={}, f(x*)={}".format(*Hooke(foo, np.array(_x0, dtype=np.float64), eps)))
    x = np.linspace(-1, 10, 20)
    y = np.linspace(-1, 10, 20)
    X, Y = np.meshgrid(x, y)
    Z = foo(X, Y)
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
    fig.add_trace(go.Scatter3d(x=[_x[0]], y=[_x[1]], z=[foo(*_x)]))
    fig.add_trace(go.Scatter3d(x=[_x0[0]], y=[_x0[1]], z=[foo(*_x0)]))
    fig.show()
    pass


lab3()
