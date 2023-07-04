from abc import ABC, abstractmethod

import numpy as np
from nptyping import NDArray


class IBytes(ABC):
    """
    バイト操作を定義する抽象基底クラス。
    全てのconverterはこのクラスを継承すること。
    """

    @abstractmethod
    def float2binary(self, data: NDArray) -> bytes:
        """浮動小数点数データをバイナリデータに変換します。

        浮動小数点数データをバイナリデータに変換するための抽象メソッド。
        具体的な変換処理は子クラスでこのメソッドを実装すること。

        Args:
            data: 変換する浮動小数点数データ

        Returns:
            変換されたバイナリデータ
        """
        raise NotImplementedError()

    @abstractmethod
    def binary2float(self, frames: bytes) -> NDArray:
        """バイナリデータを浮動小数点数データに変換します。

        バイナリデータを浮動小数点数データに変換するための抽象メソッド。
        具体的な変換処理は子クラスでこのメソッドを実装すること。

        Args:
            frames: 変換するバイナリデータ

        Returns:
            変換された浮動小数点数データ
        """
        raise NotImplementedError()


class TwoBytes(IBytes):
    """2バイトに対するバイト操作を行うクラス。"""

    def __init__(self):
        pass

    def float2binary(self, data: NDArray) -> bytes:
        """浮動小数点数データを2バイトのバイナリデータに変換します。

        Args:
            data: 変換する浮動小数点数データ

        Returns:
            変換された2バイトのバイナリデータ
        """
        data = _normalize_float2binary(data=data, byte_size=2)
        return data.astype(np.int16).tobytes()

    def binary2float(self, frames: bytes) -> NDArray:
        """2バイトのバイナリデータを浮動小数点数データに変換します。

        Args:
            frames: 変換する2バイトのバイナリデータ

        Returns:
            変換された浮動小数点数データ
        """
        data = np.frombuffer(frames, dtype=np.int16)
        data = _normalize_binary2float(data=data, byte_size=2)
        return data


class FourBytes(IBytes):
    """4バイトに対するバイト操作を行うクラス。"""

    def __init__(self):
        pass

    def float2binary(self, data: NDArray) -> bytes:
        """浮動小数点数データを4バイトのバイナリデータに変換します。

        Args:
            data: 変換する浮動小数点数データ

        Returns:
            変換された4バイトのバイナリデータ
        """
        data = _normalize_float2binary(data=data, byte_size=4)
        return data.astype(np.int32).tobytes()

    def binary2float(self, frames: bytes) -> NDArray:
        """4バイトのバイナリデータを浮動小数点数データに変換します。

        Args:
            frames: 変換する4バイトのバイナリデータ

        Returns:
            変換された浮動小数点数データ
        """
        data = np.frombuffer(frames, dtype=np.int32)
        data = _normalize_binary2float(data=data, byte_size=4)
        return data


def create_converter(converter_name: str) -> IBytes:
    """指定されたconverter名に基づいてconverterオブジェクトを返却します。

    Args:
        converter_name: converterの名前（有効な名前："TwoBytes", "FourBytes"）

    Returns:
        作成されたconverterオブジェクト

    Raises:
        ValueError: 無効な値が入力された場合に発生します。
    """
    if converter_name == "TwoBytes":
        return TwoBytes()
    elif converter_name == "FourBytes":
        return FourBytes()
    else:
        raise ValueError(f"An invalid value was entered. The entered value was [{converter_name}].")


def _normalize_float2binary(data: NDArray, byte_size: int) -> NDArray:
    """浮動小数点数データを正規化してバイナリデータに変換します。

    Args:
        data: 変換する浮動小数点数データ
        byte_size: バイトサイズ

    Returns:
        変換されたバイナリデータ
    """
    return (data * (2 ** (8 * byte_size - 1) - 1)).reshape(data.size, 1)


def _normalize_binary2float(data: NDArray, byte_size: int) -> NDArray:
    """バイナリデータを浮動小数点数データに変換して正規化します。

    Args:
        data: 変換するバイナリデータ
        byte_size: バイトサイズ

    Returns:
        変換された浮動小数点数データ
    """
    return data.astype(float) / (2 ** (8 * byte_size - 1))
