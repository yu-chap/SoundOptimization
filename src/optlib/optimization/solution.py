import wave
from abc import ABC, abstractmethod
from typing import List

import numpy as np
from nptyping import NDArray

from ..dataformat.binaryfloatconverter import IBytes


class Solution:
    """解のデータ構造を表現するクラス。

    Attributes:
        var (NDArray): 解の変数
        obj (NDArray): 解の評価値
    """

    def __init__(self, var: NDArray, obj: NDArray):
        """
        Attributes:
            var (NDArray): 解の変数
            obj (NDArray): 解の評価値
        """
        self.var: NDArray = var
        self.obj: NDArray = obj


def make_vars(pop: List[Solution]) -> NDArray:
    """解のリストから各解の変数を抽出する。

    Args:
        pop: 解のリスト

    Returns:
        解の変数のリスト

    """
    return np.array([p.var for p in pop])


def make_objs(pop: List[Solution]) -> NDArray:
    """解のリストから各解の評価値を抽出する。

    Args:
        pop: 解のリスト

    Returns:
        解の評価値のリスト
    """
    return np.array([p.obj for p in pop])


class ISolutionWriter(ABC):
    """
    解を保存するための抽象基底クラス。
    全てのsolution writerはこのクラスを継承すること。
    """

    @abstractmethod
    def save_solution(self, sol: Solution, file_path: str) -> None:
        """解を保存します。

        解を保存するための抽象メソッド。
        具体的な保存処理は子クラスでこのメソッドを実装すること。

        Args:
            sol: 保存する解
            file_path: 保存するファイルパス
        """
        raise NotImplementedError()


class Wave(ISolutionWriter):
    """waveフォーマットで解を保存するクラス。

    Attributes:
        channels (int): チャンネル数
        sample_width (int): サンプル幅
        frame_rate (int): フレームレート
        byte_type (IBytes): バイトの型
    """

    def __init__(self, channels: int, sample_width: int, frame_rate: int, byte_type: IBytes):
        """
        Attributes:
            channels: チャンネル数
            sample_width: サンプル幅
            frame_rate: フレームレート
            byte_type: バイトの型
        """
        self.channels: int = channels
        self.sample_width: int = sample_width
        self.frame_rate: int = frame_rate
        self.byte_type: IBytes = byte_type

    def save_solution(self, sol: Solution, file_path: str) -> None:
        """解をwaveフォーマットで保存します。

        Args:
            sol: 保存する解
            file_path: 保存するファイルパス
        """
        with wave.open(file_path, "wb") as wr:
            wr.setnchannels(self.channels)
            wr.setsampwidth(self.sample_width)
            wr.setframerate(self.frame_rate)
            frames = self.byte_type.float2binary(sol.var)
            wr.writeframes(frames)
