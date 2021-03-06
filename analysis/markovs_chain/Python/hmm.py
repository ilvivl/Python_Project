import numpy as np
import pandas as pd
import networkx as nx
import math as m
import matplotlib.pyplot as plt
from pprint import pprint 
from urllib.parse import urlparse

# TODO: классовая структура

# Представим, что мы переходим только между тремя веб страницами: web_1, web_2 и web_3. Вообще говороя 
# состояния необходимо делать с более сложно структурой: кроме веб страниц, состояния будут 
# отображать мат ожидание и дисперсиюс корости движения мыши, скорости печати и пр. на данной странице, но 
# в данной тестовой версии мы ипользуем в качестве состояний только название веб страницы.  
# Легко понять, что в модели цепей Маркова веб страницы является явными состоянием, 
# то есть таким состояния, о которых в любой момент времени можно точно сказать, 
# находится ли наблюдаемый объект в нем или нет. В противовес явным существуют скрытые,
# но о них будет скзаано позже. Также стоит заметить, что вообще говоря, такая модель цепи Маркова является 
# не полной из-а того, что в ней подрузамивается, что все параметры являются дискртными6 когда на самом деле
# правильнее было бы считать скорости нормально распределенными случайнми величиными6 но это уже следующий этап


# Матрица переходов между веб страницами -  матрица вероятностей попасть с web_i на web_j
# понятное дело, что сумма вероятностей перейти из состояния web_i во все остальные состояния равняется единице

# Теперь займемся скрытыми состояниями цепи. Скрытыми они называются потому, что мы никогда доподлино не знаем,
# в каком именно стостоянии нахоится пользователь, мы можем только рассуждать о наиболее вероятном состоянии соответсвующему
# пройденному пути

# hidden_states = ['good', 'bad']

# Легко понять, что начальное распределение лучше выбрать равновероятным

# pi = [0.5, 0.5]

# Изначально матрица переходов между скрытыми состояниями также лучше выбрать такой

# a_df = pd.DataFrame(columns=hidden_states, index=hidden_states)
# a_df.loc[hidden_states[0]] = [0.5, 0.5]
# a_df.loc[hidden_states[1]] = [0.5, 0.5]

# print(a_df, "\n\n")

# Создадим теперь матрицу вероятностей наблюдейний, то есть матрицу в которой записаны условные вероятности
# получить наблюдение o_k^ находиться в состоянии i
# Матрица имеет размер (M x Q), где M - число скрытых состояний, а Q - число наблюдений. 

# observable_states = ['o' + str(i) for i in range(100)]

# b_df = pd.DataFrame(columns=observable_states, index=hidden_states)
# b_df.loc[hidden_states[0]] = [0.01 for _ in range(100)]
# b_df.loc[hidden_states[1]] = [0.01 for _ in range(100)]

# print(b_df, "\n\n")

# Последовательность наблюдений поведения пользователя закодируем числами

# observ_map = {'o1':0, 'o2':1, 'o3':2, 'o4':3}
# observ = np.array([1,1,2,1,0,1,2,3,1,30,0,2,2,0,1,0,1,3,3])

