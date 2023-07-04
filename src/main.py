import os

from optlib.dataformat.binaryfloatconverter import TwoBytes
from optlib.optimization.optimizationoperator import OperatorIDESO
from optlib.optimization.optimizer import SoundOptimizer
from optlib.optimization.problem import SoundOptimizationProblem
from optlib.optimization.selector import SOSelector
from optlib.optimization.solution import Wave

# 最適化探索で生成する個体数
POP_SIZE: int = 5
# 最適化アルゴリズムのパラメータ scale factor F
F: float = 1.0
# 音声のチャンネル数
CH: int = 2
# 音声のサンプリング周波数
SAMPLE_WIDTH: int = 2
# 音声のフレームレート
FR: int = 44100

# 最適化する音声ファイル一覧
SOUND_FILES = [
    "./data/original/cricket.wav",
    "./data/original/glassland1.wav",
    "./data/original/springwater1.wav",
    "./data/original/summer_beach1.wav",
    "./data/original/summer_hill1.wav",
]


def main():
    # 最適化に必要なパラメータを初期化します。
    byte_type = TwoBytes()
    operator = OperatorIDESO(F=F)
    problem = SoundOptimizationProblem(
        n=POP_SIZE,
        sound_files=SOUND_FILES,
        byte_type=byte_type
    )
    writer = Wave(
        channels=CH,
        sample_width=SAMPLE_WIDTH,
        frame_rate=FR,
        byte_type=byte_type
    )
    selector = SOSelector(
        writer=writer,
        base_file_path="./data/evaluation/"
    )
    optimizer = SoundOptimizer(
        problem=problem,
        operator=operator,
        selector=selector
    )

    print("Start sound optimization.")
    optimizer.run()

    # 最適化によって得られた解を保存します。また、その保存場所を出力します。
    result_writer = Wave(
        channels=CH,
        sample_width=SAMPLE_WIDTH,
        frame_rate=FR,
        byte_type=byte_type
    )

    base_save_path = "./data/result"
    for i, p in enumerate(optimizer.result):
        save_path = f"{base_save_path}/pop{i + 1}.wav"
        result_writer.save_solution(sol=p, file_path=save_path)
    save_abs_path = os.path.abspath(base_save_path)
    print(f"The final result was saved in {save_abs_path}.")

    print("Terminate sound optimization.")


if __name__ == "__main__":
    main()
