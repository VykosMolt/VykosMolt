<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/card-dark.svg?v=880eebf5">
    <img src="assets/card-light.svg?v=21033788" alt="Jan Kirin — ML researcher / SWE. Arch Linux, Hyprland, Neovim. Research: looped and recurrent language models, interpretability, agent learning. Selected work: SemABI, Operational Proto-Introspection, Curunír." width="880">
  </picture>
</p>

<p align="center">
  <a href="mailto:vykos@tutamail.com">Email</a>
  ·
  <a href="https://github.com/VykosMolt">GitHub</a>
  ·
  <a href="https://hr.linkedin.com/in/jan-kirin-833074422">LinkedIn</a>
  ·
  <a href="https://scholar.google.com/citations?user=JDFRr8sAAAAJ">Google Scholar</a>
  ·
  <a href="https://arxiv.org/search/?query=Jan+Kirin&searchtype=author&abstracts=show&order=-announced_date_first&size=50">arXiv</a>
</p>

---

## Selected work

### [SemABI](https://github.com/VykosMolt/semabi)

**Learning what an application does by operating it.**

SemABI interacts with an unfamiliar web application through an ordinary browser and
learns a typed relational model of what the application contains and what its controls do.

No source. No API. No schema. No documentation. No demonstrations. No predefined action
vocabulary. The learner itself uses no language model.

It is an attempt to answer a simple but nontrivial question:

> Can an agent recover the semantics of an unfamiliar application purely by interacting
> with its interface?

---

### [Operational Proto-Introspection](https://arxiv.org/abs/2607.18553) · [code](https://github.com/VykosMolt/Branching-Looped-Transformer)

Research into what looped language models know about the quality of their own ongoing
computation, where those signals become readable, and whether an external intervention
can actually turn that readout into better outcomes.

The work spans hidden-state process-quality taps, executable branching over recurrent
states, recurrence-depth analysis, cross-model replication, and the boundary between
**readable internal information** and **usable control**.

---

### [Curunír](https://github.com/VykosMolt/Curunir)

An intelligence workbench that will not let a conclusion outrun its evidence.

Curunír is built around explicit provenance, inspectable claims, reproducible evidence,
and adversarial review rather than treating an agent's final answer as the artifact.

---

### [Lifetime Meta-Learning](https://github.com/VykosMolt/Lifetime-Meta-Learning)

Experiments on whether recurrent representations are causally **writable**, rather than
merely readable.

The broader question is whether computation can be useful not only because it improves
the current answer, but because it improves what the model is able to learn afterwards.

---

### [looped-wiki](https://github.com/VykosMolt/looped-wiki)

An agent-first index of the literature around recurrent and looped models.

The basic unit is a **claim instance**, not a paper: findings, mechanisms, evidence,
relationships, and limitations are represented separately so agents can reason across
the literature rather than merely retrieve documents.

---

## Research

My main interests are recurrent / looped language models, representation-level
evaluation, interpretability, latent reasoning, agent learning, and the relationship
between **reading** an internal representation and **controlling** computation through it.

### Papers

