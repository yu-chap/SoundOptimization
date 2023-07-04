from abc import ABC, abstractmethod
from typing import List, Optional

from .optimizationoperator import IOperator
from .problem import Problem, EquationProblem
from .selector import ISelector
from .solution import Solution


class BaseOptimizer(ABC):
    """
    最適化処理を行うための抽象基底クラス。
    全てのoptimizerはこのクラスを継承すること。

    Attributes:
        result (Optional[List[Solution]]): 最終的に得られた解
    """

    def __init__(self):
        self.result: Optional[List[Solution]] = None

    @abstractmethod
    def run(self) -> None:
        """
        最適化処理を実行するための抽象メソッド。
        具体的な最適化処理は子クラスでこのメソッドを実装すること。
        """
        pass


class BasicOptimizer(BaseOptimizer):
    """基本的な最適化アルゴリズム（進化->評価->選択の原理に従うアルゴリズム）による最適化処理を行うクラス。

    基本的な最適化アルゴリズムの例：
        Genetic algorithm
        Differential evolution
        .etc

    Attributes:
        result (Optional[List[Solution]]): 最終的に得られた解
        problem (EquationProblem): 最適化対象の問題（数式で定義可能な問題）
        operator (IOperator): 進化的操作のための最適化operator
        selector (ISelector): 新たな世代を選択するためのselector
    """

    def __init__(self, problem: EquationProblem, operator: IOperator, selector: ISelector):
        """
        Args:
            problem: 最適化対象の問題（数式で定義可能な問題）
            operator: 進化的操作のための最適化operator
            selector: 新たな世代を選択するためのselector
        """
        super().__init__()
        self.problem: EquationProblem = problem
        self.operator: IOperator = operator
        self.selector: ISelector = selector

    def run(self) -> None:
        """
        最適化処理を実行する。
        問題の初期化から選択までをループで実行する。
        """
        pop = self.problem.initialize()

        while not self.problem.is_terminated():
            offsprings = self.operator.evolve(pop)
            offsprings = self.problem.evaluate_all(offsprings)
            pop = self.selector.select(pop, offsprings)

        self.result = pop


class SoundOptimizer(BaseOptimizer):
    """音声に対する最適化処理を行うクラス。

    Attributes:
        result (Optional[List[Solution]]): 最終的に得られた解
        problem (EquationProblem): 最適化対象の問題
        operator (IOperator): 進化的操作のための最適化operator
        selector (ISelector): 新たな世代を選択するためのselector
        generation (int): 世代数
    """

    def __init__(self, problem: Problem, operator: IOperator, selector: ISelector):
        """
        Args:
            problem: 最適化対象の問題
            operator: 進化的操作のための最適化operator
            selector: 新たな世代を選択するためのselector
        """
        super().__init__()
        self.problem: Problem = problem
        self.operator: IOperator = operator
        self.selector: ISelector = selector
        self.generation: int = 0

    def run(self) -> None:
        """
        最適化処理を実行する。
        人間による評価を行うため、最適化の回数を逐次表示する。
        """
        pop = self.problem.initialize()

        while not self.problem.is_terminated():
            self.generation += 1
            print(f"Execute the {self.generation}-th optimization procedure.")
            offsprings = self.operator.evolve(pop)
            pop = self.selector.select(pop, offsprings)

        self.result = pop
