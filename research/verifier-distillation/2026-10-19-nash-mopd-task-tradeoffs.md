# Nash-MOPD: Optimizing Task Trade-offs in Multi-Teacher On-Policy Distillation

- **作者**：Siyuan Gan、Bo Yang、Linjian Meng、Boyan Wang、Xiaolong Qi、Jing Huo、Yang Gao
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.26124
- **arXiv ID**：2610.26124
- **DOI**：https://doi.org/10.48550/arXiv.2610.26124
- **代码/项目**：未公开

## 一句话结论

用局部 minimax/Nash 调度器分配多 teacher 的 prompt 预算，避免学习快的域持续吞噬 rollout、让慢域失去训练机会。

## 真正新增的内容

把多域 reverse-KL 及其下降速度转成“最大化最小预测比例改进”的预算博弈，而非固定比例或追逐最近下降最大的域。

## 核心方法

利用已有 reverse-KL 统计拟合局部进展，在不增加 teacher 查询或 rollout 的条件下求均衡采样比例，优先补足需要更多样本才能取得可比进展的域。

## 关键实验结果

在 DeepSeek-R1-Distill-Qwen-1.5B 上第 100 步已超过两个基线最终数学与代码分数；在 Qwen3-8B-Base 上达到 Fixed 最终水平；九项指标中领先八项，六项数学/代码准确率均最佳或并列最佳。

## 证据质量与局限

结果包含两个 student 规模且成本对照清晰；但任务域主要是数学和代码，尚未验证 verifier 面板或长 Agent 环境中的非平稳冲突。

## 最接近的相关工作

与 VG-OPD、Lightning Weave、D3-MOPD 和多目标优化相近；它解决的是 teacher/域预算而不是 token 级 teacher 选择。

## 如何复用或推进 LLM-as-a-Verifier

将不同 verifier teacher、环境 oracle、critic 与 critique 生成器视作不同域，用各自校准损失下降估计预算，而不是简单平均或固定轮询。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】对 A/B/T 与序数分布实验，可把“最差域校准改进”作为采样目标；但硬真值门控应保持最高优先级，Nash 调度只分配软监督预算。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
