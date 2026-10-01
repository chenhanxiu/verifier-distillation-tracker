# Semifactual Credit-Augmented Policy Optimization

- **作者**：Junshu Pan, Zhizhang Fu, Shulin Huang, Yiran Ding, Zifan Cheng, Wenqi Shao, Qiaosheng Zhang, Yue Zhang
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40360
- **代码**：https://github.com/DtYXs/SCAPO

## 一句话结论

SCAPO 用保持题意与答案不变的 semifactual 扰动检测 token 概率漂移，并削弱不稳定 token 的优势，AIME 2024–2026 比 GRPO 高 4.17–5.63 点。

## 真正新增的内容

【论文原文】GRPO 把同一 outcome advantage 给所有 response token，可能同时强化有用推理与无关提示依赖。SCAPO 对固定回答施加语义不变干预，按 token 稳定性重分配早期训练信用；稳定本身不额外加分，只削弱相对不稳定 token。

【分析推断】这是一种“反事实不变性 verifier”，可作为 score-level 蒸馏中 teacher 信号的可靠性系数。

## 核心方法

构造不改变问题和答案的 prompt semifactual；测量固定 response 下 token 概率漂移；归一化稳定性并降低高漂移 token advantage。

## 关键实验结果

【论文原文】Qwen3-4B-Base 与 1.7B-Base 在 AIME 2024–2026 相对 GRPO分别提升 5.63、4.17 个百分点；多数数学基准及全部 OOD 基准为比较方法最优。

## 证据质量与局限

有两个尺度、OOD 与公开代码；但任务限于数学，semifactual 生成是否真正语义等价是关键假设，未报告 Agent 环境干预。

## 最接近的相关工作

IWD、MAWILE、Beyond Aggregate Scores、UECR-GRPO、DCSD。

## 如何复用或推进 LLM-as-a-Verifier

对 Agent 状态做保持任务约束不变的表述、顺序与界面扰动，测量 verifier score/critique 是否稳定；把不稳定度用作蒸馏降权而非正奖励。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：以稳定性折扣 verifier 分数，避免表面特征主导。
- **A/B/T 与序数分布**：若 A/B 在等价扰动下翻转，则改标 T 并扩大不确定性。
- **硬真值门控**：只接受通过程序化等价检查的 semifactual。
- **student-generated critique states**：critique 要在语义保持扰动下保持因果结论。
- **高熵分叉**：稳定性只削弱伪信号，不把高熵本身当错误。
- **sealed eval**：冻结未见扰动族，防止对已知 metamorphic test 过拟合。
