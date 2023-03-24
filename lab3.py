from random import uniform
from math import sqrt, sin, radians
from matplotlib import pyplot as plt


def r_0_1() -> float:
    """Случайное число по равн. закону распределения от 0 до 1"""
    return uniform(0, 1)


def n_0_1() -> float:
    """Случайное число по норм. закону распределения мат. ожид. = 0, сред. квадр. откл. = 1"""
    s = 0
    for i in range(1, 13):
        s += r_0_1()
    return s - 6


def n_m_sigma(m: float, sigma: float) -> float:
    """Случайное число по норм. закону распределения при заданном мат. ожид. и сред. квадр. откл."""
    return m + sigma * n_0_1()


def cannon_shot(v: float, alpha: float) -> float:
    """Расчёт расстояния выстрела пушки"""
    print(f"V: {v}")
    print(f"Alpha: {alpha}")
    result = ((v**2)*sin(2 * alpha)) / 9.8
    print(f"-> ВЫСТРЕЛ:{result} (M)")
    print("---------------------------")
    return result


def graph_mu_d(x: int, separation: int, m: list, flag: int):
    """График мат. ожидания и дисперсии"""
    plt.plot([i for i in range(1, x, separation)], m)
    if flag == 1:
        plt.ylabel('Математическое ожидание')
    else:
        plt.ylabel('Дисперсия')
    plt.xlabel('Количество выстрелов')
    plt.xlim(1, x)
    plt.show()


def graph_p(p: list, m_n: list):
    """Функция построения гистограммы частоты попаданий"""
    n, bins, patches = plt.hist(m_n[:-1], m_n, weights=p)
    plt.title("Частоты попаданий в интервалы")
    plt.ylabel("Частота (%)")
    plt.xlabel("Интервал (метрах)")
    plt.show()


def target_hit_probability(result_shots: list, n_shots: int, d: int, L: int):
    """Расчёт попадания в мешень на расстоянии L, размером дельта"""
    k = 0
    S = 0
    for i in result_shots:
        S += i
        if (i >= (L - d / 2)) and (i <= (L + d / 2)):
            k += 1
    print("Средняя дальность выстрела:", S / n_shots)
    print("Вероятность попадания в заданную мишень: ", k / n_shots)


def calc_mu_D(list_shots: list, d: int):
    """Вычисление средних мат. ожидание и дисперсии"""
    mu = []
    D = []
    S_xi2 = 0
    S_xi = 0
    for i in range(len(list_shots)):
        S_xi += list_shots[i]
        S_xi2 += (list_shots[i]) ** 2
        if ((i + 1) % d) == 0:
            mu.append(S_xi / (i + 1))
            D.append((1 / i) * (S_xi2 - (1 / (i + 1)) * (S_xi ** 2)))
    return mu, D


def tank(n: int, m_v: float, m_alpha: float, sigma_v:float, sigma_alpha: float) -> list:
    """Функция генерирующая заданное количество выстрелов"""
    result_shots = []
    k = 1
    while k <= n:
        v_shot = n_m_sigma(m_v, sigma_v)
        alpha_shot = n_m_sigma(m_alpha, sigma_alpha)
        result_shots.append(cannon_shot(v_shot, alpha_shot))
        k += 1
    return result_shots


def calc_p(start: int, end: int, d: int, n_shots: int, result_shots: list):
    """Расчёты частоты попадания для гистограммы"""
    p = []
    n = []
    S_P = 0
    print(f"Вероятность попадения в интервал [{start}:{end}] = ", end="")
    start += d
    while start <= end:
        k = 0
        for j in result_shots:
            if (j >= (start - d)) and (j <= start):
                k += 1
        p.append(k / n_shots)
        S_P += (k / n_shots)
        n.append(start - d)
        start += d
    n.append(end)
    print(S_P)
    return p, n


def check_result(result_shot: list, mu: float, D: float):
    """Функция проверки, правилом 3 сигма """
    check_start = mu - 3 * sqrt(D)
    check_stop = mu + 3 * sqrt(D)
    k_check = 0
    for i in result_shot:
        if (i >= check_start) and (i <= check_stop):
            k_check += 1
    print("---------------ПРОВЕРКА РЕЗУЛЬТАТОВ---------------")
    print(f"При MU={mu}, D={D}, sigma={sqrt(D)} попадание в [{check_start}:{check_stop}] = {(k_check/len(result_shot))*100}(%)")


def main():
    """Основная функция, c вводом начальных значений и последовытельным выполнением действий лабораторныой работы"""
    # L = float(input("Введите дальность стрельбы (в метрах): "))
    L = 5000
    # delta = float(input("Введите размер мишени (в метрах): "))
    delta = 20
    m_alpha = radians(float(input("Введите мат. ожидание для угла (в градусах): ")))
    print(f"Математическое ожидание (в радианах): {m_alpha}")
    # m_v = float(input("Введите мат. ожид. для скорости: "))
    m_v = sqrt(L * 9.8/(sin(2 * m_alpha)))
    print(f"Вычислим мат. ожидание для скорости корень({L}*9.8)/sin(2*{m_alpha}) = {m_v}")
    sigma_v = float(input("Введите среднеквадр. откл для скорости: "))
    sigma_alpha = float(input("Введите среднеквадр. откл для угла: "))
    n_shots = int(input("Введите количество выстрелов пушки: "))
    del_n_shots = int(input("Введите размер деления выстрелов для диаграмм: "))
    graph_start = int(input("Введите точку начала для гистограммы: "))
    graph_end = int(input("Введите точку конца для гистограммы: "))
    graph_del = int(input("Введите размер деления для гистограммы: "))
    list_result_shots = tank(n_shots, m_v, m_alpha, sigma_v, sigma_alpha)
    m_mu, m_D = calc_mu_D(list_result_shots, del_n_shots)
    average_mu = sum(m_mu)/len(m_mu)
    average_D = sum(m_D)/len(m_D)
    # print(m_mu)
    # print(m_D)
    target_hit_probability(list_result_shots, n_shots, delta, L)
    m_p, m_n = calc_p(graph_start, graph_end, graph_del, n_shots, list_result_shots)
    # print(m_n)
    # print(m_p)
    graph_mu_d(n_shots, del_n_shots, m_mu, 1)
    graph_mu_d(n_shots, del_n_shots, m_D, 2)
    graph_p(m_p, m_n)
    check_result(list_result_shots, average_mu, average_D)


main()
