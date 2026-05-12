"""
╔══════════════════════════════════════════════════════════════╗
║   BREAKING THE BUBBLE                                        ║
║   Echo Chamber Detection & Network Robustness Analysis       ║
╚══════════════════════════════════════════════════════════════╝

Requirements:
    pip install networkx matplotlib numpy

Run:
    python breaking_the_bubble.py
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.gridspec as gridspec
from networkx.algorithms import community
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────
# THEME
# ─────────────────────────────────────────
BG     = "#0d1117"
PANEL  = "#161b22"
GRID   = "#21262d"
TEXT   = "#e6edf3"
MUTED  = "#8b949e"
BLUE   = "#58a6ff"
RED    = "#f85149"
GREEN  = "#3fb950"
GOLD   = "#d29922"
PURPLE = "#bc8cff"
TEAL   = "#39d353"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   PANEL,
    "axes.edgecolor":   GRID,
    "axes.labelcolor":  TEXT,
    "xtick.color":      MUTED,
    "ytick.color":      MUTED,
    "text.color":       TEXT,
    "grid.color":       GRID,
    "grid.linestyle":   "--",
    "grid.alpha":       0.5,
    "font.family":      "DejaVu Sans",
})

# ─────────────────────────────────────────
# 1. BUILD GRAPH
# ─────────────────────────────────────────

G = nx.Graph()

edges = [
    (1, 2), (1, 3), (2, 3), (2, 4), (3, 4),
    (5, 6), (5, 7), (6, 7), (6, 8), (7, 8),
    (9, 10), (9, 11), (10, 11), (10, 12), (11, 12),
    (4, 5), (8, 9), (3, 10), (2, 11)
]
G.add_edges_from(edges)

opinions = {
    1:"A", 2:"A", 3:"A",  4:"A",
    5:"B", 6:"B", 7:"B",  8:"B",
    9:"A", 10:"A", 11:"B", 12:"B"
}
nx.set_node_attributes(G, opinions, "opinion")

# ─────────────────────────────────────────
# 2. ANALYSIS
# ─────────────────────────────────────────

communities_list = list(community.greedy_modularity_communities(G))
community_map    = {}
for i, com in enumerate(communities_list):
    for node in com:
        community_map[node] = i

degree_cent      = nx.degree_centrality(G)
betweenness_cent = nx.betweenness_centrality(G)
closeness_cent   = nx.closeness_centrality(G)

top_degree_node  = sorted(degree_cent, key=degree_cent.get, reverse=True)[0]

echo_chambers      = []
echo_chamber_nodes = set()

for i, com in enumerate(communities_list):
    count = {}
    for n in com:
        op = opinions[n]
        count[op] = count.get(op, 0) + 1
    dominant = max(count, key=count.get)
    ratio    = count[dominant] / len(com)
    if ratio >= 0.75:
        echo_chambers.append(i + 1)
        echo_chamber_nodes.update(com)

COMM_COLORS = [PURPLE, TEAL, GOLD]

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

def node_colors(graph, highlight=None):
    colors = []
    for n in graph.nodes():
        if highlight and n in highlight:
            colors.append(GOLD)
        elif graph.nodes[n].get("opinion") == "A":
            colors.append(BLUE)
        else:
            colors.append(RED)
    return colors

def node_sizes(graph, scale=1200):
    return [300 + degree_cent.get(n, 0) * scale for n in graph.nodes()]

def draw_glowing_edges(ax, graph, pos):
    for u, v in graph.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        is_bridge = (betweenness_cent.get(u, 0) > 0.10
                     or betweenness_cent.get(v, 0) > 0.10)
        c        = GREEN if is_bridge else "#555566"
        lw_outer = 2.5 if is_bridge else 1.5
        lw_inner = 1.2 if is_bridge else 0.6
        ax.plot([x0,x1],[y0,y1], color=c, lw=lw_outer, alpha=0.18, solid_capstyle="round")
        ax.plot([x0,x1],[y0,y1], color=c, lw=lw_inner, alpha=0.70, solid_capstyle="round")

def add_glow_nodes(ax, graph, pos, colors, sizes):
    nodes   = list(graph.nodes())
    xs      = [pos[n][0] for n in nodes]
    ys      = [pos[n][1] for n in nodes]
    ax.scatter(xs, ys, s=[s*2.8 for s in sizes], c=colors, alpha=0.08, linewidths=0, zorder=3)
    ax.scatter(xs, ys, s=[s*1.5 for s in sizes], c=colors, alpha=0.12, linewidths=0, zorder=4)
    borders = [GOLD if n == top_degree_node else GRID for n in nodes]
    ax.scatter(xs, ys, s=sizes, c=colors, alpha=0.90,
               linewidths=1.5, edgecolors=borders, zorder=5)

def label_nodes(ax, graph, pos, font_size=9):
    for n in graph.nodes():
        x, y = pos[n]
        ax.text(x, y, str(n), ha="center", va="center",
                fontsize=font_size, fontweight="bold", color="white", zorder=6,
                path_effects=[pe.withStroke(linewidth=2, foreground="black")])

# ─────────────────────────────────────────
# FIGURE 1 — MAIN DASHBOARD (2×2)
# ─────────────────────────────────────────

fig = plt.figure(figsize=(20, 16))
fig.patch.set_facecolor(BG)

gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.28,
                        left=0.05, right=0.97, top=0.88, bottom=0.05)

pos = nx.spring_layout(G, seed=42, k=1.8)

# ── Panel A : Original Network ─────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(PANEL)
ax1.set_title("Original Social Network",
              color=TEXT, fontsize=13, fontweight="bold", pad=10)

draw_glowing_edges(ax1, G, pos)
add_glow_nodes(ax1, G, pos, node_colors(G), node_sizes(G))
label_nodes(ax1, G, pos)

ax1.legend(handles=[
    mpatches.Patch(color=BLUE,  label="Opinion A"),
    mpatches.Patch(color=RED,   label="Opinion B"),
    mpatches.Patch(color=GREEN, label="Bridge edge"),
    mpatches.Patch(color=GOLD,  label=f"Top influencer (User {top_degree_node})"),
], loc="lower left", fontsize=7.5,
   facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, framealpha=0.9)
ax1.axis("off")

# ── Panel B : Community Detection ──────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(PANEL)
ax2.set_title("Community Detection (Greedy Modularity)",
              color=TEXT, fontsize=13, fontweight="bold", pad=10)

for i, com in enumerate(communities_list):
    xs = [pos[n][0] for n in com]
    ys = [pos[n][1] for n in com]
    cx, cy = np.mean(xs), np.mean(ys)
    r  = max(max(abs(x-cx) for x in xs), max(abs(y-cy) for y in ys)) + 0.22
    ax2.add_patch(plt.Circle((cx,cy), r, color=COMM_COLORS[i], alpha=0.10, zorder=1))
    ax2.add_patch(plt.Circle((cx,cy), r, fill=False, edgecolor=COMM_COLORS[i],
                              linewidth=1.5, linestyle="--", alpha=0.55, zorder=2))

draw_glowing_edges(ax2, G, pos)
comm_node_colors = [COMM_COLORS[community_map[n]] for n in G.nodes()]
add_glow_nodes(ax2, G, pos, comm_node_colors, node_sizes(G))
label_nodes(ax2, G, pos)

ax2.legend(handles=[mpatches.Patch(color=c, label=f"Community {i+1}")
                    for i, c in enumerate(COMM_COLORS)],
           loc="lower left", fontsize=8,
           facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, framealpha=0.9)
ax2.axis("off")

# ── Panel C : Echo Chamber Highlight ───────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(PANEL)
ax3.set_title("Echo Chamber Detection",
              color=TEXT, fontsize=13, fontweight="bold", pad=10)

draw_glowing_edges(ax3, G, pos)
add_glow_nodes(ax3, G, pos, node_colors(G, highlight=echo_chamber_nodes), node_sizes(G))
label_nodes(ax3, G, pos)

for i, com in enumerate(communities_list):
    if (i+1) in echo_chambers:
        xs = [pos[n][0] for n in com]
        ys = [pos[n][1] for n in com]
        ax3.text(np.mean(xs), np.mean(ys)+0.30,
                 f"Echo\nChamber {i+1}", ha="center", va="center",
                 fontsize=7.5, color=GOLD, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor=BG,
                           edgecolor=GOLD, alpha=0.8))

ax3.legend(handles=[
    mpatches.Patch(color=GOLD, label="Echo chamber node"),
    mpatches.Patch(color=BLUE, label="Opinion A (non-echo)"),
    mpatches.Patch(color=RED,  label="Opinion B (non-echo)"),
], loc="lower left", fontsize=7.5,
   facecolor=PANEL, edgecolor=GRID, labelcolor=TEXT, framealpha=0.9)
ax3.axis("off")

# ── Panel D : After Influencer Removal ─────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(PANEL)
ax4.set_title(f"After Removing Top Influencer (User {top_degree_node})",
              color=TEXT, fontsize=13, fontweight="bold", pad=10)

G_removed   = G.copy()
G_removed.remove_node(top_degree_node)
pos_removed = {n: pos[n] for n in G_removed.nodes()}

draw_glowing_edges(ax4, G_removed, pos_removed)
add_glow_nodes(ax4, G_removed, pos_removed, node_colors(G_removed), node_sizes(G_removed))
label_nodes(ax4, G_removed, pos_removed)

rx, ry = pos[top_degree_node]
ax4.scatter([rx], [ry], s=400, marker="X", color=RED, alpha=0.6, zorder=7)
ax4.text(rx, ry-0.14, f"User {top_degree_node}\nremoved",
         ha="center", fontsize=7, color=RED, alpha=0.8)

n_comp = nx.number_connected_components(G_removed)
ax4.text(0.02, 0.02,
         f"Connected: {nx.is_connected(G_removed)}   Components: {n_comp}",
         transform=ax4.transAxes, fontsize=8, color=MUTED,
         bbox=dict(facecolor=BG, edgecolor=GRID, boxstyle="round,pad=0.3", alpha=0.8))
ax4.axis("off")

# ── Super title — letter_spacing REMOVED (fix) ─────────────
fig.text(0.5, 0.94,
         "BREAKING THE BUBBLE  —  Echo Chamber Detection & Network Robustness",
         ha="center", va="center", fontsize=16, fontweight="bold", color=TEXT)
fig.text(0.5, 0.91,
         f"{G.number_of_nodes()} users  ·  {G.number_of_edges()} connections  "
         f"·  {len(communities_list)} communities  ·  {len(echo_chambers)} echo chamber(s)",
         ha="center", va="center", fontsize=10, color=MUTED)

fig.savefig("dashboard.png", dpi=200, bbox_inches="tight", facecolor=BG)
plt.close(fig)
print("✓ dashboard.png saved")


# ─────────────────────────────────────────
# FIGURE 2 — CENTRALITY BAR CHARTS
# ─────────────────────────────────────────

fig2, axes = plt.subplots(1, 3, figsize=(18, 5))
fig2.patch.set_facecolor(BG)
fig2.suptitle("Centrality Metrics per User",
              fontsize=15, fontweight="bold", color=TEXT, y=1.01)

centrality_data = [
    ("Degree Centrality",      degree_cent,      BLUE),
    ("Betweenness Centrality", betweenness_cent, GREEN),
    ("Closeness Centrality",   closeness_cent,   PURPLE),
]

for ax, (title, cent, color) in zip(axes, centrality_data):
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)

    nodes_sorted = sorted(cent.keys())
    values       = [cent[n] for n in nodes_sorted]
    bar_colors   = [GOLD if n == top_degree_node else color for n in nodes_sorted]

    bars = ax.bar([str(n) for n in nodes_sorted], values,
                  color=bar_colors, edgecolor=BG, linewidth=0.8, zorder=3)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.005,
                f"{val:.2f}", ha="center", va="bottom",
                fontsize=7.5, color=TEXT)

    ax.set_title(title, color=TEXT, fontsize=11, fontweight="bold", pad=8)
    ax.set_xlabel("User",  color=MUTED, fontsize=9)
    ax.set_ylabel("Score", color=MUTED, fontsize=9)
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(axis="y", zorder=0)
    ax.tick_params(colors=MUTED)

fig2.tight_layout()
fig2.savefig("centrality_charts.png", dpi=200, bbox_inches="tight", facecolor=BG)
plt.close(fig2)
print("✓ centrality_charts.png saved")


# ─────────────────────────────────────────
# FIGURE 3 — ADJACENCY MATRIX HEATMAP
# ─────────────────────────────────────────

fig3, ax = plt.subplots(figsize=(8, 7))
fig3.patch.set_facecolor(BG)
ax.set_facecolor(BG)

node_order = sorted(G.nodes())
matrix     = nx.to_numpy_array(G, nodelist=node_order)

ax.imshow(matrix, cmap="Blues", aspect="auto", vmin=0, vmax=1)

ax.set_xticks(range(len(node_order)))
ax.set_yticks(range(len(node_order)))
ax.set_xticklabels([f"U{n}" for n in node_order], fontsize=9, color=TEXT)
ax.set_yticklabels([f"U{n}" for n in node_order], fontsize=9, color=TEXT)
ax.set_title("Adjacency Matrix", color=TEXT, fontsize=13, fontweight="bold", pad=12)

for i in range(len(node_order)):
    for j in range(len(node_order)):
        if matrix[i][j]:
            ax.text(j, i, "●", ha="center", va="center",
                    fontsize=10, color=BLUE, alpha=0.85)

comm_positions = {n: idx for idx, n in enumerate(node_order)}
for com in communities_list:
    idxs = sorted([comm_positions[n] for n in com])
    lo, hi = idxs[0]-0.5, idxs[-1]+0.5
    ax.add_patch(mpatches.FancyBboxPatch(
        (lo, lo), hi-lo, hi-lo,
        linewidth=1.5, edgecolor=GOLD, facecolor="none",
        linestyle="--", boxstyle="round,pad=0.1"))

ax.text(0.98, 0.01, "Dashed boxes = communities",
        transform=ax.transAxes, fontsize=8, color=GOLD, ha="right", va="bottom", alpha=0.8)

for spine in ax.spines.values():
    spine.set_edgecolor(GRID)

fig3.tight_layout()
fig3.savefig("adjacency_matrix.png", dpi=200, bbox_inches="tight", facecolor=BG)
plt.close(fig3)
print("✓ adjacency_matrix.png saved")


# ─────────────────────────────────────────
# FIGURE 4 — INTERACTIVE PYVIS GRAPH
# ─────────────────────────────────────────

try:
    from pyvis.network import Network
    import webbrowser, os

    net = Network(height="650px", width="100%", bgcolor=BG,
                  font_color=TEXT, notebook=False)

    net.set_options("""
    {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -4500,
          "centralGravity": 0.3,
          "springLength": 130,
          "springConstant": 0.05,
          "damping": 0.12
        },
        "stabilization": { "iterations": 200 }
      },
      "interaction": { "hover": true, "tooltipDelay": 150 }
    }
    """)

    for node_id in G.nodes():
        op       = opinions[node_id]
        ci       = community_map.get(node_id, 0)
        deg      = degree_cent[node_id]
        bet      = betweenness_cent[node_id]
        size     = 20 + deg * 60
        base_col = BLUE if op == "A" else RED
        is_top   = (node_id == top_degree_node)
        bdr      = GOLD if is_top else (GREEN if bet > 0.10 else COMM_COLORS[ci])
        bdr_w    = 4 if is_top else (3 if bet > 0.10 else 2)

        net.add_node(node_id,
            label=f"User {node_id}",
            title=(f"User {node_id}\nOpinion: {op}\n"
                   f"Community: {ci+1}\n"
                   f"Degree: {deg:.2f}\nBetweenness: {bet:.2f}"),
            color={"background": base_col, "border": bdr,
                   "highlight": {"background": "#ffffff", "border": bdr},
                   "hover":     {"background": "#ffffff", "border": bdr}},
            size=size, borderWidth=bdr_w,
            font={"color": "#ffffff", "size": 14, "bold": True},
            shadow={"enabled": True, "color": base_col, "size": 12, "x": 0, "y": 0})

    for a, b in G.edges():
        is_bridge = (betweenness_cent.get(a,0) > 0.10
                     or betweenness_cent.get(b,0) > 0.10)
        ec = GREEN if is_bridge else "#555566"
        ew = 2.5   if is_bridge else 1.2
        net.add_edge(a, b,
            color={"color": ec, "highlight": "#ffffff", "hover": "#ffffff"},
            width=ew, smooth={"type": "dynamic"})

    net.save_graph("social_network.html")
    print("✓ social_network.html saved")
    webbrowser.open("file://" + os.path.abspath("social_network.html"))
    print("  Opened in browser — nodes are draggable and hoverable!")

except ImportError:
    print("  pyvis not installed — skipping interactive graph.")
    print("  To enable it:  pip install pyvis")


# ─────────────────────────────────────────
# TERMINAL SUMMARY
# ─────────────────────────────────────────

DIV = "─" * 54

def header(t):
    print(f"\n{DIV}\n  {t}\n{DIV}")

header("DETECTED COMMUNITIES")
for i, com in enumerate(communities_list):
    print(f"  Community {i+1}: {sorted(com)}")

header("ECHO CHAMBER ANALYSIS")
for i, com in enumerate(communities_list):
    count = {}
    for n in com:
        op = opinions[n]
        count[op] = count.get(op, 0) + 1
    dominant = max(count, key=count.get)
    ratio    = count[dominant] / len(com)
    tag      = "Echo Chamber DETECTED" if ratio >= 0.75 else "Mixed — no chamber"
    print(f"  Community {i+1} {sorted(com)}")
    print(f"    Opinions: {count}  |  Dominant: {dominant} ({ratio:.0%})  ->  {tag}")

header("TOP INFLUENCERS — DEGREE CENTRALITY")
for n, v in sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:3]:
    bar = "█" * int(v * 40)
    print(f"  User {n:2d}:  {bar}  {v:.3f}")

header("TOP BRIDGES — BETWEENNESS CENTRALITY")
for n, v in sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:3]:
    bar = "█" * int(v * 40)
    print(f"  User {n:2d}:  {bar}  {v:.3f}")

header("ROBUSTNESS — BEFORE REMOVAL")
print(f"  Nodes: {G.number_of_nodes()}   Edges: {G.number_of_edges()}")
print(f"  Connected: {nx.is_connected(G)}   Components: {nx.number_connected_components(G)}")

header(f"ROBUSTNESS — AFTER REMOVING USER {top_degree_node}")
print(f"  Nodes: {G_removed.number_of_nodes()}   Edges: {G_removed.number_of_edges()}")
print(f"  Connected: {nx.is_connected(G_removed)}   Components: {nx.number_connected_components(G_removed)}")

header("GENERATED OUTPUTS")
print("  1. dashboard.png          — 4-panel network analysis")
print("  2. centrality_charts.png  — degree / betweenness / closeness bars")
print("  3. adjacency_matrix.png   — connection heatmap with community boxes")
print("  4. social_network.html    — interactive draggable graph (needs pyvis)")
print(f"\n  Analysis complete.\n")