class hmm():
	def __init__(self, pi, A, B, delta = 1e-4, states = ['good', 'bad']):
		self.states = states
		self.delta = delta
		self.A = A
		self.B = B
		self.pi = pi
	
	def learn(self, obs, epochs = 1):
		self.epochs = epochs
		self.baum_welch_(obs)

	def forward_(self, obs):

		# Длина последовательности наблюдений
		T = len(obs)

		# Число скрытых состояний
		N = self.A.shape[0]

		self.alpha = np.zeros((T, N))
		self.alpha[0] = self.pi * self.B[ : , obs[0]]

		for t in range(1, T):
			self.alpha[t] = self.alpha[t - 1].dot(self.A) * self.B[ : , obs[t]]

	def backward_(self, obs):

		# Длина последовательности наблюдений
		T = len(obs)

		# Число скрытых состояний
		N = self.A.shape[0]

		self.beta = np.zeros((N, T))
		self.beta[ : , T - 1] = 1

		for t in reversed(range(T - 1)):
			for n in range(N):
				self.beta[n , t] = np.sum(self.beta[ : , t + 1] * self.A[n , : ] * self.B[ : , obs[t + 1]])

	def likelihood_(self, obs):
		self.likelihood = forward_(obs)[-1].sum()    

	def gamma_(self, obs):

		T = len(obs)
		self.gamma = np.multiply(self.alpha, self.beta.T)
		for t in range(T):
			self.gamma[t] = self.gamma[t]/np.sum(self.alpha[t, :] * self.beta[:, t])

	def ksi_(self, obs):
		
		# Число скрытых состояний
		N = self.A.shape[0]

		# Длина последовательности наблюдений 
		T = len(obs)

		self.ksi = np.zeros((T, N, N))

		for t in range(T - 1):
			P = 0
			for i in range(N):
				for j in range(N):
					self.ksi[t, i, j] = self.alpha[t, i] * self.A[i, j] * self.B[j, obs[t + 1]] * self.beta[j, t + 1]
					P += self.ksi[t, i, j]
			self.ksi[t, :, :] /= P
			
		for i in range(N):
			for j in range(N):
				self.ksi[T - 1, i, j] = self.alpha[T - 1, i] * self.A[i, j]
		self.ksi[T - 1, :, :] /= np.sum(self.ksi[T - 1,: ,: ])


	def baum_welch_(self, obs):

		N = self.A.shape[0]
		T = len(obs)
		K = np.shape(self.B)[1]
		A_old = self.A.copy()
		B_old = self.B.copy()
		for _ in range(self.epochs):
			self.forward_(obs)
			self.backward_(obs)
			self.gamma_(obs)
			self.ksi_(obs)
			# self.pi = self.gamma[0]
			for i in range(N):
				self.pi[i] = np.sum(self.ksi[0, i, :])
				# print("ksi", self.ksi, "alpha", self.alpha, "beta", self.beta, "pi", self.pi)

				for j in range(N):
					self.A[i, j] = np.sum(self.ksi[: T - 1, i, j]) / np.sum(self.gamma[: T - 1, i])
				

				for k in range(K):
					s = 0
					for t in range(T):
						if (obs[t] == k):
							s += self.gamma[t, i]
					self.B[i, k] = s / sum(self.gamma[: , i])
			
			error = (np.abs(self.A - A_old)).max() + (np.abs(self.B - B_old)).max() 
			if error < self.delta:
				break


	# Алгоритм Витерби — алгоритм поиска наиболее подходящего списка состояний (называемого путём Витерби), который в контексте цепей Маркова
	# получает наиболее вероятную последовательность произошедших событий. Великолепно написано на https://en.wikipedia.org/wiki/Viterbi_algorithm
	def viterbi(self, obs):

		# Количество состояний
		K = np.shape(self.B)[0]
		
		# Число намблюдений
		T = np.shape(obs)[0]
		
		# Инициализируем путь по состояниям нулями
		path = np.zeros(T)
		T1 = np.zeros((K, T))
		T2 = np.zeros((K, T))
		
		# Начальная инициализация
		T1[:, 0] = self.pi * self.B[:, obs[0]]
		T2[:, 0] = 0
	  
		for i in range(1, T):
			for j in range(K):
				T1[j, i] = np.max(T1[:, i - 1] * self.A[:, j]) * self.B[j, obs[i]] 
				T2[j, i] = np.argmax(T1[:, i - 1] * self.A[:, j])
		
		path[T - 1] = np.argmax(T1[:, T - 1])
		for i in range(T - 2, -1, -1):
			path[i] = T2[int(path[i + 1]), i + 1]
		print("path:", path)
		print("T1 ", T1)
		print("T2 ", T2)
		return path, np.max(T1[:, T - 1])
# df = pd.read_csv('/Users/MaximZubkov/Desktop/Programming/Python/Python_Project/analysis/data/matvei_history.csv', sep = ',')
# # print(df.head())
# val = df.values
# event = []
# for i in range(len(val)):
# 	url = urlparse(val[i][0])
# 	event.append(url.netloc + url.path)
# # print(len(unique))
# indexing = dict()
# i = 0
# for e in event[:-1]:
# 	if e not in indexing.keys():
# 		indexing[e] = i
# 		i += 1
# # print(indexing)
# obs_seq = []
# for web_page in event[:-1]:
# 	obs_seq.append(indexing[web_page])
# # print(obs_seq)
# unique = set(obs_seq)
# print(len(unique))
# constant = m.sqrt(len(unique))
# a = constant * np.array([[0.5, 0.5] , [0.5, 0.5]])
# r_1 = np.random.random(len(unique))
# r_1 = constant * r_1 / np.sum(r_1)
# r_2 = np.random.random(len(unique))
# r_2 = constant * r_2 / np.sum(r_2)
# b = np.array([r_1, r_2])
# pi = constant * np.array([0.1, 0.9])
# a = len(unique) * np.array([[0.5, 0.5] , [0.5, 0.5]]) / 30
# r_1 = np.random.random(len(unique))
# r_1 = len(unique) * r_1 / np.sum(r_1) / 30
# r_2 = np.random.random(len(unique))
# r_2 = len(unique) * r_2 / np.sum(r_2) / 30
# b = np.array([r_1, r_2])
# pi = len(unique) * np.array([0.1, 0.9]) / 30
# url = urlparse(event['current_page'])
# event['current_page'] = url.netloc + url.path
# pages = [urlparse()]

# a = a_df.values
# b = b_df.values

# HMM = hmm(hidden_states, pi, a, b)
# HMM.viterbi(observ
# np.seterr(all='ignore')
# HMM = hmm(pi, a, b)

# HMM.learn(obs_seq)
# print("A:\n", HMM.A)
# print("B:\n",HMM.B)
# print("pi:\n",HMM.pi)

# a = a_df.values
# b = b_df.values

# HMM = hmm(hidden_states, pi, a, b)
# HMM.viterbi(observ)

# HMM = hmm(hidden_states, pi, a, b)
# HMM.learn(observ)
# print("A:\n", HMM.A)
# print("B:\n",HMM.B)
# print("pi:\n",HMM.pi)