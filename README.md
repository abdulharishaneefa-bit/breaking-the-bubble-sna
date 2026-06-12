<div align="center">

<h1>🫧 Breaking the Bubble</h1>
<h3>Echo Chamber Detection and Network Robustness Analysis</h3>

<p><strong>Graph-based social network analysis for community detection, echo chamber identification, and structural resilience evaluation</strong></p>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph%20Analysis-orange?style=for-the-badge)](https://networkx.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)](https://matplotlib.org)
[![PyVis](https://img.shields.io/badge/PyVis-Interactive%20Graph-green?style=for-the-badge)](https://pyvis.readthedocs.io)
[![License](https://img.shields.io/badge/License-Academic-blue?style=for-the-badge)](LICENSE)

<br/>

> Social networks don't just connect people — they also trap them. This project models how opinion bubbles form, which nodes hold them together, and what happens when you break them open.

</div>

---

## 📌 Overview

**Breaking the Bubble** is a Social Network Analysis (SNA) project that models a social network as a graph and applies graph-theoretic techniques to study:

- How user communities naturally form (Greedy Modularity)
- Where opinion echo chambers emerge (dominance ratio analysis)
- Which users hold the most influence or act as critical bridges (centrality measures)
- How the network degrades when those nodes are removed (robustness analysis)

Nodes represent users. Edges represent relationships. Opinions are binary (A or B) and assigned to nodes to simulate real-world ideological clustering.

Built as an M.Tech project at **Government Engineering College Thrissur**, April 2026.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🕸️ **Graph Construction** | Models users and relationships as a NetworkX graph |
| 👥 **Community Detection** | Greedy Modularity algorithm groups densely connected users |
| 🫧 **Echo Chamber Detection** | Opinion dominance ratio flags ideologically homogeneous communities |
| 📊 **Centrality Analysis** | Degree, Betweenness, and Closeness centrality per node |
| ⭐ **Influential User Detection** | Identifies top influencers by centrality score |
| 🔗 **Bridge Node Detection** | Finds nodes whose removal disconnects communities |
| 🏚️ **Robustness Evaluation** | Simulates node removal and measures structural impact |
| 🌐 **Interactive Visualization** | PyVis-powered HTML graph with zoom, drag, and explore |
| 📈 **Dashboard & Charts** | Multi-panel Matplotlib dashboard with centrality and adjacency plots |

---

## 🏗️ System Architecture

```
                    ┌─────────────────────────┐
                    │   Social Network Input   │
                    │  Users + Relationships   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Graph Construction    │
                    │       (NetworkX)         │
                    │  Nodes = Users           │
                    │  Edges = Relationships   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Opinion Assignment    │
                    │  Each node → Opinion A  │
                    │              Opinion B  │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Community Detection   │
                    │  Greedy Modularity      │
                    │  Groups densely         │
                    │  connected subgraphs    │
                    └──────┬─────────┬────────┘
                           │         │
              ┌────────────▼──┐  ┌───▼───────────────┐
              │  Echo Chamber │  │  Centrality        │
              │  Detection    │  │  Analysis          │
              │               │  │  · Degree          │
              │  D = dom/total│  │  · Betweenness     │
              │  D ≥ 0.75 →   │  │  · Closeness       │
              │  Echo Chamber │  └───────────┬────────┘
              └──────┬────────┘              │
                     │              ┌────────▼────────┐
                     │              │  Influential     │
                     │              │  User Detection  │
                     │              └────────┬────────┘
                     │                       │
                     └──────────┬────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   Robustness Analysis    │
                    │  Remove top influencer   │
                    │  Measure:                │
                    │  · Connectivity          │
                    │  · Components            │
                    │  · Structural stability  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   Visualization Layer    │
                    └───────────┬─────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
  ┌────────▼──────┐   ┌─────────▼──────┐  ┌─────────▼──────┐
  │ dashboard.png │   │centrality_      │  │social_network  │
  │ (multi-panel) │   │charts.png       │  │    .html       │
  └───────────────┘   │adjacency_       │  │(PyVis HTML)    │
                      │matrix.png       │  └────────────────┘
                      └─────────────────┘
```

---

## 🔬 Key Concepts

### Community Detection — Greedy Modularity

The Greedy Modularity algorithm iteratively merges node pairs that produce the greatest increase in **modularity** — a score measuring how much the community structure exceeds what would be expected in a random graph.

```
         Initial: Each node is its own community
                         │
         Merge pair that increases modularity most
                         │
         Repeat until no improvement is possible
                         │
         Final: Set of densely-connected communities
```

Modularity Q ranges from -1 to 1. Higher Q indicates stronger community structure.

---

### Echo Chamber Detection — Dominance Ratio

For each detected community, the system computes the **opinion dominance ratio D**:

```
         Dominant Opinion Count
D  =  ─────────────────────────────
         Total Community Members

D ≥ 0.75  →  Community classified as ECHO CHAMBER
D < 0.75  →  Community is DIVERSE
```

A community where 75% or more of members share the same opinion is considered an echo chamber — a bubble where dissenting views are structurally absent.

---

### Centrality Measures

| Measure | Formula (conceptual) | Meaning |
|---|---|---|
| **Degree Centrality** | connections(v) / (n - 1) | How many direct connections a node has |
| **Betweenness Centrality** | Fraction of shortest paths passing through v | How critical a node is as a bridge |
| **Closeness Centrality** | (n - 1) / Σ distances(v, u) | How quickly a node can reach all others |

---

### Robustness Analysis

```
Original Graph G
       │
Remove top-degree influencer node v*
       │
Compute G' = G − {v*}
       │
Measure:
  · Is G' still connected?
  · How many components does G' split into?
  · What fraction of nodes are now isolated?
       │
Compare G vs G' → Structural fragility score
```

A network that shatters into many components after removing one node is structurally fragile — heavily dependent on a small number of bridges.

---

## 📤 Generated Outputs

| File | Description |
|---|---|
| `dashboard.png` | Multi-panel analysis dashboard |
| `centrality_charts.png` | Bar charts for degree, betweenness, and closeness centrality |
| `adjacency_matrix.png` | Heatmap of node connectivity |
| `social_network.html` | Interactive PyVis graph (open in any browser) |

---

## 🗂️ Project Structure

```
breaking-the-bubble/
│
├── breaking_the_bubble.py     # Main analysis script
│
├── outputs/
│   ├── dashboard.png
│   ├── centrality_charts.png
│   ├── adjacency_matrix.png
│   └── social_network.html
│
├── screenshots/               # Demo screenshots
├── README.md
└── ARCHITECTURE.md
```

---

## ⚙️ Installation & Usage

### Install Dependencies

```bash
pip install networkx matplotlib numpy pyvis
```

### Run the Analysis

```bash
python breaking_the_bubble.py
```

All output files are generated in the `outputs/` directory. Open `social_network.html` in any browser for the interactive graph.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.x |
| **Graph Construction & Analysis** | NetworkX |
| **Visualization (static)** | Matplotlib |
| **Visualization (interactive)** | PyVis |
| **Numerical Operations** | NumPy |
| **Development Tools** | VS Code, GitHub, Overleaf |

---

## 💻 Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Processor | Intel Core i3 | Intel Core i5/i7 |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB | 1 GB SSD |

---

## 🔮 Future Enhancements

- [ ] Real-world datasets (Twitter/X API, Reddit, Facebook Graph API)
- [ ] Dynamic network analysis (temporal evolution of echo chambers)
- [ ] Real-time social network monitoring dashboard
- [ ] ML-based influence prediction (GNN, Node2Vec)
- [ ] Advanced community detection (Louvain, Leiden algorithm)
- [ ] Opinion spread simulation (voter model, SIR model)
- [ ] Multi-opinion support (beyond binary A/B)

---

## 👨‍💻 Author

**Abdul Haris H**
M.Tech — Computer Science and Engineering
Government Engineering College Thrissur
April 2026

---

## 📄 License

This project is developed for academic and educational purposes.

---

<div align="center">
  <sub>Built with ❤️ using NetworkX, Matplotlib, and PyVis</sub>
</div>