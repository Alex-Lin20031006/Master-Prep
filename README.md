# Master-Prep

Personal study notes for strengthening electrical engineering and computer science fundamentals before graduate study, with an emphasis on embedded systems and the hardware–software interface.

This repository connects **data structures, digital logic, computer organization, and computer architecture** through explanations, worked examples, exercises, and references.

## Start Here

| Topic | Notes | Focus | Current scope |
| --- | --- | --- | --- |
| Data Structures | [Data Structures notes.md](Data%20Structures%20notes.md) | Data representation, common structures, and programming examples | Existing study draft; not audited as part of the architecture update |
| Logic Design | [Logic_Design.md](Logic_Design.md) | Number systems, binary arithmetic, gates, and adders | Introductory material is present; later chapters are outlines |
| Computer Organization and Design | [Computer_Organization_and_Design.md](Computer_Organization_and_Design.md) | Representation, RV32I, datapaths, control, pipelines, caches, and I/O | Structured foundation notes with worked examples and sources |
| Computer Architecture | [Computer_Architecture.md](Computer_Architecture.md) | Performance, Amdahl's law, prediction, memory systems, multicore, and Roofline | Foundation-to-intermediate notes, with introductory advanced topics |

**Language:** This README is in English. The new architecture and organization notes use Traditional Chinese explanations with English technical terms. Existing notes contain both languages.

## Learning Goals

- Explain how source-level operations become instructions and hardware activity.
- Trace integer representations, register values, memory addresses, and simple instruction sequences.
- Understand the roles of the datapath, control unit, pipeline, cache, and virtual memory.
- Evaluate performance using explicit assumptions, equations, and meaningful baselines.
- Relate these ideas to embedded projects and Raspberry Pi development.
- Build the habit of checking specifications and reproducing calculations instead of memorizing unsupported claims.

## Recommended Learning Path

1. **Programming and representation:** Review arrays, pointers, binary numbers, hexadecimal, and basic Boolean logic.
2. **Organization, Sections 2–5:** Study integer/floating-point representation, RV32I instructions, arrays, loops, and calling conventions.
3. **Organization, Sections 6–9:** Follow datapaths and control signals; work through pipeline hazards, cache fields, and I/O mechanisms.
4. **Architecture, Sections 2–6:** Calculate CPU time, speedup, AMAT, and address translation.
5. **Architecture, Sections 7–9:** Introduce coherence, consistency, parallelism, accelerators, and embedded-system trade-offs.
6. **Practice and verify:** Complete the exercises, run the small code examples, and record your own measurements.

The two new documents intentionally overlap at their boundary: **organization** explains how the machine works; **architecture** uses that foundation to reason about design choices and performance. Course titles vary, so this is a reading convention for this repository.

## What the New Notes Include

- Linked tables of contents and consistent section numbering.
- Definitions, formulas with units, and clearly stated modeling assumptions.
- **22 original textbook-style worked examples**, plus concise discussions of two identified examples from the public textbook *Dive Into Systems*.
- Practice questions with expandable answers.
- A complete C bit/byte inspection example and a Python direct-mapped cache model.
- RV32I assembly examples and a register-by-register walkthrough.
- Practical connections to image processing, sensor systems, memory layout, and Raspberry Pi development.
- Section-level source identifiers and reference tables.

## Sources and Verification Policy

The new notes were researched against publicly accessible primary sources on **September 27, 2026**:

| Resource | Why it is used |
| --- | --- |
| [MIT OpenCourseWare 6.004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Digital systems, processors, timing, and pipelines |
| [MIT 6.004 tutorial problems and solutions](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/pages/tutorial-problems/) | Public exercises for independent practice |
| [Cornell CS 3410](https://www.cs.cornell.edu/courses/cs3410/2026sp/) | Public explanations of representation, RISC-V, caches, virtual memory, and concurrency |
| [RISC-V ISA specifications](https://docs.riscv.org/reference/isa/v20240411/unpriv/rv32.html) and [psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/) | Instruction semantics and calling conventions |
| [Dive Into Systems](https://diveintosystems.org/book/index.html) | Public textbook explanations and identified worked examples |
| [MIT 6.5900, Fall 2023](https://csg.csail.mit.edu/6.5900F23/lecnotes.html) | Advanced pipelines, prediction, coherence, and consistency |
| [Berkeley Roofline report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.html) | Compute-versus-memory performance modeling |
| [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/processors.html) and [Linux DMA documentation](https://docs.kernel.org/core-api/dma-api-howto.html) | Hardware context and device-memory interfaces |

### How to interpret examples

- **Original textbook-style examples** are newly written exercises, not claimed to be questions or official solutions from a commercial textbook.
- **Public textbook examples** identify their source and section; the notes provide short discussions rather than reproducing chapters or illustrations.
- The Patterson–Hennessy *Computer Organization and Design RISC-V Edition*, second edition, reading map is based on the [publisher's public table of contents](https://shop.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6), not an asserted review of its paid full text.
- Teaching assumptions—such as a five-stage pipeline, 4 KiB pages, or a particular cache geometry—are not universal hardware specifications.
- References provide an audit trail, not a guarantee that every teaching simplification applies to every processor. Check the relevant ISA and processor manual for implementation-specific work.

## Using the Notes

Read the Markdown files directly on GitHub. No installation is required for reading; GitHub renders the tables, equations, diagrams, and expandable answers.

To keep a local copy:

```sh
git clone --branch Study-Notes https://github.com/Alex-Lin20031006/Master-Prep.git
cd Master-Prep
```

For the optional examples:

| Example | Requirement | Instructions |
| --- | --- | --- |
| C bit/byte inspection | C11-compatible compiler | Copy the complete snippet and follow Organization §10.1 |
| Python cache model | Python 3 | Copy the complete snippet and follow Architecture §10.1 |
| RV32I assembly | A suitable RISC-V assembler and execution environment | The notes give instruction/function examples; a full toolchain tutorial is not yet included |

**Architecture distinction:** Raspberry Pi 3 uses Arm hardware. The RV32I examples are for learning and do not run natively on the Pi or an Apple Silicon Mac.

The small C and Python examples and numerical worked examples were checked during preparation. The RV32I function was traced against its stated assumptions; it was not presented as a board-tested application. No real-device performance measurements are included.

## Repository Contents

| File | Purpose |
| --- | --- |
| `README.md` | Overview, reading order, and source policy |
| `Data Structures notes.md` | Existing data structures notes |
| `Logic_Design.md` | Existing logic design notes and chapter outline |
| `Computer_Organization_and_Design.md` | Foundations and implementation mechanisms |
| `Computer_Architecture.md` | Performance and architectural trade-offs |

This is a notes repository. Code is currently embedded in the Markdown documents; there are no standalone labs, RTL implementations, or benchmark datasets in this update.

## Suggested Next Steps

These are study suggestions, not completed work:

- [ ] Complete the remaining Logic Design chapters.
- [ ] Review and test the earlier data structures examples.
- [ ] Work through the new paper-and-pencil exercises before viewing the answers.
- [ ] Set up a documented RV32I simulation workflow.
- [ ] Extend the cache model to set associativity and replacement policies.
- [ ] Add reproducible measurements from actual hardware, including setup details and correctness checks.

## Corrections and Attribution

When correcting a note, identify the section, explain the error, and attach a reliable source or reproducible calculation. Keep architecture-specific assumptions explicit.

Linked resources remain subject to their authors' terms. Linking a textbook or course does not grant permission to redistribute its full contents. This update does not add or imply a repository-wide license.
