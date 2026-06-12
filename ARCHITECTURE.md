# System Architecture — Breaking the Bubble: Echo Chamber Detection and Network Robustness Analysis

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Full System Diagram](#2-full-system-diagram)
3. [Module Descriptions](#3-module-descriptions)
4. [Algorithm Details](#4-algorithm-details)
5. [Data Flow](#5-data-flow)
6. [Output Files](#6-output-files)
7. [Hardware & Software Requirements](#7-hardware--software-requirements)

---

## 1. Architecture Overview

The system is structured as a single-pipeline graph analytical application with five functional layers:

```
┌──────────────────────────────────────────────┐
│         Layer 1 — Data Modelling              │
│    Graph construction + opinion assignment    │
├──────────────────────────────────────────────┤
│         Layer 2 — Community Analysis          │
│    Greedy Modularity + Echo Chamber Detection │
├──────────────────────────────────────────────┤
│         Layer 3 — Centrality Analysis         │
│    Degree · Betweenness · Closeness           │
├──────────────────────────────────────────────┤
│         Layer 4 — Robustness Analysis         │
│    Node removal simulation + connectivity     │
├──────────────────────────────────────────────┤
│         Layer 5 — Visualization & Reporting   │
│    Dashboard · Charts · PyVis HTML            │
└──────────────────────────────────────────────┘
```

---

## 2. Full System Diagram

```
                    ┌─────────────────────────┐
                    │   Social Network Input   │
                    │  Users + Relationships   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Graph Construction    │
                    │       (NetworkX)         │
                    │  G = (V, E)              │
                    │  V = {users}             │
                    │  E = {relationships}     │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Opinion Assignment    │
                    │  ∀ v ∈ V:               │
                    │  opinion(v) ∈ {A, B}    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Community Detection   │
                    │  Greedy Modularity      │
                    │  Maximize Q → {C1..Ck}  │
                    └──────┬─────────┬────────┘
                           │         │
              ┌────────────▼──┐  ┌───▼───────────────┐
              │  Echo Chamber │  │  Centrality        │
              │  Detection    │  │  Analysis          │
              │               │  │                    │
              │  For each Ci: │  │  · Degree          │
              │  D = dom/|Ci| │  │  · Betweenness     │
              │  D ≥ 0.75 →   │  │  · Closeness       │
              │  Echo Chamber │  └───────────┬────────┘
              └──────┬────────┘              │
                     │              ┌────────▼────────┐
                     │              │  Influential     │
                     │              │  User Detection  │
                     │              │  argmax(degree)  │
                     │              └────────┬────────┘
                     │                       │
                     └──────────┬────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   Robustness Analysis    │
                    │  G' = G − {v*}           │
                    │  · is_connected(G')?     │
                    │  · n_components(G')      │
                    │  · isolated nodes        │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   Visualization Layer    │
                    └──┬──────────┬───────────┘
                       │          │
           ┌───────────▼─┐   ┌────▼──────────────┐
           │ Static Plots│   │ Interactive Graph  │
           │             │   │  (PyVis HTML)      │
           │ dashboard   │   │  social_network    │
           │ .png        │   │  .html             │
           │             │   └───────────────────┘
           │ centrality  │
           │ _charts.png │
           │             │
           │ adjacency   │
           │ _matrix.png │
           └─────────────┘
```

---

## 3. Module Descriptions

### Module 1 — Graph Construction

Creates the undirected social network graph using NetworkX. Each user is added as a node and each relationship as an edge.

| Property | Value |
|---|---|
| Library | NetworkX |
| Graph Type | Undirected (`nx.Graph`) |
| Node Attributes | User ID, opinion |
| Edge Attributes | Relationship (unweighted) |

```python
# Pseudocode
G = nx.Graph()
G.add_nodes_from(users)
G.add_edges_from(relationships)
```

---

### Module 2 — Opinion Assignment

Assigns a binary opinion (A or B) to each node to simulate real-world ideological or political alignment. Opinions are used downstream by the echo chamber detection module.

| Property | Value |
|---|---|
| Opinion Values | `"A"` or `"B"` |
| Assignment | Configurable (random or preset) |
| Storage | Node attribute: `G.nodes[v]['opinion']` |

---

### Module 3 — Community Detection

Applies the **Greedy Modularity** algorithm to partition the graph into communities of densely connected users.

| Property | Value |
|---|---|
| Algorithm | `nx.community.greedy_modularity_communities()` |
| Objective | Maximize modularity Q |
| Output | List of frozensets, each = one community |

See Section 4 for algorithm details.

---

### Module 4 — Echo Chamber Detection

For each detected community, computes the **opinion dominance ratio D** and classifies the community as an echo chamber if D ≥ 0.75.

| Property | Value |
|---|---|
| Input | Community node set + node opinions |
| Threshold | D ≥ 0.75 |
| Output | `ECHO CHAMBER` or `DIVERSE` label per community |

Formula:

```
        count(nodes with dominant opinion in Ci)
D  =  ─────────────────────────────────────────
                    |Ci|
```

---

### Module 5 — Centrality Analysis

Computes three centrality measures for every node in the graph.

| Measure | NetworkX Function | Meaning |
|---|---|---|
| Degree Centrality | `nx.degree_centrality(G)` | Direct connection count (normalized) |
| Betweenness Centrality | `nx.betweenness_centrality(G)` | Fraction of shortest paths through node |
| Closeness Centrality | `nx.closeness_centrality(G)` | Inverse mean shortest path to all nodes |

---

### Module 6 — Influential User Detection

Identifies the single most influential user in the network by selecting the node with the maximum degree centrality score.

| Property | Value |
|---|---|
| Criterion | `argmax(degree_centrality)` |
| Output | Top influencer node ID + centrality score |
| Secondary | Top betweenness node (bridge identification) |

---

### Module 7 — Robustness Analysis

Simulates the removal of the top influencer node and evaluates the structural impact on the network.

| Property | Value |
|---|---|
| Operation | `G.remove_node(v*)` on a copy |
| Metrics | Connectivity, component count, isolated nodes |
| Functions | `nx.is_connected()`, `nx.connected_components()` |

```
G  → connected, 1 component
         │
Remove v* (top influencer)
         │
G' → connected? [ YES / NO ]
     components: k
     largest component size: m
     isolated nodes: p
```

---

### Module 8 — Visualization Module

Generates all static and interactive output visualizations.

| Output | Tool | Description |
|---|---|---|
| `dashboard.png` | Matplotlib | Multi-panel: graph, communities, echo chambers |
| `centrality_charts.png` | Matplotlib | Bar charts for all three centrality measures |
| `adjacency_matrix.png` | Matplotlib + NumPy | Heatmap of the adjacency matrix |
| `social_network.html` | PyVis | Interactive graph with physics simulation |

---

## 4. Algorithm Details

### Greedy Modularity Community Detection

**Modularity Q** measures the fraction of edges within communities minus the expected fraction if edges were placed randomly:

```
        1    ⎡         ki · kj  ⎤
Q  =  ─────  Σ  ⎢ Aij  −  ──────  ⎥  δ(ci, cj)
       2m   i,j ⎣          2m   ⎦

Where:
  Aij  = 1 if edge (i,j) exists, else 0
  ki   = degree of node i
  m    = total number of edges
  ci   = community label of node i
  δ    = 1 if ci == cj (same community), else 0
```

The greedy algorithm starts with each node as its own community and merges the pair that produces the greatest ΔQ at each step, until no merge improves Q.

```
Step 1   Initialize: each node = its own community
                          │
Step 2   Compute ΔQ for every pair of adjacent communities
                          │
Step 3   Merge pair with maximum ΔQ
                          │
Step 4   Repeat Steps 2–3 until ΔQ ≤ 0 for all pairs
                          │
Step 5   Return final community partition
```

---

### Echo Chamber Detection

```python
# Pseudocode
for community in communities:
    opinions = [G.nodes[v]['opinion'] for v in community]
    dominant = max(set(opinions), key=opinions.count)
    D = opinions.count(dominant) / len(opinions)

    if D >= 0.75:
        label = "ECHO CHAMBER"
    else:
        label = "DIVERSE"
```

---

### Centrality Formulas

**Degree Centrality** (normalized):
```
          deg(v)
Cd(v) = ──────────
          n − 1
```

**Betweenness Centrality** (normalized):
```
           Σ  σ(s,t|v)
            s≠v≠t
Cb(v) = ──────────────────
             σ(s,t)

Where σ(s,t)   = total shortest paths from s to t
      σ(s,t|v) = those passing through v
```

**Closeness Centrality**:
```
           n − 1
Cc(v) = ──────────────
         Σ d(v, u)
          u≠v

Where d(v,u) = shortest path distance from v to u
```

---

### Robustness Metrics

After removing node v*:

| Metric | Description |
|---|---|
| `is_connected(G')` | Whether the graph remains fully connected |
| `number_connected_components(G')` | How many isolated subgraphs result |
| Largest component size | Number of nodes in the biggest remaining cluster |
| Isolated node count | Nodes with degree 0 after removal |

A high component count post-removal indicates the network was structurally dependent on v* as a bridge.

---

## 5. Data Flow

```
Step 1   Define user list and relationship list

Step 2   Construct NetworkX graph G = (V, E)

Step 3   Assign opinion (A or B) to each node v ∈ V

Step 4   Run greedy_modularity_communities(G)
         → partition {C1, C2, ..., Ck}

Step 5   For each Ci:
           compute opinion dominance ratio D
           classify: Echo Chamber or Diverse

Step 6   Compute degree_centrality(G) for all nodes
         Compute betweenness_centrality(G) for all nodes
         Compute closeness_centrality(G) for all nodes

Step 7   Identify v* = argmax(degree_centrality)

Step 8   Construct G' = G − {v*}
         Measure connectivity, components, isolated nodes

Step 9   Generate dashboard.png (multi-panel Matplotlib figure)
         Generate centrality_charts.png
         Generate adjacency_matrix.png

Step 10  Generate social_network.html (PyVis interactive graph)

Step 11  Print analysis summary to console
```

---

## 6. Output Files

| File | Format | Description |
|---|---|---|
| `dashboard.png` | PNG | Multi-panel figure: original graph, communities, echo chambers, robustness |
| `centrality_charts.png` | PNG | Side-by-side bar charts for degree, betweenness, closeness centrality |
| `adjacency_matrix.png` | PNG | Colour-coded heatmap of the N×N adjacency matrix |
| `social_network.html` | HTML | Physics-based interactive graph (drag, zoom, hover) powered by PyVis + vis.js |

---

## 7. Hardware & Software Requirements

### Hardware

| Component | Minimum | Recommended |
|---|---|---|
| Processor | Intel Core i3 | Intel Core i5/i7 |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB | 1 GB SSD |

### Software

| Package | Purpose |
|---|---|
| Python 3.x | Runtime |
| NetworkX | Graph construction, community detection, centrality, robustness |
| Matplotlib | Static visualization (dashboard, charts, adjacency matrix) |
| NumPy | Matrix operations for adjacency matrix |
| PyVis | Interactive HTML graph rendering |
| VS Code | Development environment |
| GitHub | Version control |
| Overleaf | LaTeX report writing |

---

*Architecture documented by Abdul Haris H — M.Tech CSE, Government Engineering College Thrissur, April 2026*