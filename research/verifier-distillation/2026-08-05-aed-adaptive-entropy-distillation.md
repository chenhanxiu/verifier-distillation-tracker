# AED：将 Reverse KL 重释为自适应熵蒸馏

## 基本信息
- **论文标题**：Rethinking Reverse KL as Adaptive Entropy Distillation
- **作者**：Shizhen Li, Zhiyu Shen, Yuyin Lu, Yunhe Pang, Jielin Song, Yanghui Rao, Fu Lee Wang
- **首次公开日期**：2026-08-05（本次进入 arXiv new submissions 检索窗口）
- **版本日期**：2026-08-05（v1）
- **原始论文**：https://arxiv.org/abs/2608.14685
- **DOI**：10.48550/arXiv.2608.14685
- **代码**：https://github.com/ShizhenL1/AED

## 一句话结论
AED 将 on-policy reverse KL 分解为 teacher fitting 与 student entropy 两项，并用 teacher entropy 动态调节模仿强度，为“高置信位置收敛、模糊位置保留探索”提供了理论化实现。

## 真正新增的内容
**论文原文**：RKL 的 token 级最优 student 等价于 teacher 的温度化分布；无需额外 forward-KL 分支，即可通过自适应权重平衡 mode-seeking 与 uncertainty preservation。

**分析推断**：同样的权重可作用于 verifier 的 ordinal logits 或 A/B/T 分布，但 teacher entropy 只能表示不确定性，不能证明 teacher 方向正确，仍需结果真值门控。

## 核心方法
把 RKL 改写为 teacher-fitting 项与 student-entropy 项；根据 teacher token entropy 计算自适应强度。低熵 teacher 更强地集中 student，高熵 teacher 则减弱模仿、保留 student 支撑。

## 关键实验结果
在 Dolly、SelfInst、Vicuna、S-NI、UnNI 指令遵循与三项数学推理评测中，AED 报告最高总体表现，并改善 teacher–student 分布和熵对齐。TinyLLaMA-1.1B 上用 GPT-5.4 做 win/tie/loss judge，AED 对 RKL、AKL、ToDi、EOPD 的 win rate 均高于 loss rate；数学 Pass@1 与 Pass@k 也更高。

## 证据质量与局限
包含理论推导、多个基准、不同架构、消融和分布诊断。局限是只支持共享词表的开放模型，未测试黑盒/异构 tokenizer 或超大模型；部分质量结论依赖单一 GPT-5.4 judge，缺少 sealed 多 judge/人工验证；未测试 Agent 轨迹。

## 最接近的相关工作
RKL/forward KL 混合、EOPD、AKL、ToDi、entropy regularization、temperature distillation。AED 的区别是从 RKL 本身导出自适应熵权衡。

## 如何复用或推进 LLM-as-a-Verifier
对 ordinal reward distribution 的 teacher entropy 设蒸馏强度：teacher 很确定时集中 student，teacher 模糊时保留概率质量。对 A/B/T 可避免把 teacher 的 Tie/不确定性压成硬标签。

## 对 Agent verifier × OPD 路线的影响
- **score-level**：蒸馏完整分布及其熵，而非只拟合均值。
- **A/B/T**：高 teacher entropy 保持 Tie 和多个候选。
- **真值门控**：只有环境验证 teacher 方向可靠时才能加强 imitation。
- **critique states**：在 student critique 上记录 teacher entropy，作为采样和权重特征。
- **高熵探索**：直接提供保留支撑的可实现基线。
- **sealed eval**：报告 calibration、NLL、ECE、rank accuracy 与独立 outcome，不只 judge win rate。

## 结论边界
论文支持 entropy-adaptive RKL 改善所测文本任务，但不能证明 teacher entropy 能替代环境可恢复性或长期贡献评估。
