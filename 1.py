import numpy as np
import math
import time
import matplotlib.pyplot as plt

def f(x):
    return np.log(x)


# Простая функция f_n(x):
# f_n(x) = i/n, где i/n ≤ ln(x) < (i+1)/n
# Реализация разбиения из т.(об аппроксимации измеримой ф-ии простыми)

def f_n(x, n):
    lx = np.log(x)
    i = np.floor(n * lx)  # определяем номер интервала ∆_i
    return i / n  # значение простой функции


# 2.1. Построение графиков
print("2.1. Графики f_n(x)")
x_vals = np.linspace(1, 4, 1000)
f_vals = f(x_vals)

# Графики для разных n
for n in [1, 2, 10, 100, 1000]:
    plt.figure(figsize=(8, 5))

    # График исходной функции
    plt.plot(x_vals, f_vals, 'k-', lw=2, label='ln x')

    # График простой функции
    plt.step(x_vals, f_n(x_vals, n), where='post', lw=1.5, label=f'f_{n}(x)')

    plt.title(f'f_n, n = {n}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'fn_plot_n_{n}.png', dpi=120)
    plt.close()
print()

# 2.2. Интеграл Лебега
print("2.2. Интеграл Лебега: ∫︁_E f_n d𝜆")

# Аналитическое значение ∫︁_1, 4  ln x dx
analyt_leb = 4 * math.log(4) - 3
print(f"Аналитически: ∫︁ ln x dx = {analyt_leb:.10f}\n")


# Вычисление интеграла Лебега от f_n
# ∫︁ f_n d𝜆 = ∑︁ (i/n) * 𝜆(A_i),
# где A_i = [e^{i/n}, e^{(i+1)/n}) ∩ [1,4]

def leb_integral_fn(n):
    res = 0.0
    i = 0

    # Перебор всех интервалов Δ_i, попадающих в диапазон значений ln(x)
    while i / n <= math.log(4):

        # Границы множества A_i
        a_i = max(math.exp(i / n), 1.0)
        b_i = min(math.exp((i + 1) / n), 4.0)

        # Если вышли за пределы отрезка - прекращаем
        if a_i >= 4.0:
            break

        # Добавляем вклад (i/n) * длина интервала
        if b_i > a_i:
            res += (i / n) * (b_i - a_i)
        i += 1
    return res


print(f"{'n':>6} | {'∫︁ f_n d𝜆':>16} | {'Ошибка':>12} | {'Время, с':>10}")
print("-" * 54)

# Вычисления для разных n
for n in [10, 100, 1000]:
    t0 = time.time()
    val = leb_integral_fn(n)
    elapsed = time.time() - t0
    err = abs(val - analyt_leb)
    print(f"{n:>6} | {val:>16.10f} | {err:>12.3e} | {elapsed:>10.6f}")

print()

# 2.3. Интеграл Лебега–Стилтьеса
print("2.3. Интеграл Лебега–Стилтьеса: ∫︁_E f_n d𝜇_F")

# Точки разрыва F(x)=⌈x^2⌉: x = √k, k = 2,...,16
break_points = [math.sqrt(k) for k in range(2, 17)]

# Аналитическое значение (1/2)·ln(16!)
analyt = sum(0.5 * math.log(k) for k in range(2, 17))
print(f"Аналитически: (1/2)·ln(16!) = {analyt:.10f}\n")


# Интеграл Лебега–Стилтьеса:
# ∫︁ f_n d𝜇_F = ∑︁ f_n(x_k), x_k - точки разрыва функции F
def st_integral_fn(n):
    res = 0.0
    for xk in break_points:
        # значение простой функции в точке разрыва
        i = math.floor(n * math.log(xk))
        fn_val = i / n
        res += fn_val
    return res


print(f"{'n':>6} | {'∫︁ f_n d𝜇_F':>16} | {'Ошибка':>12} | {'Время, с':>10}")
print("-" * 54)

# Вычисления для разных n
for n in [50, 500, 5000, 10000, 15000]:
    t0 = time.time()
    val = st_integral_fn(n)
    elapsed = time.time() - t0
    err = abs(val - analyt)
    print(f"{n:>6} | {val:>16.10f} | {err:>12.3e} | {elapsed:>10.6f}")