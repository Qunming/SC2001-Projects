import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
 
COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]
 
 
def knapsack_bottom_up(C, w, p):
    n = len(w)
    P = [0] * (C + 1)
    choice = [None] * (C + 1)  # item index, 'skip' (carry P[c-1]), or None
    for c in range(1, C + 1):
        best, best_choice = 0, None
        # option: leave one unit of capacity unused
        if P[c - 1] > best:
            best, best_choice = P[c - 1], "skip"
        for i in range(n):
            if w[i] <= c:
                val = p[i] + P[c - w[i]]
                if val > best:
                    best, best_choice = val, i
        P[c], choice[c] = best, best_choice
    return P, choice
 
 
def traceback(C, w, choice):
    items, c = [], C
    while c > 0:
        ch = choice[c]
        if ch is None:
            break
        if ch == "skip":
            c -= 1
        else:
            items.append(ch)
            c -= w[ch]
    return items
 
 
def print_run(C, w, p, title):
    P, choice = knapsack_bottom_up(C, w, p)
    items = traceback(C, w, choice)
    print("=" * 60)
    print(title)
    print(f"weights = {w}, profits = {p}, C = {C}")
    print("-" * 60)
    print(f"{'c':>3} | {'P(c)':>4} | choice")
    for c in range(C + 1):
        ch = choice[c]
        desc = "-" if ch is None else ("skip (P(c-1))" if ch == "skip"
                                       else f"item {ch} (w={w[ch]}, p={p[ch]})")
        print(f"{c:>3} | {P[c]:>4} | {desc}")
    print("-" * 60)
    print(f"Maximum profit P({C}) = {P[C]}")
    counts = {i: items.count(i) for i in sorted(set(items))}
    print("Items used (type: count) =", counts if counts else "none")
    print(f"Total weight = {sum(w[i] for i in items)} / {C}")
    return P, choice, items
 
 
def plot_dp_table(C, w, p, P, choice, items, fname, title):
    fig, ax = plt.subplots(figsize=(10, 4.5))
    bar_cols = []
    for c in range(C + 1):
        ch = choice[c]
        bar_cols.append("#bbbbbb" if ch in (None, "skip") else COLORS[ch % len(COLORS)])
    ax.bar(range(C + 1), P, color=bar_cols, edgecolor="black")
    for c in range(C + 1):
        ax.text(c, P[c] + 0.4, str(P[c]), ha="center", fontsize=9)
    ax.set_xticks(range(C + 1))
    ax.set_xlabel("Capacity c")
    ax.set_ylabel("P(c)")
    ax.set_title(title)
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[i % len(COLORS)],
                             label=f"item {i} (w={w[i]}, p={p[i]})") for i in range(len(w))]
    handles.append(plt.Rectangle((0, 0), 1, 1, color="#bbbbbb", label="no item / skip"))
    ax.legend(handles=handles, loc="upper left")
    fig.tight_layout()
    fig.savefig(fname, dpi=150)
    plt.close(fig)
 
 
def plot_subproblem_graph(C, w, p, choice, fname, title):
    n = len(w)
    # reachable nodes from C
    reach, stack = set(), [C]
    while stack:
        c = stack.pop()
        if c in reach:
            continue
        reach.add(c)
        for i in range(n):
            if c - w[i] >= 0:
                stack.append(c - w[i])
    nodes = sorted(reach, reverse=True)
 
    # optimal path edges
    opt_edges, c = set(), C
    while c > 0 and choice[c] not in (None, "skip"):
        nxt = c - w[choice[c]]
        opt_edges.add((c, nxt, choice[c]))
        c = nxt
 
    fig, ax = plt.subplots(figsize=(15, 6))
    xs = {c: C - c for c in nodes}  # left = P(C), right = P(0)
    y = 0
    for c in nodes:
        ax.scatter(xs[c], y, s=900, color="#f2f2f2", edgecolor="black", zorder=3)
        ax.text(xs[c], y, f"P({c})", ha="center", va="center", fontsize=8, zorder=4)
 
    for c in nodes:
        for i in range(n):
            t = c - w[i]
            if t < 0 or t not in reach:
                continue
            is_opt = (c, t, i) in opt_edges
            rad = 0.25 + 0.12 * i
            sign = 1 if i % 2 == 0 else -1
            arrow = FancyArrowPatch(
                (xs[c], y), (xs[t], y),
                connectionstyle=f"arc3,rad={sign * rad * 0.5}",
                arrowstyle="-|>", mutation_scale=12,
                color=COLORS[i % len(COLORS)],
                lw=3.2 if is_opt else 1.0,
                alpha=1.0 if is_opt else 0.55,
                shrinkA=14, shrinkB=14, zorder=2)
            ax.add_patch(arrow)
 
    ax.set_xlim(-1, C + 1)
    ax.set_ylim(-5.5, 5.5)
    ax.axis("off")
    handles = [plt.Line2D([0], [0], color=COLORS[i % len(COLORS)], lw=2.5,
                          label=f"item {i}: P(c) -> P(c-{w[i]})  (+{p[i]})") for i in range(n)]
    handles.append(plt.Line2D([0], [0], color="black", lw=4, label="bold = optimal path"))
    ax.legend(handles=handles, loc="upper center", ncol=2)
    ax.set_title(title, fontsize=13)
    fig.tight_layout()
    fig.savefig(fname, dpi=150)
    plt.close(fig)
 
 
def run_case(C, w, p, tag, label):
    P, choice, items = print_run(C, w, p, label)
    plot_dp_table(C, w, p, P, choice, items, f"{tag}_dp_table.png",
                  f"{label}: P(c) for c = 0..{C}   (max profit = {P[C]})")
    plot_subproblem_graph(C, w, p, choice, f"{tag}_subproblem_graph.png",
                          f"{label}: subproblem graph rooted at P({C})")
 
 
if __name__ == "__main__":
    # (2) subproblem graph for P(15) with w=[4,5,8], p=[7,6,9]
    P15, ch15 = knapsack_bottom_up(15, [4, 5, 8], [7, 6, 9])
    plot_subproblem_graph(15, [4, 5, 8], [7, 6, 9], ch15, "q2_P15_subproblem_graph.png",
                          "Q2: subproblem graph for P(15), w=[4,5,8], p=[7,6,9]")
    print(f"P(15) = {P15[15]}\n")
 
    # 4(a)
    run_case(16, [4, 5, 8], [7, 6, 9], "q4a_P16", "4(a) P(16)")
    # 4(b)
    run_case(12, [5, 6, 7], [7, 6, 9], "q4b_P12", "4(b) P(12)")
 