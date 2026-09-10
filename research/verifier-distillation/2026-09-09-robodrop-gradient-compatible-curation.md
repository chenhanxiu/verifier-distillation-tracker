# RoboDrop：用局部梯度相容性筛选 VLA 后训练轨迹

- **论文标题**：RoboDrop: Curating VLA Post-Training Data via Local Gradient Compatibility
- **作者**：Runze Xu, Yuanfan Xu, Cuijie Xu, Shuang Dai, Yining Li, Yu Wang, Jincheng Yu
- **首次公开日期**：2026-09-09
- **版本日期**：2026-09-09（v1）
- **原始论文**：https://arxiv.org/abs/2609.10021
- **代码**：截至本次记录未发现公开代码

## 一句话结论

RoboDrop 用候选样本梯度与语义/视觉匹配 clean validation 样本梯度的一致性评估监督是否会推动正确更新，比基于长度或表示相似度的轨迹筛选更可靠。

## 真正新增的内容

**论文原文结论**：在一次 warm-up 训练过程中在线计算 context-conditioned local gradient compatibility，随后聚合成 episode 分数并自动过滤；该信号能统一发现时序错位、动作错误和自然质量差异。

**分析推断**：这为 verifier 蒸馏提供了“更新级门控”视角：teacher label 即使表面合理，只要其梯度与少量硬真值锚点冲突，就应降权或进入 A/B/T 复核，而不是直接进入 OPD。

## 核心方法

进行一轮 warm-up；为候选样本寻找任务语义和视觉上匹配的 validation 样本，比较两者局部梯度的余弦相容性；沿训练 checkpoint 更新 reference gradient，聚合 sample score 为 episode score；固定预算或用 GMM+BIC 自动决定过滤比例。

## 关键实验结果

LIBERO-10 的时序/动作污染检测平均 AUROC 97.4、balanced accuracy 93.5，筛后成功率 91.8。真实机器人非专家识别 AUROC 98.38、balanced accuracy 95.63；统一移除 20% 时成功率从 35.0% 到 63.75%，自动预算达到 67.5%。在 Robomimic 消融中，完整方法 AUROC 87.67，优于固定 checkpoint 83.50 和仅 DINO 相似度 75.86。

## 证据质量与局限

覆盖合成污染、自然质量变化、不同 VLA backbone 与真实机器人，且包含多种消融，证据较强。主要局限是必须拥有可信 clean reference set，筛选质量继承其偏差；计算梯度有额外成本；episode 聚合可能掩盖长轨迹中“有效前缀 + 局部错误”的结构。

## 最接近的相关工作

Influence-function 数据选择、Behavior Retrieval、DataMIL、Scizor、QoQ，以及 Key-Step Supervision、PGPO、Legibility is Not Interpretability 等步骤信用分配方法最接近。RoboDrop 的独特之处是沿实际训练轨迹测量局部更新方向。

## 如何复用或推进 LLM-as-a-Verifier

从 sealed、程序可验的少量轨迹建立 reference-gradient bank；对 teacher score、pairwise label 和 critique 分别测量其对 verifier/student 的梯度相容性。将相容性作为独立置信特征，而非直接等同正确性。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：加入 gradient-compatibility gate，比较硬过滤、软权重和不门控。
- **A/B/T 与序数分布**：方向冲突且真值不足时标 tie/abstain，不强造 winner。
- **真值门控**：reference bank 必须来自程序或环境真值，并按任务语义匹配。
- **critique states**：保留能产生相容更新的 critique；局部不相容只惩罚责任步骤。
- **高熵探索**：避免按整条失败轨迹删除，将 episode 分数拆到关键 step/branch。
- **sealed eval**：reference bank、训练选择集和最终评测三方隔离，防止筛选器与 student 共适应。
