# Master-Prep

Personal study notes for strengthening electrical engineering and computer science fundamentals before graduate study, with an emphasis on embedded systems and the hardware–software interface.

This repository connects **data structures, digital logic, computer organization, and computer architecture** through explanations, worked examples, exercises, and references.

## Start Here

| Topic | Notes | Focus | Current scope |
| --- | --- | --- | --- |
| Data Structures | [Data Structures notes.md](Data%20Structures%20notes.md) | Data representation, common structures, and programming examples | Existing study draft; not audited as part of the architecture update |
| Logic Design | [Logic_Design.md](Logic_Design.md) | Boolean algebra, K-maps, combinational/sequential circuits, counters, FSMs, memory, and HDL | CH0–CH9 completed as foundation-to-intermediate study notes, with worked examples and sources |
| Computer Organization and Design | [Computer_Organization_and_Design.md](Computer_Organization_and_Design.md) | Representation, RV32I, datapaths, control, pipelines, caches, and I/O | Structured foundation notes with worked examples and sources |
| Computer Architecture | [Computer_Architecture.md](Computer_Architecture.md) | Performance, Amdahl's law, prediction, memory systems, multicore, and Roofline | Foundation-to-intermediate notes, with introductory advanced topics |

**Language:** This README is in English. The logic design, architecture, and organization notes use Traditional Chinese explanations with English technical terms. The data structures draft contains both languages.

## ESE Core Preparation Notes

The [ESE Core Study Guide](ESE_Core/README.md) adds seven Traditional Chinese notes with English technical terms, researched on **September 29, 2026 (Asia/Taipei)**.

| Course mapping | Notes |
| --- | --- |
| ECEN 5613 | [Embedded System Design](ESE_Core/01_Embedded_System_Design.md) |
| ECEN 5623 | [Real-Time Embedded Systems](ESE_Core/02_Real_Time_Embedded_Systems.md) |
| ECEN 5813 + 5713 | [Embedded Software and Advanced Embedded Linux](ESE_Core/03_Embedded_Software_and_Linux.md) |
| ECEN 5823 + 5773 extension | [IoT Firmware and Industrial IoT](ESE_Core/04_IoT_Firmware_and_Industrial_IoT.md) |
| ECEN 5833 | [Low Power Embedded Design](ESE_Core/05_Low_Power_Embedded_Design.md) |
| ECEN 5853 | [Embedding Sensors and Motors](ESE_Core/06_Embedding_Sensors_and_Motors.md) |
| ECEN 5863 | [Programmable Logic Embedded Design](ESE_Core/07_Programmable_Logic_Embedded_Design.md) |

The official ESE page currently describes choosing **any five core courses**, not taking all seven as individually mandatory courses. This independent study guide covers the seven courses in the supplied list; it is not an official syllabus or a substitute for the applicable catalog and advisor-approved degree plan.

Each note includes explanations, explicit assumptions, original textbook-style examples, applications, exercises with answers, and sources. Public textbook examples are identified separately. The software note combines the introductory and advanced courses; Industrial IoT is a related extension rather than a claimed official two-course sequence.

[Eight Mac-first project specifications](ESE_Core/Projects.md) provide interfaces, milestones, acceptance tests, deliverables, and optional hardware upgrades. All complete projects are **planned**. Six MVPs prioritize native macOS; Linux-specific work uses a suitable Linux environment. The public Spring 2026 ECEN5713 page still specifies an x86-64 host, so an M2 self-study workflow is not claimed to match the supported classroom environment.

Small verification examples are included:

```sh
python3 ESE_Core/examples/check_models.py
cc -std=c11 -Wall -Wextra -Werror ESE_Core/examples/firmware_core.c -o /tmp/firmware_core
/tmp/firmware_core
```

These were run in the preparation environment: numerical checks, RTA pass/fail cases, 65,536 saturating-adder reference inputs, and C decoding/overflow/ring-buffer tests. No new RTL simulation, Buildroot build, full network project, or hardware measurement is claimed. The sensor note discloses the limited retrieval available for the CTMS motor example.

## Learning Goals

- Explain how source-level operations become instructions and hardware activity.
- Trace integer representations, register values, memory addresses, and simple instruction sequences.
- Understand the roles of the datapath, control unit, pipeline, cache, and virtual memory.
- Evaluate performance using explicit assumptions, equations, and meaningful baselines.
- Relate these ideas to embedded projects and Raspberry Pi development.
- Build the habit of checking specifications and reproducing calculations instead of memorizing unsupported claims.

## Recommended Learning Path

1. **Programming and digital logic:** Review arrays and pointers, then work through Logic Design CH0–CH7: representation, Boolean algebra, combinational circuits, timing, counters, and FSMs. CH8–CH9 introduce memory, HDL, and implementation concerns.
2. **Organization, Sections 2–5:** Study integer/floating-point representation, RV32I instructions, arrays, loops, and calling conventions.
3. **Organization, Sections 6–9:** Follow datapaths and control signals; work through pipeline hazards, cache fields, and I/O mechanisms.
4. **Architecture, Sections 2–6:** Calculate CPU time, speedup, AMAT, and address translation.
5. **Architecture, Sections 7–9:** Introduce coherence, consistency, parallelism, accelerators, and embedded-system trade-offs.
6. **Practice and verify:** Complete the exercises, run the small code examples, and record your own measurements.

