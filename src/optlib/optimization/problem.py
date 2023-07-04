import wave
from abc import ABC, abstractmethod
from typing import List

import numpy as np
from nptyping import NDArray

from .solution import Solution
from ..dataformat.binaryfloatconverter import IBytes


class Problem(ABC):
    """
    最適化問題の抽象基底クラス。
    全てのProblemはこのクラスを継承すること。
    """

    @abstractmethod
    def initialize(self) -> List[Solution]:
        """初期集団を生成します。

        初期集団を生成するための抽象メソッド。
        具体的な生成処理は子クラスでこのメソッドを実装すること。

        Returns:
            初期集団
        """
        raise NotImplementedError()

    @abstractmethod
    def is_terminated(self) -> bool:
        """最適化が終了したかどうかを判定します。

        最適化が終了したかどうかを判定するための抽象メソッド。
        具体的な判定処理は子クラスでこのメソッドを実装すること。

        Returns:
            最適化が終了した場合はTrue、それ以外の場合はFalse
        """
        raise NotImplementedError()


class EquationProblem(Problem, ABC):
    """
    数式で定式化可能な最適化問題の抽象基底クラス。
    全てのEquationProblemはこのクラスを継承すること。
    """

    @abstractmethod
    def evaluate(self, sol: Solution) -> Solution:
        """個体の評価を行います。

        個体を評価するための抽象メソッド。
        具体的な評価処理は子クラスでこのメソッドを実装すること。

        Args:
            sol: 評価する個体

        Returns:
            評価後の個体
        """
        raise NotImplementedError()

    @abstractmethod
    def evaluate_all(self, pop: List[Solution]) -> List[Solution]:
        """解集団全体の評価を行います。

        解集団全体を評価するための抽象メソッド。
        具体的な評価処理は子クラスでこのメソッドを実装すること。

        Args:
            pop: 評価する解集団

        Returns:
            評価後の解集団
        """
        raise NotImplementedError()


class Sphere(EquationProblem):
    """Sphere関数による最適化問題を表すクラス。

    Attributes:
        n (int): 集団のサイズ
        m (int): 目的関数の数
        d (int): 解の次元数
        fe (int): 現在の評価回数
        max_fe (int): 最大評価回数
        lower (NDArray): 探索範囲の最小値制約
        upper (NDArray): 探索範囲の最大値制約
    """

    def __init__(self, n: int, m: int, d: int, max_fe: int):
        """
        Args:
            n: 集団のサイズ
            m: 目的関数の数
            d: 解の次元数
            max_fe: 最大評価回数
        """
        self.n: int = n
        self.m: int = m
        self.d: int = d
        self.fe: int = 0
        self.max_fe: int = max_fe
        self.lower: NDArray = np.zeros(self.d) - 100
        self.upper: NDArray = np.zeros(self.d) + 100

    def initialize(self) -> List[Solution]:
        """Sphere関数の初期集団を生成します。

        Returns:
            初期集団
        """
        vars_ = np.random.uniform(self.lower[0], self.upper[0], (self.n, self.d))
        pop = [Solution(var, np.zeros(self.m)) for var in vars_]
        pop = self.evaluate_all(pop)
        return pop

    def evaluate(self, sol: Solution) -> Solution:
        """個体の評価を行います。

        返却値はx1^2 + x2^2 + ... + xd^2で計算された値。

        Args:
            sol: 評価する個体

        Returns:
            評価後の個体
        """
        obj = np.sum(np.square(sol.var))
        return Solution(sol.var, obj)

    def evaluate_all(self, pop: List[Solution]) -> List[Solution]:
        """解集団全体の評価を行います。

        Args:
            pop: 評価する解集団

        Returns:
            評価後の解集団
        """
        pop = [self.evaluate(p) for p in pop]
        self.fe += len(pop)
        return pop

    def is_terminated(self) -> bool:
        """最適化が終了したかどうかを判定します。

        Returns:
            最適化が終了した場合はTrue、それ以外の場合はFalse
        """
        return self.max_fe < self.fe


class SoundOptimizationProblem(Problem):
    """音声の最適化問題を表すクラス。

    Attributes:
        n (int): 集団のサイズ
        sound_files (List[str]): 最適化対象の音声ファイルのリスト
        byte_type (IBytes): 音声ファイルのバイト形式
    """

    def __init__(self, n: int, sound_files: List[str], byte_type: IBytes):
        """
        Args:
            n: 集団のサイズ
            sound_files: 最適化対象の音声ファイルのリスト
            byte_type: 音声ファイルのバイト形式
        """
        self.n: int = n
        self.sound_files: List[str] = sound_files
        self.byte_type: IBytes = byte_type

    def initialize(self) -> List[Solution]:
        """音声の最適化問題の初期集団を生成します。

        探索を行う初期集団を生成するために、最適化する音声ファイルから音声データを取得しデータの整形を行う。
        整形されたデータをSolutionとして保持しそのリストを返却する。

        Returns:
            初期集団
        """
        pop = []
        for file_path in self.sound_files:
            with wave.open(file_path, "rb") as wr:
                fn = wr.getnframes()
                frames = wr.readframes(fn)
                var = self.byte_type.binary2float(frames)
                sol = Solution(var, np.nan)
                pop.append(sol)

        return pop

    def is_terminated(self) -> bool:
        """最適化が終了したかどうかを判定します。

        最適化が終了したかどうかをユーザーに尋ねることで判定します。
        終了判定はユーザーに1か0を入力させることで行います。(1 -> 最適化継続。0 -> 終了。)

        Returns:
            最適化が終了する場合はTrue、それ以外の場合はFalse。
        """
        while True:
            print("Please input 1 to proceed with optimization or 0 to terminate.")
            is_termination = input("-> ")

            # 1か0が入力された場合は、正常動作のため、それぞれに対応する値を返却する。
            if is_termination == "0":
                return True
            if is_termination == "1":
                return False

            # 1と0以外の値が入力された場合は、正常な入力ではないため、再度入力を促す。
            print(f"Please input 1 or 0. You inputted {is_termination}.")
