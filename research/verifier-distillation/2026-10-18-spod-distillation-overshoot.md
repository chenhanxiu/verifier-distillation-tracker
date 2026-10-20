# Beyond the Teacher: Understanding and Preserving Distillation Overshoot in Agentic On-Policy Distillation

- **作者**：Jike Zhong、Ming Li、Yuxiang Lai、Xi Xiao、Sheng Zhang、Ritwick Chaudhry、Tianle Chen、Jingyu Xie、Zheda Mai、Shao-Yuan Lo、Konstantinos Psounis、Yuanyuan Lei
- **首次公开日期**：2026-10-18
- **版本日期**：2026-10-18（v1）
- **原始论文**：https://arxiv.org/abs/2610.25034
- **arXiv ID**：2610.25034
- **DOI**：https://doi.org/10.48550/arXiv.2610.25034
- **代码/项目**：https://github.com/Jike338/SPOD

## 一句话结论

发现 Agent OPD 会先让 student 超越 teacher、随后又被持续 teacher 监督拉回；SPOD 用成功轨迹门控和单侧概率下限保护 student 已验证的优势。

## 真正新增的内容

论文把“student 超越 teacher 后为何回退”拆成 repair 与 erosion 两股作用，并给出不依赖额外 critic 的成功保护机制。

## 核心方法

在成功 episode 中，若 teacher 对 student 已选动作的概率低于 student，则屏蔽该状态的 teacher KL，改用单侧概率下限；其余状态保持普通全词表 OPD。

## 关键实验结果

两个模型族、三个 Agent benchmark、六个设置中，最终成功率相对普通 OPD 最高提升 15.2 个百分点，相对 teacher 最高领先 20.0 点；全部设置的最终 checkpoint 也超过普通 OPD 的最佳中间 checkpoint。

## 证据质量与局限

证据覆盖多模型族与多环境且代码公开；但门控依赖二值 episode success，尚未证明对稠密、延迟或含噪环境奖励同样稳健。

## 最接近的相关工作

最接近 RetireOPD、TCOD、SAGE-OPD 与普通 OPD early stopping；区别是它在决策级保护已成功的 student 动作，而非只决定何时停教。

## 如何复用或推进 LLM-as-a-Verifier

可直接把 verifier 的环境真值作为 success gate：成功且 teacher–student 冲突时保留 student 分布；失败状态继续接受 score-level teacher 蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有 Agent verifier × OPD 路线应加入“成功分支免侵蚀”消融，并把 A/B/T 中的 T 扩展为“teacher 冲突但环境已验真”的保留态；sealed eval 仍需独立于训练门控。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
