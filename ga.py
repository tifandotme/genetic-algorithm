import numpy as np
import math
import random

"""
Tifan Dwi Avianto
A11.2017.10629

Program ini untuk mencari solusi dari persamaan
a+2b+3c+4d = 30
"""

class algoritma_genetika:
	# 1. PEMBENTUKAN KROMOSOM
	jumlah_chrom = 6
	gen = ["a", "b", "c", "d"]
	nilai_per_gen = {
		'min' : 0,
		'max' : 30
	}

	crossover_rate = 50/100
	mutasi_rate = 50/100
	total_generasi = 1000
	next_gen = np.arange(4)

	stop = False

	# 2. INISIALISASI
	def __init__(self):
		# generasi chromosome yang random
		self.first_chromosome = np.random.randint(low=self.nilai_per_gen['min'], high=self.nilai_per_gen['max'], size=(self.jumlah_chrom, len(self.gen)))
		print(self.first_chromosome)

	# 3. EVALUASI KROMOSOM
	def evaluasi_chrom(self, chrom, generasi):
		print("GENERASI ["+str(generasi)+"]")

		jumlah_chromo = len(chrom)
		j = np.arange(jumlah_chromo)
		fitness = np.arange(jumlah_chromo, dtype='f')

		for x in range(len(chrom)):

			# fungsi objektif
			ev = abs((chrom[x][0] + 2*chrom[x][1] + 3*chrom[x][2] + 4*chrom[x][3])-30)
			j[x] = ev

			# seleksi dan mencari fitness
			fitn = 1/(ev+1)

			fitness[x] = fitn
			if (fitn == 1):
				self.stop = True

			print("CHROMOSOME {0} : {1}, fitness = {2}".format(x, np.array2string(chrom[x], separator=','), fitn))

		print("FITNESS SELESAI")
		print(j)

		# 4. SELEKSI KROMOSOM
		P = np.arange(jumlah_chromo, dtype='f')

		total_fitness = fitness.sum()
		P = fitness / total_fitness
		print("total fitness : {}".format(str(total_fitness)))
		print("Rata-rata fitness : {}".format(str(np.average(fitness))))
		print("Probabilitas : {}".format(np.array2string(P, separator=',')))
		print("Probabilitas Paling Tinggi : {}, pada chromosome {}".format(P[P.argmax()], str(P.argmax())))
		print("Chromosome Yang Mungkin Terpilih : {}".format(np.array2string(chrom[P.argmax()], separator=',')))

		self.next_gen = chrom[P.argmax()]

		# proses seleksi roullete wheel
		C = np.arange(jumlah_chromo, dtype='f')
		total_x = 0
		for x in range(len(P)):
			total_x += P[x]
			C[x] = total_x

		# putar roullete wheel sebanyak jumlah sel
		R = np.random.sample(len(fitness))
		new_chrom = np.arange(jumlah_chromo*len(self.gen)).reshape(jumlah_chromo, len(self.gen))

		#chromosome baru berdasarkan roulette wheel
		for y in range(len(R)):
			for k in range(len(new_chrom)):
				if (R[y] < C[0]):
					new_chrom[y] = chrom[0]
				elif((C[k-1] < R[y]) & (R[y] < C[k])):
					new_chrom[y] = chrom [k]

		# 5. CROSSOVER
		R = np.random.sample(jumlah_chromo)
		index_chrom_parent = []
		for p in range(len(R)):
			if(R[p] < self.crossover_rate):
				index_chrom_parent.append(p)


		#MENENTUKAN POSISI CROSS OVER
		#membangkitkan bilangan acak dari 1 sampai (panjang chromosome - 1)
		posisi_CO = np.random.randint(low=1, high=len(self.gen), size=len(index_chrom_parent))

		#menentukan posisi crossover
		#membangkitkan bilangan acak dari 1 sampai (panjang chromosome - 1)
		off_spring = np.arange(len(self.gen)*len(index_chrom_parent)).reshape(len(index_chrom_parent), len(self.gen))

		for i_parent in range(len(index_chrom_parent)):
			index_chrome_1 = index_chrom_parent[i_parent]
			if(i_parent == len(index_chrom_parent)-1):
				index_chrome_2 = index_chrom_parent[0]
			else:
				index_chrome_2 = index_chrom_parent[i_parent+1]

			#melakukan cut-point
			cut_point = posisi_CO[i_parent]
			for p in range(len(new_chrom[index_chrome_1])):
				# looping berdasarkan generasi
				if(p >= posisi_CO[i_parent]):
					off_spring[i_parent][p] = new_chrom[index_chrome_2][p]
				else:
					off_spring[i_parent][p] = new_chrom[index_chrome_1][p]

		for x in range(len(off_spring)):
			new_chrom[index_chrom_parent[x]] = off_spring[x]

		# 6. MUTASI
		total_gen = len(chrom) * len(chrom[0])
		jumlah_mutasi = self.mutasi_rate * total_gen
		jumlah_mutasi = int(jumlah_mutasi)

		random_i_mutasi = np.random.randint(low=0, high=total_gen, size=jumlah_mutasi)

		for x in range(len(random_i_mutasi)):
			index_mutasi = random_i_mutasi[x]
			banyak_kromosom = len(chrom)
			banyak_gen = len(chrom[0])
			random_value = random.randint(self.nilai_per_gen['min'], self.nilai_per_gen['max'])

			if(index_mutasi <= banyak_gen):
				new_chrom[0][index_mutasi-1]
			else:
				pos_y = index_mutasi/banyak_gen
				pos_y = int(pos_y)
				pos_x = index_mutasi % banyak_gen
				new_chrom[pos_y][pos_x] = random_value

		return new_chrom

	def process_now(self):
			chromosome_current = self.first_chromosome
			for generasi in range(0, self.total_generasi):
				if(self.stop != True):
					chromosome_current = self.evaluasi_chrom(chromosome_current, generasi)

			print("Selesai, chromosome tertinggi adalah:")
			print(self.next_gen)

run = algoritma_genetika()
run.process_now()