The organization and architecture documents intentionally overlap at their boundary: **organization** explains how the machine works; **architecture** uses that foundation to reason about design choices and performance. Course titles vary, so this is a reading convention for this repository.

## What the New Notes Include

- Linked tables of contents and consistent section numbering.
- Definitions, formulas with units, and clearly stated modeling assumptions.
- The architecture and organization pair contains **22 original textbook-style worked examples**, plus concise discussions of two identified examples from the public textbook *Dive Into Systems*.
- Logic Design adds **28 original textbook-style worked examples**, 15 practice questions with answers, and an independently derived D-flip-flop solution to the enabled counter specification identified as Plantz Chapter 5, Example 5-a.
- Practice questions with expandable answers.
- A complete C bit/byte inspection example and a Python direct-mapped cache model.
- Logic truth tables, K-maps, FSM diagrams, a Python verification script, and a SystemVerilog sequence detector with explicit validation limits.
- RV32I assembly examples and a register-by-register walkthrough.
- Practical connections to image processing, sensor systems, memory layout, and Raspberry Pi development.
- Section-level source identifiers and reference tables.

## Sources and Verification Policy

The new notes were researched against publicly accessible primary sources on **September 26, 2026**:

| Resource | Why it is used |
| --- | --- |
| [MIT OpenCourseWare 6.004](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Digital systems, processors, timing, and pipelines |
| [MIT 6.004 tutorial problems and solutions](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/pages/tutorial-problems/) | Public exercises for independent practice |
| [Cornell CS 3410](https://www.cs.cornell.edu/courses/cs3410/2026sp/) | Public explanations of representation, RISC-V, caches, virtual memory, and concurrency |
| [RISC-V ISA specifications](https://docs.riscv.org/reference/isa/v20240411/unpriv/rv32.html) and [psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/) | Instruction semantics and calling conventions |
| [Dive Into Systems](https://diveintosystems.org/book/index.html) | Public textbook explanations and identified worked examples |
| [Robert G. Plantz's public textbook](https://bob.cs.sonoma.edu/IntroCompOrg-x64/bookch5.html) and [All About Circuits](https://www.allaboutcircuits.com/textbook/digital/chpt-8/karnaugh-maps-truth-tables-boolean-expressions/) | Boolean logic, counters, K-maps, and sequential-circuit explanations |
| [AMD UG901](https://docs.amd.com/r/2023.2-English/ug901-vivado-synthesis/Always-Procedures), [Altera design guidance](https://docs.altera.com/r/docs/683323/18.1/intel-quartus-prime-standard-edition-user-guide-design-recommendations/metastability-analysis-in-the-intel-quartus-prime-software), and [TI SCEA094](https://www.ti.com/document-viewer/lit/html/SCEA094) | HDL, synchronization, reset, and switch-debounce implementation concerns |
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
| Python logic checks | Python 3 | Copy the complete snippet in Logic Design §9.3 into `logic_checks.py`, then run `python3 logic_checks.py` |
| SystemVerilog sequence detector | A SystemVerilog simulator; a target FPGA toolchain for implementation | Logic Design §9.2 provides RTL and expected behavior; a complete testbench and board project are planned |
| RV32I assembly | A suitable RISC-V assembler and execution environment | The notes give instruction/function examples; a full toolchain tutorial is not yet included |

**Architecture distinction:** Raspberry Pi 3 uses Arm hardware. The RV32I examples are for learning and do not run natively on the Pi or an Apple Silicon Mac.

The small C and Python examples and numerical worked examples were checked during preparation. The RV32I function was traced against its stated assumptions; it was not presented as a board-tested application. No real-device performance measurements are included.

The logic Python checks passed K-map/BCD equivalence, all eight FSM state/input combinations, and all **8,191 bitstreams of lengths 0–12** against an independent substring matcher. These checks validate the mathematical model, not the SystemVerilog source. RTL simulation, synthesis, static timing analysis, and FPGA testing are **planned**.

## Repository Contents

| File | Purpose |
| --- | --- |
| `README.md` | Overview, reading order, and source policy |
| `Data Structures notes.md` | Existing data structures notes |
| `Logic_Design.md` | CH0–CH9 logic design notes, worked examples, practice answers, and a source map |
| `Computer_Organization_and_Design.md` | Foundations and implementation mechanisms |
| `Computer_Architecture.md` | Performance and architectural trade-offs |

This is primarily a notes repository. `ESE_Core/examples/` contains small executable verification examples; other illustrative code is embedded in Markdown. Complete project implementations, an FPGA board project, and measured benchmark datasets are planned.

## Suggested Next Steps

These are study suggestions, not completed work:

- [ ] Add a SystemVerilog testbench and reproducible simulator workflow for the sequence detector.
- [ ] Implement the proposed debounced mod-6 counter project and document pin assignments, timing constraints, and hardware results.
- [ ] Review and test the earlier data structures examples.
- [ ] Work through the new paper-and-pencil exercises before viewing the answers.
- [ ] Set up a documented RV32I simulation workflow.
- [ ] Extend the cache model to set associativity and replacement policies.
- [ ] Add reproducible measurements from actual hardware, including setup details and correctness checks.

## Corrections and Attribution

When correcting a note, identify the section, explain the error, and attach a reliable source or reproducible calculation. Keep architecture-specific assumptions explicit.

Linked resources remain subject to their authors' terms. Linking a textbook or course does not grant permission to redistribute its full contents. This update does not add or imply a repository-wide license.
