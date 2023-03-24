from random import normalvariate
from math import log, e, sqrt


def tilda(a: float, y: float) -> float:
    return -(1/a * log(y, e))


def create_list(n: int) -> list:
    return [0 for i in range(n)]


def normal():
    while True:
        s = normalvariate(0.5, sqrt(0.5))
        if (s > 0) and (s < 1):
            return s


def writ_experience(list_result: list, n_exp: int, s_buyers: int):
    list_mean = []
    s_customer = 0
    print("    ---------------РЕЗУЛЬТАТЫ ОПЫТОВ---------------")
    for i in range(n_exp):
        length = len(list_result[i])
        print(f"    -----РЕЗУЛЬТАТЫ {i + 1} ОПЫТА-----")
        for j in range(length - 1):
            if i == 0:
                list_mean.append(list_result[i][j])
            else:
                list_mean[j] += list_result[i][j]
            print(f"(<) {j+1} КАССА ОБСЛУЖИЛА {list_result[i][j]} ЧЕЛ.")
        if i == 0:
            list_mean.append(list_result[i][-1])
        else:
            list_mean[-1] += list_result[i][-1]
        print(f"(<) ОТКАЗАННО - {list_result[i][length-1]} ЧЕЛ.")
    print("    ---------------УСРЕДНЁННЫЕ РЕЗУЛЬТАТЫ ОПЫТОВ---------------")
    for i in range(len(list_mean)-1):
        print(f"(<) {i + 1} КАССА ОБСЛУЖИЛА В СРЕДНЕМ {list_mean[i]/n_exp} ЧЕЛ.")
        s_customer += list_mean[i]/n_exp
    print(f"(<) ОТКАЗАННО В СРЕДНЕМ - {list_mean[-1]/n_exp} ЧЕЛ.")
    print(f"(<) СРЕДНЕЕ ЧИСЛО ПОСЕТИТЕЛЕЙ: {s_buyers/n_exp}")
    print(f"(<) CРЕДНЕЕ ЧИСЛО ПОКУПАТЕЛЕЙ: {s_customer}")


def main():
    s_buyers = 0
    result = []
    n_exp = int(input("(>) Количество опытов: "))
    n = int(input("(>) Количество касс: "))
    processing_time = int(input("(>) Время обслуживания покупателя: "))
    total_time = int(input("(>) Общее время моделирования: "))
    apl_flow_density = float(input("(>) Плотность потока заявок: "))
    for i_exp in range(n_exp):
        list_cashbox = [create_list(n + 1), create_list(n)]
        time = 0
        n_buyer = 0
        while time <= total_time:
            i = 0
            while True:
                if list_cashbox[1][i] <= time:
                    list_cashbox[1][i] = time + processing_time
                    list_cashbox[0][i] += 1
                    print(f"(+) {i} КАССУ ЗАНЯЛ ПОКУПАТЕЛЬ №{n_buyer}, ОСВОБОДИТСЯ В {list_cashbox[1][i]}")
                    break
                else:
                    if i == (n - 1):
                        list_cashbox[0][n] += 1
                        print(f"(-) ПОКУПАТЕЛЮ №{n_buyer} ОТКАЗАНО В ОБСЛУЖИВАНИИ")
                        break
                    else:
                        i += 1
            time += tilda(apl_flow_density, normal())
            n_buyer += 1
            print(f"(!) ПРИШЕЛ ПОКУПАТЕЛЬ № {n_buyer} - ВРЕМЯ {time}")
        print(f"----------КОНЕЦ {i_exp + 1} ОПЫТА---------------")
        result.append(list_cashbox[0])
        s_buyers += n_buyer
    writ_experience(result, n_exp, s_buyers)


main()