**[Operational Proto-Introspection in Looped Language Models](https://arxiv.org/abs/2607.18553)**  
Process-quality taps, executable branching, recurrence-depth analysis, and the
readout–control boundary.

**[Relational Preference Encoding in Looped Transformer Internal States](https://arxiv.org/abs/2604.09870)**  
Earlier work on relational signals in Ouro's recurrent states. The associated repository
contains the correction record and subsequent evaluator work.

### Research code

| Project | What it is |
|---|---|
| **[Branching-Looped-Transformer](https://github.com/VykosMolt/Branching-Looped-Transformer)** | Experimental substrate behind Operational Proto-Introspection: hidden-state probes, branch/carry/prune machinery, control experiments, and recurrent-depth analysis. |
| **[Hidden-State-Evaluator](https://github.com/VykosMolt/Hidden-State-Evaluator)** | Pairwise evaluator experiments over internal states of Ouro-2.6B-Thinking, including the correction trail for the original preference-evaluation result. |
| **[JLens-Ouro](https://github.com/VykosMolt/JLens-Ouro)** | Jacobian-lens experiments against the raw logit lens inside a recurrent loop. |
| **[One-Concept-Multiple-Geometries](https://github.com/VykosMolt/One-Concept-Multiple-Geometries)** | Tests how different corpus operators recover different geometries from the same underlying concept. |
| **[Lifetime-Meta-Learning](https://github.com/VykosMolt/Lifetime-Meta-Learning)** | Experiments on writable recurrent representations and learning-time credit. |
| **[looped-wiki](https://github.com/VykosMolt/looped-wiki)** | Structured literature index for looped / recurrent models, organized around claims rather than documents. |

---

## Other projects

<details>
<summary><strong>Systems & desktop</strong></summary>

<br>

| Project | What it is |
|---|---|
| **[Curunír](https://github.com/VykosMolt/Curunir)** | Evidence-grounded intelligence and research workbench. |
| **[omarchy-desktop](https://github.com/VykosMolt/omarchy-desktop)** | The Omarchy Quattro desktop reconstructed as an ordinary Arch Linux session. |
| **[walltone](https://github.com/VykosMolt/walltone)** | Rotates a wallpaper and restyles Kitty from the same image. |

</details>

<details>
<summary><strong>Things to read or play</strong></summary>

<br>

| Project | What it is |
|---|---|
| **[Glasshouse](https://github.com/VykosMolt/Glasshouse)** | Two offline browser mysteries at Bellwether Conservatory, 1932. Python, no dependencies, no network. |
| **[picture-books](https://github.com/VykosMolt/picture-books)** | Interactive technical picture books: *Hidden States*, *Free Fall*, and *The Red Thread*. |
| **[Ink-Handwritting-Studio](https://github.com/VykosMolt/Ink-Handwritting-Studio)** | A handwriting generator built to handle real documents. |

</details>

---

## Open source

I also contribute patches upstream rather than keeping every change in a standalone
project.

Forks retained primarily to carry contributions:

[nixpkgs](https://github.com/VykosMolt/nixpkgs)
·
[archinstall](https://github.com/VykosMolt/archinstall)
·
[winget-pkgs](https://github.com/VykosMolt/winget-pkgs)
·
[cline](https://github.com/VykosMolt/cline)
·
[odysseus](https://github.com/VykosMolt/odysseus)
·
[omarchy](https://github.com/VykosMolt/omarchy)

tsCircuit:
[core](https://github.com/VykosMolt/core)
·
[circuit-json](https://github.com/VykosMolt/circuit-json)
·
[circuit-json-to-kicad](https://github.com/VykosMolt/circuit-json-to-kicad)

---

<details>
<summary><strong>Retired / archived work</strong></summary>

<br>

**[Hunter-Seeker-v2](https://github.com/VykosMolt/Hunter-Seeker-v2)**  
Transactional non-LLM ARC-AGI-3 agent; the compact post-erratum rebuild.

**[Hunter-Seeker-v1](https://github.com/VykosMolt/Hunter-Seeker-v1)**  
The earlier Stockfish-style implementation with its nineteen-mixin stack.

</details>

---

<p align="center">
  <a href="mailto:vykos@tutamail.com">vykos@tutamail.com</a>
  ·
  <a href="https://github.com/VykosMolt">GitHub</a>
  ·
  <a href="https://hr.linkedin.com/in/jan-kirin-833074422">LinkedIn</a>
  ·
  <a href="https://scholar.google.com/citations?user=JDFRr8sAAAAJ">Scholar</a>
  ·
  <a href="https://arxiv.org/search/?query=Jan+Kirin&searchtype=author&abstracts=show&order=-announced_date_first&size=50">arXiv</a>
</p>
