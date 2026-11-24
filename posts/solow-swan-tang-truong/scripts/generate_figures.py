#!/usr/bin/env python3
"""Regenerate Solow–Swan essay figures (matplotlib).

Parameters match the essay body (α=0.35, s=0.24, n=0.015, g=0.02, δ=0.05).
Curves are analytical model simulations — not country data.

Skip (not generated here):
  - hinh-1-1-dai-suy-thoai.png  (historical photo)
  - thumbnail.jpg / thumbnail.png (cover art)

Usage:
  uv run --python 3.12 python posts/solow-swan-tang-truong/scripts/generate_figures.py
  make figures
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

mpl.use("Agg")

OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# Essay palette (close to published PNGs)
INK = "#1a2332"
MUTED = "#5a6a7a"
GRID = "#e6ebf0"
BLUE = "#2f6fad"
ORANGE = "#d97a2b"
GREEN = "#3a8f5c"
RED = "#c44b45"
PURPLE = "#6b4f8a"
TEAL = "#2a8a7a"
NAVY = "#1d2f44"
WHITE = "#ffffff"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.unicode_minus": False,
        "mathtext.fontset": "dejavusans",
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.edgecolor": "#c5ced6",
    }
)

# Canonical parameters from the essay
ALPHA = 0.35
S = 0.24
N = 0.015
G = 0.02
DELTA = 0.05
Q = N + G + DELTA  # 0.085
S2 = 0.32


def f(k):
    return np.asarray(k, dtype=float) ** ALPHA


def mpk(k):
    k = np.asarray(k, dtype=float)
    return ALPHA * k ** (ALPHA - 1)


def k_star(s=S, q=Q):
    return (s / q) ** (1 / (1 - ALPHA))


def y_star(s=S, q=Q):
    return f(k_star(s, q))


def c_star(s=S, q=Q):
    return (1 - s) * y_star(s, q)


def k_path(t, k0, s=S, q=Q):
    """Exact Cobb–Douglas solution for k(t)."""
    t = np.asarray(t, dtype=float)
    zss = s / q
    z0 = k0 ** (1 - ALPHA)
    zt = zss + (z0 - zss) * np.exp(-(1 - ALPHA) * q * t)
    return np.maximum(zt, 1e-16) ** (1 / (1 - ALPHA))


def style_ax(ax, grid=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=3, pad=4, labelsize=9)
    if grid:
        ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)


def save(fig, name: str, dpi: int = 180):
    path = OUT / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print(f"  wrote {path.name}")


def vi(x: float, digits: int = 3) -> str:
    """Format with Vietnamese decimal comma."""
    s = f"{x:.{digits}f}"
    return s.replace(".", ",")


# ---------------------------------------------------------------------------
# Chapter II
# ---------------------------------------------------------------------------


def fig_2_1():
    fig, ax = plt.subplots(figsize=(8.2, 5.1))
    style_ax(ax)
    # Cobb–Douglas Y=K^0.5 L^0.5 = 1 → L = 1/K
    k = np.linspace(0.22, 3.6, 400)
    ax.plot(k, 1 / k, color=BLUE, lw=2.6, label=r"Đường đồng lượng Cobb–Douglas, $Y=1$")
    # Leontief Y=min(K,L)=1
    ax.plot([1, 1], [1, 3.55], color=ORANGE, lw=2.6, label=r"Đường đồng lượng Leontief, $Y=1$")
    ax.plot([1, 3.55], [1, 1], color=ORANGE, lw=2.6)
    ax.scatter([1], [1], s=55, color=BLUE, zorder=5, edgecolors=WHITE, linewidths=1.2)
    ax.set_xlim(0, 3.7)
    ax.set_ylim(0, 3.7)
    ax.set_xlabel(r"Vốn, $K$")
    ax.set_ylabel(r"Lao động, $L$")
    ax.set_title("Hình 2.1 · Công nghệ tỷ lệ cố định và thay thế đầu vào", fontsize=13, pad=10)
    ax.legend(frameon=True, fancybox=False, edgecolor=GRID, fontsize=9, loc="upper right")
    save(fig, "hinh-2-1-leontief-cobb-douglas.png")


def fig_2_2():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.55))
    # A: CRS
    ax = axes[0]
    style_ax(ax)
    lam = np.linspace(0, 4, 50)
    ax.plot(lam, lam, color=TEAL, lw=2.5)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_xlabel(r"Hệ số tăng đồng thời vốn và lao động hiệu quả, $\lambda$")
    ax.set_ylabel("Sản lượng so với mức ban đầu")
    ax.set_title("A. Hiệu suất không đổi theo quy mô", fontsize=11)
    ax.text(
        0.08,
        0.92,
        r"K và AL cùng tăng $\lambda$ lần" + "\n" + r"Y cũng tăng $\lambda$ lần",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="square,pad=0.4", facecolor=WHITE, edgecolor=GRID),
    )
    # B: diminishing MPK
    ax = axes[1]
    style_ax(ax)
    kk = np.linspace(0.01, 4, 300)
    ax.plot(kk, kk**ALPHA, color="#a06644", lw=2.5)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel(r"Vốn $K$, khi lao động hiệu quả $AL=1$")
    ax.set_ylabel(r"Sản lượng $Y$")
    ax.set_title("B. Năng suất biên của vốn giảm dần", fontsize=11)
    ax.text(
        0.08,
        0.92,
        "Chỉ vốn K tăng, AL cố định\nY tăng với mức tăng nhỏ dần",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="square,pad=0.4", facecolor=WHITE, edgecolor=GRID),
    )
    fig.tight_layout()
    save(fig, "hinh-2-2-crs-mpk.png")


def fig_2_3():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    for ax, title, K, AL, Y in [
        (axes[0], "Nền kinh tế 1", 400, 200, 300),
        (axes[1], "Nền kinh tế 2 (gấp đôi quy mô)", 800, 400, 600),
    ]:
        style_ax(ax, grid=False)
        vals = [K, AL, Y]
        labels = [r"$K$", r"$AL$", r"$Y$"]
        colors = [BLUE, ORANGE, GREEN]
        bars = ax.bar(labels, vals, color=colors, width=0.55, edgecolor=WHITE)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v * 1.02, f"{v}", ha="center", va="bottom", fontsize=10)
        k = K / AL
        y = Y / AL
        ax.set_ylim(0, max(vals) * 1.25)
        ax.set_title(title, fontsize=11)
        ax.text(
            0.5,
            0.92,
            rf"$k=K/(AL)={vi(k,1)}$" + "\n" + rf"$y=Y/(AL)={vi(y,1)}$",
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="square,pad=0.35", facecolor="#f7f9fb", edgecolor=GRID),
        )
        ax.set_ylabel("Mức tuyệt đối")
    fig.suptitle(
        "Hình 2.3 · Cùng công nghệ, khác quy mô — cùng $k$ và $y$",
        fontsize=13,
        y=1.02,
    )
    fig.tight_layout()
    save(fig, "hinh-2-3-chuan-hoa-al.png")


def fig_2_4():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.1))
    kk = np.linspace(0.05, 10, 400)
    pts = np.array([1, 2, 4, 8], dtype=float)
    # (a)
    ax = axes[0]
    style_ax(ax)
    ax.plot(kk, f(kk), color=BLUE, lw=2.5, label=r"$y=f(k)=k^{0,35}$")
    ax.scatter(pts, f(pts), color=ORANGE, s=42, zorder=5, edgecolors=WHITE, linewidths=1)
    for k0 in pts:
        ax.annotate(
            f"({int(k0)}; {vi(float(f(k0)), 2)})",
            (k0, float(f(k0))),
            textcoords="offset points",
            xytext=(6, 8),
            fontsize=8,
            color=MUTED,
        )
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2.5)
    ax.set_xlabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.set_ylabel(r"Sản lượng trên mỗi lao động hiệu quả, $y$")
    ax.set_title("(a) Sản lượng tăng với tốc độ giảm dần", fontsize=11)
    ax.legend(fontsize=9, frameon=False, loc="lower right")
    # (b)
    ax = axes[1]
    style_ax(ax)
    ax.plot(kk, mpk(kk), color=PURPLE, lw=2.5, label=r"$MPK=f'(k)=0,35\,k^{-0,65}$")
    ax.scatter(pts, mpk(pts), color=ORANGE, s=42, zorder=5, edgecolors=WHITE, linewidths=1)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 0.8)
    ax.set_xlabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.set_ylabel(r"Năng suất biên của vốn, $MPK$")
    ax.set_title("(b) Năng suất biên giảm khi $k$ tăng", fontsize=11)
    ax.legend(fontsize=9, frameon=False, loc="upper right")
    fig.suptitle(r"Hình 2.4. Hàm Cobb–Douglas trên mỗi lao động hiệu quả ($\alpha=0,35$)", fontsize=13, y=1.02)
    fig.tight_layout()
    save(fig, "hinh-2-4-cobb-douglas-mpk.png")


def fig_2_5():
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    def box(x, y, w, h, title, formula):
        p = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            linewidth=1.2,
            edgecolor=NAVY,
            facecolor="#f4f7fb",
        )
        ax.add_patch(p)
        ax.text(x + w / 2, y + h * 0.68, title, ha="center", va="center", fontsize=10, fontweight="bold", color=NAVY)
        ax.text(x + w / 2, y + h * 0.32, formula, ha="center", va="center", fontsize=10, color=INK)

    box(0.3, 2.6, 2.2, 1.5, "Tổng sản lượng", r"$Y(t)=F(K,AL)$")
    box(3.2, 4.3, 2.0, 1.3, "Tiêu dùng", r"$C=(1-s)Y$")
    box(3.2, 1.2, 2.0, 1.3, "Tiết kiệm", r"$S=sY$")
    box(6.0, 1.2, 2.0, 1.3, "Đầu tư gộp", r"$I=S$")
    box(8.8, 2.6, 2.4, 1.5, "Trữ lượng vốn", r"$K(t)$")
    box(8.8, 0.4, 2.4, 1.2, "Khấu hao", r"$\delta K(t)$")

    def arrow(a, b, dashed=False):
        ax.annotate(
            "",
            xy=b,
            xytext=a,
            arrowprops=dict(
                arrowstyle="-|>",
                color=NAVY,
                lw=1.4,
                linestyle=(0, (4, 3)) if dashed else "solid",
            ),
        )

    arrow((2.5, 3.7), (3.2, 4.7))
    arrow((2.5, 3.0), (3.2, 2.0))
    arrow((5.2, 1.85), (6.0, 1.85))
    arrow((8.0, 1.85), (8.8, 3.0))
    arrow((10.0, 2.6), (10.0, 1.6))
    arrow((8.8, 4.0), (2.5, 4.0), dashed=True)
    ax.text(5.4, 4.2, "Vốn hiện có tham gia sản xuất", fontsize=9, color=MUTED, ha="center")
    ax.text(10.15, 2.05, "Vốn hao mòn", fontsize=8, color=MUTED, rotation=90, va="center")
    ax.text(
        0.3,
        0.35,
        r"Biến động ròng của trữ lượng vốn:  $\dot K(t)=I(t)-\delta K(t)=sY(t)-\delta K(t)$",
        fontsize=11,
        color=INK,
    )
    save(fig, "hinh-2-5-tich-luy-von.png")


# ---------------------------------------------------------------------------
# Chapter III
# ---------------------------------------------------------------------------


def fig_3_1():
    k0 = 4.0
    i_g = float(S * f(k0))
    d_k = DELTA * k0
    n_k = N * k0
    g_k = G * k0
    maintain = d_k + n_k + g_k
    dk = i_g - maintain

    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    style_ax(ax, grid=False)
    ax.set_xlim(0, 0.45)
    ax.set_ylim(-0.6, 1.8)
    ax.set_yticks([0.4, 1.2])
    ax.set_yticklabels(["Đầu tư cần duy trì k", "Đầu tư gộp"])
    ax.set_xlabel("Vốn trên một đơn vị lao động hiệu quả, tính theo một năm")

    ax.barh(1.2, i_g, height=0.45, color=BLUE, edgecolor=WHITE)
    ax.text(i_g / 2, 1.2, vi(i_g, 3), ha="center", va="center", color=WHITE, fontweight="bold")

    left = 0.0
    segs = [(d_k, ORANGE, "//", rf"Khấu hao $\delta k_0$"), (n_k, GREEN, "\\\\", rf"Tăng lao động $nk_0$"), (g_k, RED, "...", rf"Tăng hiệu quả $gk_0$")]
    for val, color, hatch, _ in segs:
        ax.barh(0.4, val, left=left, height=0.45, color=color, edgecolor=WHITE, hatch=hatch)
        ax.text(left + val / 2, 0.4, vi(val, 3), ha="center", va="center", color=WHITE, fontsize=9, fontweight="bold")
        left += val

    ax.annotate(
        "",
        xy=(maintain, 0.95),
        xytext=(i_g, 0.95),
        arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4),
    )
    ax.text((maintain + i_g) / 2, 1.05, rf"$\dot k_0 \approx {vi(dk, 3)}$", ha="center", fontsize=10)

    ax.set_title("Hình 3.1. Phân rã đầu tư duy trì trong mô hình Solow–Swan", fontsize=12, pad=8)
    ax.legend(
        handles=[
            patches.Patch(facecolor=BLUE, label=rf"Đầu tư gộp $sf(k_0)$"),
            patches.Patch(facecolor=ORANGE, hatch="//", label=rf"Khấu hao $\delta k_0$"),
            patches.Patch(facecolor=GREEN, hatch="\\\\", label=rf"Tăng lao động $nk_0$"),
            patches.Patch(facecolor=RED, hatch="...", label=rf"Tăng hiệu quả lao động $gk_0$"),
        ],
        loc="lower right",
        fontsize=8,
        frameon=True,
        fancybox=False,
        edgecolor=GRID,
        ncol=2,
    )
    ax.text(
        0.0,
        -0.45,
        rf"Tham số giả định: $k_0=4$, $\alpha=0,35$, $s=24\%$, $n=1,5\%$, $g=2\%$, $\delta=5\%$.",
        fontsize=8,
        color=MUTED,
    )
    save(fig, "hinh-3-1-dau-tu-duy-tri.png")


def fig_3_2():
    ks = k_star()
    kk = np.linspace(0, 11, 500)
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    style_ax(ax)
    ax.plot(kk, S * f(kk), color=BLUE, lw=2.6, label=r"Đầu tư gộp, $sf(k)$")
    ax.plot(kk, Q * kk, color="#8b5a2b", lw=2.3, label=r"Đầu tư duy trì, $(n+g+\delta)k$")
    ax.scatter([ks], [S * f(ks)], color=INK, s=50, zorder=5, edgecolors=WHITE, linewidths=1.2)
    ax.axvline(ks, color=MUTED, ls=(0, (3, 3)), lw=1.1)
    ax.annotate(
        rf"Trạng thái dừng $k^*\approx {vi(ks, 2)}$",
        xy=(ks, S * f(ks)),
        xytext=(ks + 1.4, S * f(ks) + 0.18),
        arrowprops=dict(arrowstyle="->", color=INK),
        fontsize=10,
    )
    ax.text(1.6, 0.55, "Đầu tư gộp > đầu tư duy trì", fontsize=9, color=MUTED)
    ax.text(7.2, 0.78, "Đầu tư gộp < đầu tư duy trì", fontsize=9, color=MUTED)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.set_ylabel("Đầu tư trên mỗi lao động hiệu quả")
    ax.set_title("Hình 3.2. Điều kiện trạng thái dừng trong mô hình Solow–Swan", fontsize=12)
    ax.legend(loc="upper left", frameon=True, fancybox=False, edgecolor=GRID, fontsize=9)
    # mark k*
    ax.text(ks, -0.06, r"$k^*$", ha="center", transform=ax.get_xaxis_transform(), fontsize=11)
    save(fig, "hinh-3-2-trang-thai-dung.png")


def fig_3_3():
    ks = k_star()
    kk = np.linspace(0.01, 12, 600)
    psi = S * f(kk) - Q * kk
    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    style_ax(ax)
    ax.axhline(0, color=INK, lw=1.0)
    ax.plot(kk, psi, color=BLUE, lw=2.5, label=r"$\dot k = sf(k)-(n+g+\delta)k$")
    ax.scatter([ks], [0], color=BLUE, s=55, zorder=5, edgecolors=WHITE, linewidths=1.2)
    ax.axvline(ks, color=MUTED, ls=(0, (3, 3)), lw=1.1)
    ax.annotate(
        rf"$k^*\approx {vi(ks, 3)}$",
        xy=(ks, 0),
        xytext=(ks + 1.8, 0.08),
        arrowprops=dict(arrowstyle="->", color=INK),
        fontsize=10,
    )
    ax.annotate("", xy=(3.2, 0.05), xytext=(1.2, 0.05), arrowprops=dict(arrowstyle="->", color=INK, lw=1.5))
    ax.text(2.0, 0.07, "k tăng", fontsize=9)
    ax.text(1.5, 0.12, r"$\dot k>0$", fontsize=10, color=BLUE)
    ax.annotate("", xy=(7.0, -0.12), xytext=(9.5, -0.12), arrowprops=dict(arrowstyle="->", color=INK, lw=1.5))
    ax.text(7.8, -0.18, "k giảm", fontsize=9)
    ax.text(8.5, -0.08, r"$\dot k<0$", fontsize=10, color=BLUE)
    ax.text(0.3, -0.42, r"$k=0$ là nghiệm biên", fontsize=9, color=MUTED)
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, 0.2)
    ax.set_xlabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.set_ylabel(r"Tốc độ thay đổi của vốn, $\dot k$")
    ax.set_title("Hình 3.3. Biểu đồ pha và tính ổn định của trạng thái dừng", fontsize=12)
    ax.legend(loc="lower left", fontsize=9, frameon=True, fancybox=False, edgecolor=GRID)
    save(fig, "hinh-3-3-bieu-do-pha.png")


# ---------------------------------------------------------------------------
# Chapter IV
# ---------------------------------------------------------------------------


def fig_4_1():
    k1, k2 = k_star(S), k_star(S2)
    c1, c2 = c_star(S), c_star(S2)
    t = np.linspace(0, 100, 400)
    kt = k_path(t, k1, s=S2)
    # consumption path: jumps then recovers
    ct = (1 - S2) * f(kt)
    c0 = c1
    c_jump = (1 - S2) * f(k1)

    fig, axes = plt.subplots(3, 1, figsize=(6.8, 10.4), gridspec_kw={"hspace": 0.35})
    kk = np.linspace(0, 11, 400)

    ax = axes[0]
    style_ax(ax)
    ax.plot(kk, S * f(kk), color=BLUE, lw=2.2, label=r"Đầu tư trước cú sốc, $s_1 f(k)$")
    ax.plot(kk, S2 * f(kk), color=ORANGE, lw=2.2, label=r"Đầu tư sau cú sốc, $s_2 f(k)$")
    ax.plot(kk, Q * kk, color=GREEN, lw=1.8, ls="--", label=r"Đầu tư duy trì, $(n+g+\delta)k$")
    ax.scatter([k1, k2], [S * f(k1), S2 * f(k2)], color=INK, s=36, zorder=5)
    ax.axvline(k1, color=BLUE, ls=":", lw=1)
    ax.axvline(k2, color=ORANGE, ls=":", lw=1)
    ax.annotate(rf"$k_1^*\approx{vi(k1,2)}$", xy=(k1, S * f(k1)), xytext=(k1 - 2.2, 0.55), arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)
    ax.annotate(rf"$k_2^*\approx{vi(k2,2)}$", xy=(k2, S2 * f(k2)), xytext=(k2 + 0.4, 0.78), arrowprops=dict(arrowstyle="->", color=INK), fontsize=9)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1.0)
    ax.set_title("(a) Đường đầu tư dịch chuyển khi $s$ tăng", fontsize=11)
    ax.set_xlabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.set_ylabel("Đầu tư trên mỗi lao động hiệu quả")
    ax.legend(fontsize=8, frameon=False, loc="upper left")

    ax = axes[1]
    style_ax(ax)
    ax.plot(t, kt, color=BLUE, lw=2.3, label=r"Quỹ đạo $k(t)$ sau cú sốc")
    ax.axhline(k1, color=MUTED, ls=":", lw=1.2, label=r"Trạng thái dừng cũ $k_1^*$")
    ax.axhline(k2, color=ORANGE, ls="--", lw=1.2, label=r"Trạng thái dừng mới $k_2^*$")
    ax.text(2, k1 + 0.15, r"Vốn không nhảy ngay tại $t=0$", fontsize=9, color=MUTED)
    ax.set_xlim(0, 100)
    ax.set_ylim(4.5, 8.0)
    ax.set_title("(b) Vốn tích lũy dẫn đến mức cân bằng mới", fontsize=11)
    ax.set_xlabel("Thời gian sau cú sốc, năm")
    ax.set_ylabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[2]
    style_ax(ax)
    ax.plot(t, ct, color=BLUE, lw=2.3, label=r"Tiêu dùng sau cú sốc, $c(t)$")
    ax.plot([0, 0], [c0, c_jump], color=ORANGE, lw=2.5)
    ax.scatter([0], [c0], color=INK, s=30, zorder=5)
    ax.axhline(c1, color=MUTED, ls=":", lw=1.2, label="Tiêu dùng ở trạng thái dừng cũ")
    ax.axhline(c2, color=ORANGE, ls="--", lw=1.2, label="Tiêu dùng ở trạng thái dừng mới")
    ax.annotate("Giảm ngay khi tỷ lệ tiết kiệm tăng", xy=(0, c_jump), xytext=(18, c_jump - 0.05), arrowprops=dict(arrowstyle="->", color=ORANGE), fontsize=8, color=ORANGE)
    ax.text(35, 1.34, "Sau đó phục hồi khi $k(t)$ và $y(t)$ tăng", fontsize=9, color=MUTED)
    ax.set_xlim(0, 100)
    ax.set_ylim(1.10, 1.45)
    ax.set_title("(c) Tiêu dùng giảm tức thời rồi phục hồi", fontsize=11)
    ax.set_xlabel("Thời gian sau cú sốc, năm")
    ax.set_ylabel(r"Tiêu dùng trên mỗi lao động hiệu quả, $c$")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    save(fig, "hinh-4-1-cu-soc-tiet-kiem.png")


def fig_4_2():
    k1 = k_star()
    q2 = Q + 0.01
    k2 = k_star(S, q2)
    t = np.linspace(0, 100, 400)
    kt = k_path(t, k1, s=S, q=q2)

    # Y/L paths: A(t) f(k(t)), A(0)=1
    # baseline: g=0.02, k fixed at k1
    A_base = np.exp(G * t)
    yl_base = A_base * f(k1)
    # n or delta shock: same k path, same g
    yl_nd = A_base * f(kt)
    # g shock: g'=0.03, k path with q2, A grows faster
    A_g = np.exp(0.03 * t)
    yl_g = A_g * f(kt)

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 8.1), gridspec_kw={"hspace": 0.3})
    kk = np.linspace(0, 11, 400)
    ax = axes[0]
    style_ax(ax)
    ax.plot(kk, S * f(kk), color=BLUE, lw=2.3, label=r"$sf(k)$")
    ax.plot(kk, Q * kk, color=GREEN, lw=1.8, ls="--", label=r"$(n+g+\delta)k$ ban đầu")
    ax.plot(kk, q2 * kk, color=ORANGE, lw=1.8, label=r"$(n'+g+\delta)k$ hoặc tương đương")
    ax.scatter([k1, k2], [S * f(k1), S * f(k2)], color=INK, s=36, zorder=5)
    ax.axvline(k1, color=MUTED, ls=":", lw=1)
    ax.axvline(k2, color=ORANGE, ls=":", lw=1)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 1.0)
    ax.set_title(r"(a) Khi $n$, $g$ hoặc $\delta$ tăng, đường đầu tư duy trì dốc hơn", fontsize=11)
    ax.set_xlabel(r"$k$")
    ax.set_ylabel("Đầu tư")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    style_ax(ax)
    ax.plot(t, yl_base, color=MUTED, lw=1.8, ls="--", label="Quỹ đạo đối chứng")
    ax.plot(t, yl_nd, color=BLUE, lw=2.2, label=r"$n$ hoặc $\delta$ tăng (+0,01)")
    ax.plot(t, yl_g, color=ORANGE, lw=2.2, label=r"$g$ tăng lên 3%")
    ax.set_xlim(0, 100)
    ax.set_title("(b) Sản lượng trên mỗi lao động thực tế so với quỹ đạo đối chứng", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel(r"$Y/L$ (chuẩn hóa $A(0)=1$)")
    ax.legend(fontsize=8, frameon=False)
    save(fig, "hinh-4-2-n-g-delta.png")


def fig_4_3():
    k2 = k_star(S2)
    starts = [2.5, k_star(S), 11.0]
    t = np.linspace(0, 100, 400)
    lam = (1 - ALPHA) * Q

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 8.4), gridspec_kw={"hspace": 0.3})
    ax = axes[0]
    style_ax(ax)
    colors = [BLUE, GREEN, ORANGE]
    for k0, c in zip(starts, colors):
        ax.plot(t, k_path(t, k0, s=S2), color=c, lw=2.2, label=rf"$k(0)={vi(k0, 3) if k0 not in (2.5, 11.0) else vi(k0, 1)}$")
    ax.axhline(k2, color=MUTED, ls="--", lw=1.2, label=rf"$k^*\approx{vi(k2, 3)}$")
    ax.set_xlim(0, 100)
    ax.set_title("(a) Các quỹ đạo vốn hội tụ về cùng trạng thái dừng", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel(r"$k(t)$")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    style_ax(ax)
    z0 = k_star(S) ** (1 - ALPHA)
    zss = S2 / Q
    gap0 = abs(z0 - zss)
    gap = gap0 * np.exp(-lam * t)
    ax.plot(t, gap / gap0, color=BLUE, lw=2.3, label=r"Khoảng cách chuẩn hóa của $z=k^{1-\alpha}$")
    ax.axhline(0.5, color=ORANGE, ls=":", lw=1.2)
    t_half = np.log(2) / lam
    ax.axvline(t_half, color=ORANGE, ls="--", lw=1.1)
    ax.text(t_half + 1, 0.55, rf"Bán rã $\approx {vi(t_half, 2)}$ năm", fontsize=9, color=ORANGE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.05)
    ax.set_title(rf"(b) Hội tụ mũ với $\lambda=(1-\alpha)q={vi(lam, 5)}$", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel("Khoảng cách chuẩn hóa")
    ax.legend(fontsize=8, frameon=False)
    save(fig, "hinh-4-3-hoi-tu.png")


def fig_4_4():
    k1 = k_star()
    t = np.linspace(0, 100, 500)
    # baseline Y/L
    yl0 = np.exp(G * t) * f(k1)
    # savings shock
    kt_s = k_path(t, k1, s=S2)
    yl_s = np.exp(G * t) * f(kt_s)
    # g shock
    q_g = N + 0.03 + DELTA
    kt_g = k_path(t, k1, s=S, q=q_g)
    yl_g = np.exp(0.03 * t) * f(kt_g)

    # instantaneous growth rates of Y/L = g + α k̇/k
    def g_yl(kt, g):
        # numerical dk/dt
        dk = np.gradient(kt, t)
        return g + ALPHA * dk / np.maximum(kt, 1e-9)

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 8.1), gridspec_kw={"hspace": 0.3})
    ax = axes[0]
    style_ax(ax)
    ax.plot(t, yl_s / yl0 - 1, color=BLUE, lw=2.3, label=r"Cú sốc tiết kiệm $s$: $24\%\to 32\%$")
    ax.plot(t, yl_g / yl0 - 1, color=ORANGE, lw=2.3, label=r"Cú sốc công nghệ $g$: $2\%\to 3\%$")
    ax.set_xlim(0, 100)
    ax.set_title("(a) Chênh lệch mức sản lượng trên mỗi lao động so với đối chứng", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel("Chênh lệch tương đối")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    style_ax(ax)
    ax.plot(t, g_yl(kt_s, G) * 100, color=BLUE, lw=2.3, label="Tốc độ tăng sau cú sốc tiết kiệm")
    ax.plot(t, g_yl(kt_g, 0.03) * 100, color=ORANGE, lw=2.3, label="Tốc độ tăng sau cú sốc công nghệ")
    ax.axhline(2.0, color=MUTED, ls=":", lw=1.1)
    ax.axhline(3.0, color=ORANGE, ls="--", lw=1.0, alpha=0.7)
    ax.set_xlim(0, 100)
    ax.set_title("(b) Tốc độ tăng trưởng tức thời của sản lượng trên mỗi lao động", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel("% mỗi năm")
    ax.legend(fontsize=8, frameon=False)
    save(fig, "hinh-4-4-tang-truong.png")


# ---------------------------------------------------------------------------
# Chapter V
# ---------------------------------------------------------------------------


def fig_5_1():
    t = np.linspace(0, 80, 400)
    n_g = N + G
    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    style_ax(ax)
    ax.plot(t, n_g * t, color=BLUE, lw=2.4, label=r"$K,Y,I,C$ (tốc độ $n+g$)")
    ax.plot(t, G * t, color=ORANGE, lw=2.2, label=r"$K/L,Y/L,\ldots$ (tốc độ $g$)")
    ax.plot(t, N * t, color=GREEN, lw=2.0, ls="--", label=r"$L$ (tốc độ $n$)")
    ax.axhline(0, color=PURPLE, lw=1.8, label=r"$k,y,i,c$ (không đổi)")
    ax.set_xlim(0, 80)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel(r"$\ln[X(t)/X(0)]$")
    ax.set_title("Hình 5.1. Cấu trúc tăng trưởng trên đường tăng trưởng cân bằng", fontsize=12)
    ax.legend(fontsize=9, frameon=True, fancybox=False, edgecolor=GRID)
    save(fig, "hinh-5-1-tang-truong-can-bang.png")


def fig_5_2():
    # growth accounting on BGP: Ŷ = αK̂ + (1-α)n + (1-α)g
    contrib = {
        "Vốn\n" + rf"$(\alpha(n+g))$": ALPHA * (N + G) * 100,
        "Lao động\n" + rf"$((1-\alpha)n)$": (1 - ALPHA) * N * 100,
        "TFP\n" + rf"$((1-\alpha)g)$": (1 - ALPHA) * G * 100,
    }
    fig, ax = plt.subplots(figsize=(8.6, 2.6))
    style_ax(ax, grid=False)
    labels = list(contrib.keys())
    vals = list(contrib.values())
    colors = [BLUE, GREEN, ORANGE]
    left = 0.0
    for lab, v, c in zip(labels, vals, colors):
        ax.barh(0, v, left=left, height=0.55, color=c, edgecolor=WHITE)
        ax.text(left + v / 2, 0, f"{vi(v, 3)} pp", ha="center", va="center", color=WHITE, fontweight="bold", fontsize=10)
        ax.text(left + v / 2, 0.42, lab, ha="center", va="bottom", fontsize=9, color=INK)
        left += v
    ax.set_xlim(0, 3.6)
    ax.set_ylim(-0.5, 0.9)
    ax.set_yticks([])
    ax.set_xlabel("Đóng góp vào tốc độ tăng tổng sản lượng (% mỗi năm)")
    ax.set_title(rf"Hình 5.2. Phân rã tăng trưởng trên BGP — tổng $\approx {vi((N+G)*100, 1)}$%", fontsize=12)
    ax.text(0.0, -0.42, rf"$\alpha={vi(ALPHA,2)}$, $n={vi(N*100,1)}\%$, $g={vi(G*100,1)}\%$", fontsize=8, color=MUTED)
    save(fig, "hinh-5-2-phan-ra-tang-truong.png")


def fig_5_3():
    k_now = k_star()
    k_gr = (ALPHA / Q) ** (1 / (1 - ALPHA))
    c_now = c_star()
    c_gr = f(k_gr) - Q * k_gr
    kk = np.linspace(0.05, 15, 500)

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 7.5), gridspec_kw={"hspace": 0.28})
    ax = axes[0]
    style_ax(ax)
    ax.plot(kk, f(kk), color=BLUE, lw=2.4, label=r"$f(k)$")
    ax.plot(kk, Q * kk, color=ORANGE, lw=2.0, ls="--", label=r"$(n+g+\delta)k$")
    # tangent at k_GR with slope q
    xx = np.linspace(k_gr - 3.5, k_gr + 3.5, 100)
    ax.plot(xx, f(k_gr) + Q * (xx - k_gr), color=MUTED, lw=1.4, ls=":", label=r"Tiếp tuyến tại $k_{GR}$, độ dốc $q$")
    ax.vlines(k_now, Q * k_now, f(k_now), color=GREEN, lw=6, alpha=0.35)
    ax.vlines(k_gr, Q * k_gr, f(k_gr), color=RED, lw=6, alpha=0.35)
    ax.scatter([k_gr], [f(k_gr)], color=BLUE, s=40, zorder=5)
    ax.axvline(k_gr, color=MUTED, ls=":", lw=1)
    ax.annotate("Khoảng cách đứng lớn nhất tại $k_{GR}$", xy=(k_gr, (f(k_gr) + Q * k_gr) / 2), xytext=(10.5, 2.2), arrowprops=dict(arrowstyle="->", color=RED), fontsize=9, color=RED)
    ax.text(k_now, -0.15, r"$k^*$ hiện tại", ha="center", transform=ax.get_xaxis_transform(), fontsize=9)
    ax.text(k_gr, -0.15, r"$k_{GR}$", ha="center", transform=ax.get_xaxis_transform(), fontsize=9)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 3.2)
    ax.set_title("(a) Tiêu dùng duy trì là chênh lệch giữa sản lượng và đầu tư duy trì", fontsize=11)
    ax.set_ylabel("Sản lượng và đầu tư")
    ax.legend(fontsize=8, frameon=False, loc="upper left")

    ax = axes[1]
    style_ax(ax)
    cstar_line = f(kk) - Q * kk
    ax.plot(kk, cstar_line, color=BLUE, lw=2.4)
    ax.scatter([k_now, k_gr], [c_now, c_gr], color=BLUE, s=45, zorder=5, edgecolors=WHITE)
    ax.axvline(k_gr, color=MUTED, ls="--", lw=1.1)
    ax.annotate(rf"Hiện tại ($s=24\%$)" + "\n" + rf"$k^*\approx{vi(k_now,3)},\ c^*\approx{vi(c_now,3)}$", xy=(k_now, c_now), xytext=(1.0, 0.7), arrowprops=dict(arrowstyle="->", color=INK), fontsize=8)
    ax.annotate(rf"Quy tắc vàng ($s=35\%$)" + "\n" + rf"$k_{{GR}}\approx{vi(k_gr,3)},\ c_{{GR}}\approx{vi(c_gr,3)}$", xy=(k_gr, c_gr), xytext=(10.2, 1.05), arrowprops=dict(arrowstyle="->", color=INK), fontsize=8)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1.55)
    ax.set_title("(b) Tiêu dùng trạng thái dừng đạt cực đại tại vốn Quy tắc vàng", fontsize=11)
    ax.set_xlabel(r"Vốn trên mỗi lao động hiệu quả, $k$")
    ax.set_ylabel(r"Tiêu dùng trạng thái dừng, $c^*$")
    save(fig, "hinh-5-3-quy-tac-vang.png")


def fig_5_4():
    k_gr = (ALPHA / Q) ** (1 / (1 - ALPHA))
    s_gr = ALPHA
    k_low = k_star(S)
    # over-accumulation path: start from high s then cut to golden rule
    s_high = 0.45
    k_high = k_star(s_high)
    t = np.linspace(0, 120, 500)

    # under-accumulation: raise s from 0.24 to 0.35
    kt_up = k_path(t, k_low, s=s_gr)
    ct_up = (1 - s_gr) * f(kt_up)
    ct_up = ct_up.copy()
    # immediate jump down at t=0
    c_jump_up = (1 - s_gr) * f(k_low)

    # over-accumulation: cut s from 0.45 to 0.35
    kt_down = k_path(t, k_high, s=s_gr)
    ct_down = (1 - s_gr) * f(kt_down)
    c_jump_down = (1 - s_gr) * f(k_high)

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 7.2), gridspec_kw={"hspace": 0.3})
    ax = axes[0]
    style_ax(ax)
    ax.plot(t, ct_up, color=BLUE, lw=2.3, label=r"Tiêu dùng khi $s:24\%\to 35\%$")
    ax.plot([0, 0], [c_star(S), c_jump_up], color=ORANGE, lw=2.2)
    ax.axhline(f(k_gr) - Q * k_gr, color=GREEN, ls="--", lw=1.2, label=r"$c_{GR}$")
    ax.axhline(c_star(S), color=MUTED, ls=":", lw=1.1)
    ax.set_title("(a) Tích lũy dưới Quy tắc vàng: hy sinh tiêu dùng hiện tại", fontsize=11)
    ax.set_ylabel(r"$c(t)$")
    ax.set_xlim(0, 120)
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    style_ax(ax)
    ax.plot(t, ct_down, color=BLUE, lw=2.3, label=r"Tiêu dùng khi $s:45\%\to 35\%$")
    ax.plot([0, 0], [c_star(s_high), c_jump_down], color=ORANGE, lw=2.2)
    ax.axhline(f(k_gr) - Q * k_gr, color=GREEN, ls="--", lw=1.2, label=r"$c_{GR}$")
    ax.axhline(c_star(s_high), color=MUTED, ls=":", lw=1.1)
    ax.set_title("(b) Tích lũy vượt Quy tắc vàng: có thể nâng tiêu dùng ngay", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel(r"$c(t)$")
    ax.set_xlim(0, 120)
    ax.legend(fontsize=8, frameon=False)
    save(fig, "hinh-5-4-chuyen-tiep-vang.png")


# ---------------------------------------------------------------------------
# Chapter VI
# ---------------------------------------------------------------------------


def fig_6_1():
    t = np.linspace(0, 100, 400)
    yss = y_star()
    # absolute: same params, different k0
    y_poor = f(k_path(t, 2.5))
    y_rich = f(k_path(t, 9.0))
    # conditional: different s
    y_a = f(k_path(t, 2.7, s=0.18))
    y_b = f(k_path(t, 5.2, s=0.32))
    yss_a, yss_b = y_star(0.18), y_star(0.32)

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 7.5), gridspec_kw={"hspace": 0.3})
    ax = axes[0]
    style_ax(ax)
    ax.plot(t, y_poor, color=BLUE, lw=2.3, label=r"Nền kinh tế nghèo hơn ban đầu, $k(0)=2,5$")
    ax.plot(t, y_rich, color=ORANGE, lw=2.3, label=r"Nền kinh tế giàu hơn ban đầu, $k(0)=9,0$")
    ax.axhline(yss, color=MUTED, ls="--", lw=1.3, label="Cùng mức cân bằng sau loại trừ xu thế công nghệ")
    ax.set_xlim(0, 100)
    ax.set_ylim(1.3, 2.25)
    ax.set_title("(a) Hội tụ tuyệt đối khi các tham số cấu trúc giống nhau", fontsize=11)
    ax.set_ylabel(r"$(Y/L)/A(t)=f(k)$")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    style_ax(ax)
    ax.plot(t, y_a, color=BLUE, lw=2.3, label=r"Nền kinh tế A, $s=18\%$, $k(0)=2,7$")
    ax.plot(t, y_b, color=ORANGE, lw=2.3, label=r"Nền kinh tế B, $s=32\%$, $k(0)=5,2$")
    ax.axhline(yss_a, color=BLUE, ls=":", lw=1.2, label="Trạng thái dừng của A")
    ax.axhline(yss_b, color=ORANGE, ls="--", lw=1.2, label="Trạng thái dừng của B")
    ax.set_xlim(0, 100)
    ax.set_ylim(1.3, 2.25)
    ax.set_title("(b) Hội tụ có điều kiện về các mức cân bằng khác nhau", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel(r"$(Y/L)/A(t)=f(k)$")
    ax.legend(fontsize=8, frameon=False)
    save(fig, "hinh-6-1-hoi-tu-tuyet-doi-co-dieu-kien.png")


def fig_6_2():
    rng = np.random.default_rng(7)
    n = 40
    # synthetic illustration of beta vs sigma
    y0 = rng.uniform(0.8, 2.5, size=n)
    # beta: poorer grow faster on average, plus noise
    g_i = 0.04 - 0.012 * np.log(y0) + rng.normal(0, 0.008, size=n)
    yT = y0 * np.exp(g_i * 20)
    # for sigma: cross-section dispersion rises slightly
    years = np.arange(0, 21)
    sig = []
    ys = y0.copy()
    for _ in years:
        sig.append(float(np.std(np.log(ys))))
        grow = 0.03 - 0.01 * (np.log(ys) - np.mean(np.log(ys))) + rng.normal(0, 0.02, size=n)
        # add common dispersion shock
        ys = ys * np.exp(grow + rng.normal(0.0, 0.01))

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 7.5), gridspec_kw={"hspace": 0.3})
    ax = axes[0]
    style_ax(ax)
    ax.scatter(np.log(y0), g_i * 100, color=BLUE, s=36, alpha=0.85, edgecolors=WHITE, linewidths=0.6)
    # OLS line
    X = np.column_stack([np.ones(n), np.log(y0)])
    beta = np.linalg.lstsq(X, g_i * 100, rcond=None)[0]
    xx = np.linspace(np.log(y0).min(), np.log(y0).max(), 100)
    ax.plot(xx, beta[0] + beta[1] * xx, color=ORANGE, lw=2.0, label="Xu hướng hồi quy (minh họa)")
    ax.set_title(r"(a) $\beta$-convergence: tăng trưởng và thu nhập ban đầu", fontsize=11)
    ax.set_xlabel(r"$\ln y_0$")
    ax.set_ylabel("Tốc độ tăng trưởng trung bình (%/năm)")
    ax.legend(fontsize=8, frameon=False)

    ax = axes[1]
    style_ax(ax)
    ax.plot(years, sig, color=BLUE, lw=2.3, marker="o", ms=3.5, label=r"Độ lệch chuẩn của $\ln y_t$")
    ax.set_title(r"(b) $\sigma$-convergence: phân tán thu nhập theo thời gian", fontsize=11)
    ax.set_xlabel("Thời gian, năm")
    ax.set_ylabel(r"$\sigma_t$")
    ax.legend(fontsize=8, frameon=False)
    fig.text(0.5, 0.01, "Minh họa mô phỏng lý thuyết — không phải dữ liệu quốc gia quan sát.", ha="center", fontsize=8, color=MUTED)
    save(fig, "hinh-6-2-beta-sigma.png")


FIGURES = [
    fig_2_1,
    fig_2_2,
    fig_2_3,
    fig_2_4,
    fig_2_5,
    fig_3_1,
    fig_3_2,
    fig_3_3,
    fig_4_1,
    fig_4_2,
    fig_4_3,
    fig_4_4,
    fig_5_1,
    fig_5_2,
    fig_5_3,
    fig_5_4,
    fig_6_1,
    fig_6_2,
]


def main():
    print(f"Output → {OUT}")
    print(f"Params: α={ALPHA}, s={S}, n={N}, g={G}, δ={DELTA}, q={Q}")
    print(f"k*={k_star():.4f}, y*={y_star():.4f}")
    for fn in FIGURES:
        fn()
    print("Done. Skipped: hinh-1-1 (photo), thumbnail (cover).")


if __name__ == "__main__":
    main()
