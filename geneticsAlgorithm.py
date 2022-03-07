from lib import *
from params.eval import *
from abc import ABCMeta, abstractmethod
import random
import itertools
import simulator
import decisionMaker
import evaluator

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
        return self.population[index], fitnessMax

    def _NextGeneration(self):

        # 適応度の計算
        self._CalcFitness()

        # エリート選択
        elite, fitnessMax = self._Elite()
        nextGeneration = [elite]

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

        return nextGeneration, fitnessMax
        
    def Optimize(self):

        for _ in range(self.g):
            self.population, fitnessMax = self._NextGeneration()
            print(f"param = {self.population[0]}")
            print(f"best = {fitnessMax}")

        return self._Elite()
        

class TetrisParam(Chromosome):
    def __init__(self, 
                 eval_height, 
                 eval_roughness, 
                 eval_blank_under_block,
                 eval_single,
                 eval_double,
                 eval_triple,
                 eval_tetris,
                 eval_t_spin_single,
                 eval_t_spin_double,
                 eval_t_spin_triple,
                 eval_t_spin_mini_single,
                 eval_t_spin_mini_double ):
        self.eval_height = eval_height 
        self.eval_roughness = eval_roughness
        self.eval_blank_under_block = eval_blank_under_block
        self.eval_single = eval_single
        self.eval_double = eval_double 
        self.eval_triple = eval_triple 
        self.eval_tetris = eval_tetris 
        self.eval_t_spin_single = eval_t_spin_single
        self.eval_t_spin_double = eval_t_spin_double 
        self.eval_t_spin_triple = eval_t_spin_triple 
        self.eval_t_spin_mini_single = eval_t_spin_mini_single
        self.eval_t_spin_mini_double = eval_t_spin_mini_double
    
    @classmethod
    def randomGen(cls):
        return cls(
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000)
        )
        

    def fitness(self):
        # simulation

        board = Board()
        board.followingMinos = [simulator.GenerateMino() for _ in range(FOLLOWING_MINOS_COUNT)]

        # パラメタの設定
        # todo: ランダムすぎてすぐゲームオーバーするのをなんとかする
        board.evalParam = Evalparam(
            [0, self.eval_single, self.eval_double, self.eval_triple, self.eval_tetris],
            self.eval_height, 
            self.eval_roughness, 
            self.eval_blank_under_block, 
            self.eval_t_spin_single,
            self.eval_t_spin_double,
            self.eval_t_spin_triple,
            self.eval_t_spin_mini_single,
            self.eval_t_spin_mini_double
        )

        for _ in range(60):
            assert type(board.score) == int
            addedMino = simulator.GenerateMino()
            board = simulator.AddFollowingMino(board, addedMino)

            # 思考ルーチン
            value, mino, path = decisionMaker.Decide(board)

            # ミノを動かしてラインを消す
            isTspin = evaluator.IsTSpin(board.mainBoard, mino, path)
            isTspinmini = evaluator.IsTSpinMini(board.mainBoard, mino, path)
            joinedMainBoard, joinedTopRowIdx = JoinDirectedMinoToBoard(mino, board.mainBoard, board.topRowIdx)
            newMainBoard, newTopRowIdx, clearedRowCount = ClearLines(joinedMainBoard, joinedTopRowIdx)

            # スコアの計算
            scoreAdd, backToBack, ren = evaluator.Score(isTspin, isTspinmini, clearedRowCount, board.backToBack, board.ren)

            board = Board(
                newMainBoard,
                None,
                board.followingMinos,
                board.holdMino,
                True,
                newTopRowIdx,
                board.score + scoreAdd,
                backToBack,
                ren,
                board.evalParam
            )

        return board.score
    
    def crossOver(self, other):
        eval_height             = self.eval_height if random.random() < 0.5 else other.eval_height
        eval_roughness          = self.eval_roughness if random.random() < 0.5 else other.eval_roughness
        eval_blank_under_block  = self.eval_blank_under_block if random.random() < 0.5 else other.eval_blank_under_block
        eval_single             = self.eval_single if random.ranndom() < 0.5 else other.eval_single
        eval_double             = self.eval_double if random.random() < 0.5 else other.eval_double
        eval_triple             = self.eval_triple if random.random() < 0.5 else other.eval_triple
        eval_tetris             = self.eval_tetris if random.random() < 0.5 else other.eval_tetris
        eval_t_spin_single      = self.eval_t_spin_single if random.random() < 0.5 else other.eval_t_spin_single
        eval_t_spin_double      = self.eval_t_spin_double if random.random() < 0.5 else other.eval_t_spin_double
        eval_t_spin_triple      = self.eval_t_spin_triple if random.random() < 0.5 else other.eval_t_spin_triple
        eval_t_spin_mini_single = self.eval_t_spin_mini_single if random.random() < 0.5 else other.eval_t_spin_mini_single
        eval_t_spin_mini_double = self.eval_t_spin_mini_double if random.random() < 0.5 else other.eval_t_spin_mini_double
        return TetrisParam(
            eval_height, 
            eval_roughness, 
            eval_blank_under_block,
            eval_single,
            eval_double,
            eval_triple,
            eval_tetris,
            eval_t_spin_single,
            eval_t_spin_double,
            eval_t_spin_triple,
            eval_t_spin_mini_single,
            eval_t_spin_mini_double 
        )

    def mutation(self):
        eval_height             = self.eval_height if random.random() < 0.5 else self.eval_height + random.randint(-100,100)
        eval_roughness          = self.eval_roughness if random.random() < 0.5 else self.eval_roughness + random.randint(-100,100)
        eval_blank_under_block  = self.eval_blank_under_block if random.random() < 0.5 else self.eval_blank_under_block + random.randint(-100,100)
        eval_single             = self.eval_single if random.ranndom() < 0.5 else self.eval_single + random.randint(-100,100)
        eval_double             = self.eval_double if random.random() < 0.5 else self.eval_double + random.randint(-100,100)
        eval_triple             = self.eval_triple if random.random() < 0.5 else self.eval_triple + random.randint(-100,100)
        eval_tetris             = self.eval_tetris if random.random() < 0.5 else self.eval_tetris + random.randint(-100,100)
        eval_t_spin_single      = self.eval_t_spin_single if random.random() < 0.5 else self.eval_t_spin_single + random.randint(-100,100)
        eval_t_spin_double      = self.eval_t_spin_double if random.random() < 0.5 else self.eval_t_spin_double + random.randint(-100,100)
        eval_t_spin_triple      = self.eval_t_spin_triple if random.random() < 0.5 else self.eval_t_spin_triple + random.randint(-100,100)
        eval_t_spin_mini_single = self.eval_t_spin_mini_single if random.random() < 0.5 else self.eval_t_spin_mini_single + random.randint(-100,100)
        eval_t_spin_mini_double = self.eval_t_spin_mini_double if random.random() < 0.5 else self.eval_t_spin_mini_double + random.randint(-100,100)
        return TetrisParam(
            eval_height, 
            eval_roughness, 
            eval_blank_under_block,
            eval_single,
            eval_double,
            eval_triple,
            eval_tetris,
            eval_t_spin_single,
            eval_t_spin_double,
            eval_t_spin_triple,
            eval_t_spin_mini_single,
            eval_t_spin_mini_double 
        )
    
    # Logを取るときに必要
    def __str__(self):
        tostr = f"EVAL_HEIGHT = {self.eval_height}\n" \
                f"EVAL_ROUGHNESS = {self.eval_roughness}\n" \
                f"EVAL_BLANK_UNDER_BLOCK = {self.eval_blank_under_block}\n" \
                f"EVAL_SINGLE = {self.eval_single}\n" \
                f"EVAL_DOUBLE = {self.eval_double}\n" \
                f"EVAL_TRIPLE = {self.eval_triple}\n" \
                f"EVAL_TETRIS = {self.eval_tetris}\n" \
                f"EVAL_T_SPIN_SINGLE = {self.eval_t_spin_single}\n" \
                f"EVAL_T_SPIN_DOUBLE = {self.eval_t_spin_double}\n" \
                f"EVAL_T_SPIN_TRIPLE = {self.eval_t_spin_triple}\n" \
                f"EVAL_T_SPIN_MINI_SINGLE = {self.eval_t_spin_mini_single}\n" \
                f"EVAL_T_SPIN_MINI_DOUBLE = {self.eval_t_spin_mini_double}\n"
        
        return tostr

    
