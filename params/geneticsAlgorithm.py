from abc import ABCMeta, abstractmethod
import random
import itertools
import copy

# 遺伝的アルゴリズムを実装するための抽象クラス
# このクラスを継承して実際に学習させる

# 1つの個体
class Chromosome(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def randomGen(cls):
        # ランダムに1つの個体を生成する。
        # 0世代の生成に使用
        pass

    @abstractmethod
    def fitness(self):
        # 適応度の計算
        # 適応度が高いほど優秀な個体である。
        pass 

    @abstractmethod
    def crossOver(self, other):
        # selfとotheを交叉させて、新しい個体を作る。
        pass 

    @abstractmethod
    def mutation(self):
        # selfを突然変異させる。
        pass


# 遺伝的アルゴリズム自体を行うclass
class GeneticsAlgorithm():
    def __init__(self, n:int, g:int, probCrossOver:float, probMutation:float, generation0):
        assert n == len(generation0)
        assert probCrossOver + probMutation <= 1
        self.n = n
        self.g = g 
        self.probCrossOver = probCrossOver
        self.probMutaion = probMutation
        self.probCopy = 1 - probCrossOver - probMutation
        self.population = generation0
        self.fitness = [0 for _ in range(n)]
        self.cumFitness = [0 for _ in range(n)]
    
    def _CalcFitness(self):
        self.fitness = list(map(lambda x : x.fitness(), self.population))
        self.cumFitness = list(itertools.accumulate(self.fitness))
    
    # ルーレット選択
    # 適応度に比例して個体を選ぶ。
    # 適応度が負になる場合は使えない
    def _RouletteSelection(self):
        fitnessSum = sum(self.fitness)
        prob = random.uniform(0, fitnessSum)
        for i in range(self.n):
            if self.cumFitness[i] > prob:
                return self.population[i]
        assert False

    # トーナメント選択
    # ある一定の集合のサイズを取り出してその中で適応度が高いものを選ぶ
    def _TournamentSelection(self):
        indexSample = random.sample(range(self.n), 3)
        fitnessMax = -1e9
        indexMax = -1
        for i in indexSample:
            if self.fitness[i] > fitnessMax:
                fitnessMax = self.fitness[i]
                indexMax = i
        return self.population[indexMax]
    
    # 選択する関数
    def _Selection(self):
        # return self._RouletteSelection()
        return self._TournamentSelection()
    
    # エリート選択
    # 一番適応値が高い個体はそのまま残す。
    def _Elite(self):
        fitnessMax = -1e9
        index = -1
        for i, fit in enumerate(self.fitness):
            if fit > fitnessMax:
                fitnessMax = fit 
                index = i
        return self.population[index]

    def _NextGeneration(self):

        # 適応度の計算
        self._CalcFitness()

        # エリート選択
        nextGeneration = [self._Elite()]

        while len(nextGeneration) < self.n:
            prob = random.random()
            if prob <= self.probCrossOver:
                individual1 = self._Selection()
                individual2 = self._Selection()
                newIndividual1, newIndividual2 = individual1.crossOver(individual2)
                nextGeneration.append(newIndividual1)
                nextGeneration.append(newIndividual2)
            elif prob <= self.probCrossOver + self.probCopy:
                newIndividual = self._Selection()
                nextGeneration.append(newIndividual)
            else:
                individual = self._Selection()
                newIndividual = individual.mutation()
                nextGeneration.append(newIndividual)

        return nextGeneration
        
    def Optimize(self):

        for _ in range(self.g):
            self.population = self._NextGeneration()
            print(f"elite = {self.population[0]}")

        return self._Elite()
        



    
