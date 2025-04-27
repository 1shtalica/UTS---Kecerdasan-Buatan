import math
import random

# Desain GA
ukuranPopulasi = 100
ukuranKromosom = 32
maxGenerasi = 200
crossOverRate = 0.8
mutationRate = 1 / ukuranKromosom
elite_count = 1

# Fungsi Decode dan Konversi
def decode(kromosom):
    half = ukuranKromosom // 2
    x1_bin = kromosom[:half]
    x2_bin = kromosom[half:]
    x1 = binary_to_real(x1_bin, -10, 10)
    x2 = binary_to_real(x2_bin, -10, 10)
    return x1, x2

def binary_to_real(bits, a, b):
    value = int(bits, 2)
    return a + (value / (2**len(bits) - 1)) * (b - a)

# Fungsi Objektif
def objective_function(x1, x2):
    try:
        nilai = -(
            math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) +
            (3/4) * math.exp(1 - math.sqrt(x1**2))
        )
    except:
        nilai = float('inf')
    return nilai

# Fungsi Fitness
def hitung_fitness(kromosom):
    x1, x2 = decode(kromosom)
    nilai_obj = objective_function(x1, x2)
    if math.isnan(nilai_obj) or math.isinf(nilai_obj):
        return 0
    else:
        return 1 / (1 + max(0, nilai_obj))

# Seleksi Parent dengan Roulette Wheel
def roulette_wheel_selection(populasi, fitness_list):
    total_fitness = sum(fitness_list)
    rel_fitness = [f / total_fitness for f in fitness_list]
    cumulative = []
    current = 0
    for f in rel_fitness:
        current += f
        cumulative.append(current)

    def select_one():
        r = random.random()
        for i, cum_value in enumerate(cumulative):
            if r <= cum_value:
                return populasi[i]
        return populasi[-1]

    return select_one(), select_one()

# Crossover dengan multipoint crossover
def multipoint_crossover(parent1, parent2, num_points=2):
    if random.random() > crossOverRate:
        return parent1, parent2

    points = sorted(random.sample(range(1, ukuranKromosom), num_points))
    points = [0] + points + [ukuranKromosom]

    child1 = ''
    child2 = ''
    for i in range(len(points) - 1):
        start, end = points[i], points[i + 1]
        if i % 2 == 0:
            child1 += parent1[start:end]
            child2 += parent2[start:end]
        else:
            child1 += parent2[start:end]
            child2 += parent1[start:end]

    return child1, child2

# Mutasi
def mutasi(kromosom):
    hasil = ''
    for bit in kromosom:
        if random.random() < mutationRate:
            hasil += '1' if bit == '0' else '0'
        else:
            hasil += bit
    return hasil

# Inisialisasi Populasi
populasi = [''.join(random.choice('01') for _ in range(ukuranKromosom)) for _ in range(ukuranPopulasi)]

# Algoritma Utama
for generasi in range(maxGenerasi):
    fitness_list = [hitung_fitness(krom) for krom in populasi]
    
    # Simpan elit terbaik
    sorted_pop = sorted(zip(populasi, fitness_list), key=lambda x: x[1], reverse=True)
    elit = [ind[0] for ind in sorted_pop[:elite_count]]

    populasi_baru = elit.copy()

    # Buat sisa populasi dengan crossover dan mutasi
    while len(populasi_baru) < ukuranPopulasi:
        parent1, parent2 = roulette_wheel_selection(populasi, fitness_list)
        child1, child2 = multipoint_crossover(parent1, parent2)
        child1 = mutasi(child1)
        child2 = mutasi(child2)
        populasi_baru.extend([child1, child2])

    populasi = populasi_baru[:ukuranPopulasi]

# Output Solusi Terbaik 
fitness_list = [hitung_fitness(krom) for krom in populasi]
best_index = fitness_list.index(max(fitness_list))
best_krom = populasi[best_index]
x1_best, x2_best = decode(best_krom)
best_obj_value = objective_function(x1_best, x2_best)

print(f"Solusi terbaik ditemukan:")
print(f"Kromosom Terbaik = {best_krom}")
print(f"x1 = {x1_best}, x2 = {x2_best}")
print(f"Nilai fungsi objektif = {best_obj_value}")
