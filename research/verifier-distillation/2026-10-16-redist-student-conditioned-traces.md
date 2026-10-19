# Beyond the Answer: Student-Conditioned Trace Construction for Reasoning Distillation

## 基本信息

- 方法名：ReDiST
- 作者：Shaoang Li, Yanhang Shi, Yufei Li, Mingfu Liang, Frank Shyu, Sandeep Pandey, Luke Simon, Xi Liu, Jian Li
- 首次公开日期：2026-10-16
- 版本日期：2026-10-16（v1）
- arXiv：2610.23831
- 原始论文：https://arxiv.org/abs/2610.23831
- DOI：https://doi.org/10.48550/arXiv.2610.23831
- 代码：未发现公开代码链接

## 一句话结论

正确答案附带的推理轨迹不一定适合特定 student；从 student 自己的尝试出发修订或修复，再由 student-matched reader 筛选，能产生更可学且跨分布更稳的蒸馏目标。

## 真正新增的内容

**论文原文结论：** ReDiST 同时优化轨迹的中间内容和对目标 student 的可访问性，不把“答案正确”当成“教学有效”。它从 student drafts 出发，对答对草稿做证据约束修订、对答错草稿用已验证答案做修复提示，再由冻结的 student-matched reader 以答案恢复和 verified-answer probability 排序。

**分析推断：** 这是 student-generated critique states 的强直接基线：训练状态应围绕 student 实际错误构造，而非把 teacher 的理想 CoT 原样塞给 student。

## 核心方法

1. student 每题生成多个候选草稿。
2. 有正确草稿时，在不额外泄露答案的条件下依据证据修订；无正确草稿时，用 verified answer 作为检查提示进行修复。
3. 冻结的 student-matched reader 根据问题、证据与轨迹评估答案恢复和正确答案概率。
4. 选择后的轨迹与答案共同蒸馏，并增加 answer-token auxiliary loss，防止长轨迹淹没终局答案信号。
5. 全部构造与筛选离线完成，推理时只使用蒸馏后的 student。

## 关键实验结果

**论文原文：** 在 Qwen3-8B 的报告结果中，ReDiST 在八项展示指标上取得最高点估计；MuSiQue EM 为 58.4%，最接近的 MBT-R 为 57.9%，该小差异未被 bootstrap 结果明确区分；跨域 2Wiki EM 为 68.6%，MBT-R 为 63.3%。论文还指出，不同监督配方在源域与迁移域的排序会变化。

**分析推断：** 更可信的信号是跨域差异，而非源域 0.5 点领先；它说明“可教性筛选”需要独立迁移评测，不能只看训练分布上的答案恢复率。

## 证据质量与局限

- 有完整方法、多个 QA 基准和迁移比较，且明确承认小幅源域差异未被统计区分。
- 主要是离线 QA 蒸馏，不是长时程工具 Agent 的在线状态分布。
- reader 与 student 同构可能带来共盲区；verified answer 能保证终局，但不能自动保证每个中间关系都有证据。
- 编辑器、reader、训练 student 之间的同源性需在 sealed split 上审计。

## 最接近的相关工作

- EquiReview-R、PaperDoctor 的证据化 critique 修订；
- Critique-Conditioned OPD；
- DENSE 的证据与未完成义务轨迹压缩；
- MedSNIP 对 verifier 粒度的分析；
- outcome-only / answer-only distillation 与 trace rewriting。

## 如何复用或推进 LLM-as-a-Verifier

把 reader 的标量排序扩展为三路输出：`supported`、`useful_but_incomplete`、`unsupported`，并为每个 critique span 附来源指针。只蒸馏通过环境或检索证据门控的部分，同时保留 reader 的分布而非单一最高分。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD：** teacher score 应乘以 student-specific teaching-utility score。
- **A/B/T 与序数分布：** 对多个修订候选做 pairwise A/B/T，再保留 reader 的序数后验。
- **真值门控：** 用工具执行、测试或来源证据验证 critique，而不是仅用正确终局答案。
- **critique states：** 优先从 student 当前 rollout 生成、修订和筛选 critique。
- **高熵探索：** 不把唯一“漂亮轨迹”作为目标；保留多个同样可验证、但策略不同的候选。
- **sealed eval：** 分开报告源域、跨任务迁移、不同 student 家族和独立 verifier 的结果。
