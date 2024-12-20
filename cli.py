"""コマンドラインで勝率を計算する。"""

import argparse

from src import prob

# ruff: noqa: T201


class Cli:
    """コマンドラインインターフェース。

    Attributes:
        args (argparse.Namespace): コマンドライン引数。
    """

    def __init__(self) -> None:
        """初期化。"""
        self.parse_args()

    def parse_args(self) -> None:
        """コマンドライン引数をパースして返す。"""
        parser = argparse.ArgumentParser(description="Calculate the probability of winning.")
        parser.add_argument("-n", "-g", "--goal", type=int, default=30, help="The number of goals.")
        parser.add_argument("--fraction", action="store_true", help="Output as a fraction.")
        self.args = parser.parse_args()

    def run(self) -> None:
        """対話で勝数と負数を入力して勝率を計算する。

        入力はスペース区切りで、勝数と負数を入力する。
        または、 w と l を入力して勝負を追加する。

        Examples:
            $ python -m src.cli
            > 10 5
            0.65625
            > l


        """
        win = 0
        lose = 0
        while True:
            try:
                line = input("> ")
                if line == "l":
                    lose += 1
                elif line == "w":
                    win += 1
                else:
                    wi, lo = map(int, line.split())
                    win = wi
                    lose = lo
                self.prob(win, lose)
            except ValueError:
                print("Invalid input.")
            except EOFError:
                break
            except KeyboardInterrupt:
                break

    def prob(self, win: int, lose: int) -> None:
        """勝数と負数から勝率を計算して出力する。"""
        p = prob(win, lose, self.args.goal)
        if self.args.fraction:
            print(f"[{win:>2d}-{lose:<2d}] {p}")
        print(f"[{win:>2d}-{lose:<2d}] {p.float()}")


if __name__ == "__main__":
    Cli().run()
