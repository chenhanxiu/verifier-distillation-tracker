# OPDArena: Understanding Learning and Forgetting in On-Policy Distillation

- **作者**：Yuanze Xu、Tianzhu Ye、Hui Sun、Wenhui Wang、Li Dong、Furu Wei
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.25651
- **arXiv ID**：2610.25651
- **DOI**：https://doi.org/10.48550/arXiv.2610.25651
- **代码/项目**：https://github.com/StellarCurtain/OPDArena

## 一句话结论

teacher 的后训练来源决定 OPD 是否遗忘：RLVR teacher 更能兼顾目标学习与能力保持，而 SFT teacher 更易造成通用能力损失。

## 真正新增的内容

把 SFT、RLVR、OPD 放进同一五模型评测框架，同时测目标学习、通用能力保持和预测分布变化。

## 核心方法

比较多种 teacher 来源与后训练方法，并区分 in-domain 与 OOD 分布位移，分析 teacher 相对预训练 student 新增的信息如何集中更新。

## 关键实验结果

论文发现 RLVR teacher 的 student 在提升数学能力时保留更多既有能力；跨方法看，OOD 分布变化与遗忘的正相关比 in-domain 变化更稳定。

## 证据质量与局限

覆盖五个预训练模型和多类 teacher，代码公开；但摘要未给出统一效应量，相关性也不能单独证明分布位移导致遗忘。

## 最接近的相关工作

与 RetireOPD、RISE、Coupled Calibration and Learning 及持续学习中的遗忘审计最接近。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 蒸馏的评测拆成目标域 score、OOD calibration、pairwise 排序稳定性与 sealed task success，避免只看训练域 judge 分数。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有路线应把 teacher checkpoint 类型设为一等实验变量，并在每轮 OPD 后固定跑 OOD sealed suite；若目标分数上升而 OOD 位移陡增，应降低蒸馏权重或退休 teacher。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
