# Reading list

Selection criteria: survey (or evaluation) papers on memory for LLM agents, posted or substantially revised between April and November 2026, from established groups, that together cover the taxonomy, techniques, evaluation and safety of agent memory.

## Surveys

1. **Memory-Centric Continual Learning for AI Agents** (main paper)
   D. Li, Z. Chen, … B. Hu, X. Ji, M. Zhang (28 authors). Harbin Institute of Technology (Shenzhen), Shenzhen Loop Area Institute, Tsinghua University, Southeast University, China Telecom Xingchen AGI Lab, Huawei.
   arXiv [2610.29357](https://arxiv.org/abs/2610.29357), Oct 21, 2026.
   *Used for:* the WHERE / WHAT / HOW taxonomy, the two-loop lifecycle, the four-gate evaluation cascade, and the stateful-minus-reset and reader-policy ablations.

2. **Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents**
   T. Ding, A. Nannapaneni, B. Liu, L. Zhang. arXiv [2606.30306](https://arxiv.org/abs/2606.30306), Jun 29, 2026.
   *Used for:* the 435-work lifecycle coding, six governance axes, five invariants, and the AOEP-v0 scorecard.

3. **Memory for Large Language Models**
   S. Zhoubian, D. Zhang, E. Kharlamov, J. Tang. Tsinghua University, National University of Singapore, Bosch AI. arXiv [2607.25380](https://arxiv.org/abs/2607.25380), Jul 28, 2026.
   *Used for:* model-level memory (implicit vs explicit, online vs offline, short vs long term).

4. **From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms**
   J. Luo, Y. Tian, C. Cao, Z. Luo, H. Lin, K. Li, C. Kong, R. Yang, J. Ma. HKBU, SCNU, HKUST, NUS, USTB. arXiv [2605.06716](https://arxiv.org/abs/2605.06716), May 7, 2026. ACL 2026 Findings.
   *Used for:* the Storage → Reflection → Experience progression.

5. **A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle**
   Z. Lin, X. Hao, R. Fu, S. Cui, K. Chen, C. Li, Z. Li, F. Xiong. MemTensor, SJTU, PKU, HKUST (Guangzhou). arXiv [2604.16548](https://arxiv.org/abs/2604.16548), Apr 17, 2026; v6 Nov 20, 2026. Expanded EMNLP 2026 paper.
   *Used for:* the six-phase attack/defense lifecycle and Verifiable Memory Governance.

## Evaluation papers (leaderboard and ablations)

6. **Harness the Memory: A Holistic Evaluation of Memory Substrates in Memory Agents**
   W.-C. Huang et al. (incl. K.-W. Chang, P. S. Yu, A. Caliskan). UIC, UW, McGill, MBZUAI, UCLA. arXiv [2608.15008](https://arxiv.org/abs/2608.15008), v2 Nov 4, 2026.

7. **When Does Memory Help? A Cost-Aware Evaluation of Long-Term Memory in Tool-Using LLM Agents (MERIT)**
   S. Mishra, S. Mishra. arXiv [2609.05441](https://arxiv.org/abs/2609.05441), 2026.

## Reference papers for techniques and benchmarks

- Mem0, arXiv [2504.19413](https://arxiv.org/abs/2504.19413) (LoCoMo results, Table 2)
- Zep, arXiv [2501.13956](https://arxiv.org/abs/2501.13956) (LongMemEval results, Table 2)
- LongMemEval, arXiv [2410.10813](https://arxiv.org/abs/2410.10813) (ICLR 2025)
- MemGPT, arXiv [2310.08560](https://arxiv.org/abs/2310.08560)
