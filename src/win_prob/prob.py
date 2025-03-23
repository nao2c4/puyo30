"""確率を計算するモジュール。"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from typing import Self


@dataclass(frozen=True, slots=True)
class Expr:
    """式を表すクラス。

    p = 1/2 でテイラー展開され、4 次以降は無視される。

    Attributes:
        zero (Fraction): 0 次の係数。
        one (Fraction): 1 次の係数。
        two (Fraction): 2 次の係数。
        three (Fraction): 3 次の係数。
    """

    zero: Fraction
    one: Fraction
    two: Fraction
    three: Fraction

    def __add__(self, other: Self) -> Self:
        """加算。

        Args:
            other (Self): 加算する式。

        Returns:
            Self: 加算結果。
        """
        return Expr(
            self.zero + other.zero,
            self.one + other.one,
            self.two + other.two,
            self.three + other.three,
        )

    def __sub__(self, other: Self) -> Self:
        """減算。

        Args:
            other (Self): 減算する式。

        Returns:
            Self: 減算結果。
        """
        return Expr(
            self.zero - other.zero,
            self.one - other.one,
            self.two - other.two,
            self.three - other.three,
        )

    def __mul__(self, other: Self) -> Self:
        """乗算。

        Args:
            other (Self): 乗算する式。

        Returns:
            Self: 乗算結果。
        """
        return Expr(
            self.zero * other.zero,
            self.zero * other.one + self.one * other.zero,
            self.zero * other.two + self.one * other.one + self.two * other.zero,
            self.zero * other.three
            + self.one * other.two
            + self.two * other.one
            + self.three * other.zero,
        )

    def __str__(self) -> str:
        """式を文字列に変換。

        係数の符号に注意する。

        Returns:
            str: 式を表す文字列。
        """

        def sign(num: Fraction) -> str:
            """符号を返す。"""
            return "+" if num >= 0 else "-"

        return (
            f"{self.zero} "
            f"{sign(self.one)} {abs(self.one)} (p - 1/2) "
            f"{sign(self.two)} {abs(self.two)} (p - 1/2)^2 "
            f"{sign(self.three)} {abs(self.three)} (p - 1/2)^3"
        )

    def float(self) -> FloatExpr:
        """浮動小数点数に変換。

        Returns:
            FloatExpr: 浮動小数点数に変換した式。
        """
        return FloatExpr(
            float(self.zero),
            float(self.one),
            float(self.two),
            float(self.three),
        )


@dataclass(frozen=True, slots=True)
class FloatExpr(Expr):
    """浮動小数点数の式を表すクラス。

    Attributes:
        zero (float): 0 次の係数。
        one (float): 1 次の係数。
        two (float): 2 次の係数。
        three (float): 3 次の係数。
    """

    zero: float
    one: float
    two: float
    three: float

    def __str__(self) -> str:
        """式を文字列に変換。

        Returns:
            str: 式を表す文字列。
        """

        def sign(num: float) -> str:
            """符号を返す。"""
            return "+" if num >= 0 else "-"

        return (
            f"{self.zero:.4f} "
            f"{sign(self.one)} {abs(self.one):.4f} (p - 1/2) "
            f"{sign(self.two)} {abs(self.two):.4f} (p - 1/2)^2 "
            f"{sign(self.three)} {abs(self.three):.4f} (p - 1/2)^3"
        )


def p() -> Expr:
    """確率変数 p を表す式を返す。"""
    return Expr(Fraction(1, 2), Fraction(1, 1), Fraction(0), Fraction(0))


def q() -> Expr:
    """確率変数 q を表す式を返す。

    q = 1 - p
    """
    return Expr(Fraction(1, 2), Fraction(-1, 1), Fraction(0), Fraction(0))


@cache
def prob(win: int, lose: int, goal: int = 30) -> Expr:
    """現在の勝敗から最終的に勝つ確率を返す。

    Args:
        win (int): 勝数。
        lose (int): 敗数。
        goal (int): ゲーム先取数。Defaults to 30.

    Returns:
        Expr: 最終的に勝つ確率。

    Raises:
        ValueError: 勝数または敗数がゴールを超えている場合に送出。
    """
    if win > goal or lose > goal:
        msg = "Win or lose is over goal"
        raise ValueError(msg)
    if win == goal:
        return Expr(Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    if lose == goal:
        return Expr(Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    return p() * prob(win + 1, lose, goal) + q() * prob(win, lose + 1, goal)
