import timeit
from typing import Callable

# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    base = 256 
    modulus = 101  
    
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1

# Тестування
def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='cp1251') as f:
            return f.read()

def benchmark(func: Callable, text_: str, pattern_: str):
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(text, pattern)"
    return timeit.timeit(stmt=stmt, setup=setup_code, globals={'text': text_, 'pattern': pattern_}, number=10)

if __name__ == '__main__':
    PINK = '\033[95m'
    RESET = '\033[0m'
    
    files = ['article_1.txt', 'article_2.txt']
    algorithms = [boyer_moore_search, kmp_search, rabin_karp_search]
    
    for file in files:
        try:
            text = read_file(file)
            print(f"\nАналіз файлу: {file}")
            
            if file == 'article_1.txt':
                real_pattern = "структурі даних"
            else:
                real_pattern = "Аналіз"
            
            fake_pattern = "космос"
            
            results = []
            
            for pattern in (real_pattern, fake_pattern):
                for algo in algorithms:
                    position = algo(text, pattern)
                    res_str = f"Індекс: {position}" if position != -1 else "Не знайдено"
                    
                    time = benchmark(algo, text, pattern)
                    results.append((algo.__name__, pattern, res_str, time))
            
            min_time = min(r[3] for r in results)
            
            title = f"{'Алгоритм':<25} | {'Підрядок':<20} | {'Результат':<15} | {'Час виконання, сек'}"
            print(title)
            print("-" * len(title))
            
            for result in results:
                row_str = f"{result[0]:<25} | {result[1]:<20} | {result[2]:<15} | {result[3]:.6f}"
                
                if result[3] == min_time:
                    print(f"{PINK}{row_str}{RESET}")
                else:
                    print(row_str)
                    
        except FileNotFoundError:
            print(f"Помилка: Файл {file} не знайдено.")