# Verbalising Model's Computation for Chain-of-Thought Faithfulness Detection

## 基本信息

- 方法名：VERITAS
- 作者：Yujing Wang, Yulan He, Wenya Wang, Hanqi Yan
- 首次公开日期：2026-10-16
- 版本日期：2026-10-16（v1）
- arXiv：2610.23275
- 原始论文：https://arxiv.org/abs/2610.23275
- DOI：https://doi.org/10.48550/arXiv.2610.23275
- 代码：未发现公开代码链接

## 一句话结论

VERITAS 将逐 token 的内部计算投影成可读的推理锚点演化，再训练轨迹分类器检测 CoT 不忠实；它显著优于纯文本 Judge，可作为独立的白盒 verifier 通道。

## 真正新增的内容

**论文原文结论：** 现有 CoT verifier 多从最终文本或静态 activation 判断，难以解释不忠实如何形成。VERITAS 用 layer-wise Jacobian projection 描述推理锚点在层间、token 间如何出现、转移并显化到输出，再以这些结构特征训练分类器。

**分析推断：** 对 generative verifier 蒸馏而言，这提供了与文本 critique 机制异质的 teacher 信号，可减少多个同源 LLM Judge 的相关错误。

## 核心方法

1. 对每个生成的 CoT token 计算分层 Jacobian 投影。
2. 将内部计算相对语义锚点的演化“语言化/结构化”。
3. 沿完整轨迹聚合这些特征，训练 faithfulness classifier。
4. 在不同数据集和模型架构上测试泛化。

## 关键实验结果

**论文原文：** 在 FaithCoT-Bench 与 BonaFide 的四个数据集上，VERITAS 相对 LLM-as-a-Judge 的 balanced accuracy 提升 28.4%，相对 activation probing 平均提升 16.0%；作者还报告了跨数据集和模型架构的泛化。

**分析推断：** balanced accuracy 的提升说明它适合用作异质审计通道，但不等于能验证外部事实或 Agent 工具执行；它验证的是“显式 CoT 与内部计算是否一致”。

## 证据质量与局限

- 有四个数据集、文本 Judge 与 activation probe 基线，证据比单任务案例更强。
- 依赖白盒梯度/内部状态，无法直接用于闭源 teacher。
- faithfulness 不等于正确性；忠实地表达错误推理仍应被环境真值拒绝。
- 投影产生的可读描述本身可能引入解释偏差，需要反事实干预验证。

## 最接近的相关工作

- Monitoring and Discovering Reward Hacking 的内部表示探针；
- Caught in the Act 的跨层跨 token 监控；
- Legibility Is Not Interpretability；
- Beyond Accuracy 的过程轨迹 Overseer；
- generative verifier 与 process reward model。

## 如何复用或推进 LLM-as-a-Verifier

采用双通道 teacher：文本 generative verifier 输出 critique 与序数分布，VERITAS 输出 faithfulness 风险。只有外部真值通过且两个通道无重大冲突时，critique 才进入蒸馏；冲突样本进入 T 或人工/程序复核。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD：** 将 faithfulness risk 作为可靠性折扣，而非直接正确性奖励。
- **A/B/T 与序数分布：** 内外通道冲突时标 T，并保存两套后验。
- **真值门控：** 环境/程序真值仍决定方向；内部信号只影响幅度与路由。
- **critique states：** 拒绝与内部计算明显脱节的自生成 critique。
- **高熵探索：** 白盒风险用于定位值得分叉的 token，而不是统一压低策略熵。
- **sealed eval：** 在未训练架构、未见任务和干预式 faithfulness 测试上评估，避免分类器与生成器共适应。
