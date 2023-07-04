from abc import ABC, abstractmethod
from typing import List

import numpy as np

from .solution import ISolutionWriter, Solution, make_objs


class ISelector(ABC):
    """
    解選択を記述するための抽象基底クラス。
    全てのselectorはこのクラスを継承すること。
    """

    @abstractmethod
    def select(
            self,
            parents: List[Solution],
            offsprings: List[Solution]
    ) -> List[Solution]:
        """親と子から次世代の解を選択する。

        次世代の解を選択するための抽象メソッド。
        具体的な選択処理は子クラスでこのメソッドを実装すること。

        Args:
            parents: 親世代の解集団
            offsprings: 子世代の解集団

        Returns:
            次世代の解集団
        """
        raise NotImplementedError()


class MinSelector(ISelector):
    """最小値最適化問題の解を選択するクラス。"""

    def __init__(self):
        pass

    def select(
            self,
            parents: List[Solution],
            offsprings: List[Solution]
    ) -> List[Solution]:
        """親と子から評価値が最小の解を選択する。

        Args:
            parents: 親世代の解集団
            offsprings: 子世代の解集団

        Returns:
            次世代の解集団
        """
        replace_index = np.where(make_objs(parents) > make_objs(offsprings))[0]
        for i in replace_index:
            parents[i] = Solution(offsprings[i].var, offsprings[i].obj)
        return parents


class SOSelector(ISelector):
    """ユーザーの判断に基づいて解（音声）を選択するクラス。

    Attributes:
        writer (ISolutionWriter): 解を保存するためのwriter
        base_file_path (str): 解を保存するファイルパス
    """

    def __init__(self, writer: ISolutionWriter, base_file_path: str):
        """
        Attributes:
            writer: 解を保存するためのwriter
            base_file_path: 解を保存するファイルパス
        """
        self.writer: ISolutionWriter = writer
        self.base_file_path: str = base_file_path

    def select(
            self,
            parents: List[Solution],
            offsprings: List[Solution]
    ) -> List[Solution]:
        """ユーザーの判断に基づいて親と子から解を選択する。

        各親と子の解を一つずつ保存し、ユーザーによってその音を評価してもらう。
        評価方法は1か0を入力してもらうことで行う。（0 -> parent, 1 -> offspring）

        Args:
            parents: 親世代の解集団
            offsprings: 子世代の解集団

        Returns:
            次世代の解集団
        """
        next_pop = []
        for parent, offspring in zip(parents, offsprings):
            save_path = f"{self.base_file_path}parent.wav"
            self.writer.save_solution(parent, save_path)
            save_path = f"{self.base_file_path}offspring.wav"
            self.writer.save_solution(offspring, save_path)

            while True:
                print(
                    "Which is better for you, parent or offspring? 0: parent, 1: offspring."
                )
                cmd = input("Please input -> ")

                if cmd == "0":
                    next_pop.append(parent)
                    break
                if cmd == "1":
                    next_pop.append(offspring)
                    break

                print(f"Please input 1 or 0. You inputted {cmd}.")

        return next_pop
