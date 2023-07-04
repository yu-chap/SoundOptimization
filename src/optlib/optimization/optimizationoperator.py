import random
from abc import ABC, abstractmethod
from typing import List

import numpy as np

from .solution import Solution, make_vars


class IOperator(ABC):
    """
    遺伝的演算子を定義する抽象基底クラス。
    全てのoperatorはこのクラスを継承すること。
    """

    @abstractmethod
    def evolve(self, pop: List[Solution]) -> List[Solution]:
        """入力された解集団を進化させます。

        入力された解集団を進化させるための抽象メソッド。
        具体的な進化処理は子クラスでこのメソッドを実装すること。

        Args:
            pop: 解のリスト

        Returns:
            進化後の解のリスト
        """
        raise NotImplementedError()


class OperatorDE(IOperator):
    """差分進化(DE)演算子を実装するクラス。

    Attributes:
        CR (float): 交叉率
        F (float): スケーリング係数
    """

    def __init__(self, CR: float, F: float):
        """
        Args:
            CR: 交叉率
            F: スケーリング係数
        """
        self.CR: float = CR
        self.F: float = F

    def evolve(self, pop: List[Solution]) -> List[Solution]:
        """集団を差分進化させます。

        Args:
            pop: 解のリスト

        Returns:
            進化後の解のリスト
        """
        parent_vars = make_vars(pop)
        n, d = np.shape(parent_vars)

        offspring_vars = np.zeros((n, d))
        offsprings = []
        sample_range = list(range(n))

        for i in range(n):
            # ランダムに選択されたr1, r2, r3を用いて差分ベクトルを生成。
            # （r1, r2, r3には自分自身を採用しません。）
            sample_range.remove(i)
            r1, r2, r3 = random.sample(sample_range, 3)
            sample_range.append(i)
            mutant_vector = (parent_vars[r3]
                             + self.F
                             * (parent_vars[r1] - parent_vars[r2]))
            # ランダムに選択された突然変異点と交叉点を差分ベクトルで更新し新しい個体を作成。
            mutation_point = random.sample(range(d), 1)
            mu_index = np.random.rand(d) < self.CR
            mu_index[mutation_point] = True
            offspring_vars[i, mu_index] = mutant_vector[mu_index]
            offsprings.append(Solution(offspring_vars[i, :], pop[i].obj))

        return offsprings


class OperatorIDESO(IOperator):
    """音声最適化のための対話型差分進化(IDE)を実装するクラス。

    Attributes:
        F (float): スケーリング係数
    """

    def __init__(self, F: float):
        """
        Args:
            F: スケーリング係数
        """
        self.F: float = F

    def evolve(self, pop: List[Solution]) -> List[Solution]:
        """対話型進化差分進化(IDE)により集団を進化させます。

        Args:
            pop: 解のリスト

        Returns:
            進化後の解のリスト
        """
        parent_vars = make_vars(pop)
        n, d = np.shape(parent_vars)

        offspring_vars = np.zeros((n, d))
        offsprings = []
        sample_range = list(range(n))

        for i in range(n):
            # ランダムに選択されたr1, r2, r3を用いて差分ベクトルを生成。
            # （r1, r2, r3には自分自身を採用しません。）
            sample_range.remove(i)
            r1, r2, r3 = random.sample(sample_range, 3)
            sample_range.append(i)
            mutant_vector = (parent_vars[r3]
                             + self.F
                             * (parent_vars[r1] - parent_vars[r2]))
            # 音声変数（決定変数）は簡単に制約領域を逸脱してしまうため、
            # 最小値と最大値から差分ベクトルを生成する。
            min_vector = np.min([parent_vars[i, :], mutant_vector], axis=0)
            max_vector = np.max([parent_vars[i, :], mutant_vector], axis=0)
            offspring_vars[i, :] = (min_vector
                                    + random.random()
                                    * (max_vector - min_vector))
            # 生成した差分ベクトルを用いて新しい個体を作成する。
            offsprings.append(Solution(offspring_vars[i, :], pop[i].obj))

        return offsprings
