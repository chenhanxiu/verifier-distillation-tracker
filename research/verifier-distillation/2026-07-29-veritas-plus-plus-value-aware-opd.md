# Veritas++：Value-aware On-Policy Distillation for Perception-Enhanced AIGI Detection

> 补录自「Verifier 蒸馏论文」scheduler 于 2026-07-31 的实际发现。

## 论文信息

- **标题**：Veritas++: Value-aware On-Policy Distillation for Perception-Enhanced AIGI Detection
- **作者**：Hao Tan, Jun Lan, Zichang Tan, Ajian Liu, Zijian Yu, Chuanbiao Song, Huijia Zhu, Weiqiang Wang, Jun Wan, Zhen Lei
- **发布日期**：2026-07-29（arXiv v1）
- **arXiv**：[2607.27113](https://arxiv.org/abs/2607.27113)
- **HTML 全文**：[arxiv.org/html/2607.27113](https://arxiv.org/html/2607.27113)
- **代码与检查点**：[EricTan7/VeritasPP](https://github.com/EricTan7/VeritasPP)
- **领域**：多模态模型、AI 生成图像检测、On-Policy Self-Distillation

## 一句话结论

这篇工作的直接贡献不是 verifier 蒸馏，而是证明了：在 student 自己访问到的状态上，privileged self-teacher 的监督不应等权使用；可以同时在**轨迹、token 和散度方向**三个层面估计“蒸馏价值”，重点学习可纠正的错误信号。这个结构对 Agent verifier × OPD 很有启发，但不能直接当作 score-level verifier distillation 的先例。

## 真正的新意

Veritas++ 用三阶段训练把“感知能力”内化为可解释的真伪推理：

1. **高质量冷启动**：仅使用带人工证据的数据，减少机器生成解释中的感知幻觉。
2. **Perception-oriented Learning（PoRL）**：用可验证奖励强化细粒度目标、语义异常和像素级差异三类感知能力。
3. **Value-aware On-Policy Distillation（VaOPD）**：student 在标准查询下生成自己的推理轨迹；EMA self-teacher 获得训练时专有标签与感知提示，在同一 student prefix 上给出 dense token distribution。

VaOPD 对蒸馏信号做三级建模：

- **轨迹级重加权**：提高错误 rollout 的权重，同时保留正确样本以防遗忘。
- **token 级重加权**：用 teacher-to-student KL 衡量 privileged teacher 在该位置提供的新信息量。
- **自适应蒸馏方向**：联合 teacher/student 熵差与 teacher 对 student 已采样 token 的相对优势，识别“teacher 展示了更多合理模式、同时否定当前 token”的纠正位置；纠正信号强时，更偏向 forward-KL 式的 mode covering。

其核心不是简单筛掉低价值样本，而是把“错误程度、局部信息增量、应采用的分布匹配方向”分开建模。

## 关键实验结果

- 模型为 Qwen3-VL-8B；VaOPD 使用约 11K 样本、1 个 epoch，teacher 由 EMA 更新。
- 完整 VaOPD 相比 vanilla OPD，在 emerging benchmarks 上提升约 **+4.1 Acc / +5.6 F1**。
- 加入少量新场景样本后，emerging 场景平均准确率由 **70.3% 提升到 80.6%**，standard benchmarks 仅从 **94.0% 降至 93.6%**。
- 三种机制中，token reweighting 的单项贡献最大；轨迹和 token 重加权组合后也表现出互补增益。
- 对比 RLVR，VaOPD 更好地兼顾新能力获取与旧能力保持。

## 证据质量与局限

**证据质量：中高（方法与消融较完整，但仍是 arXiv v1，且结论主要局限于单一视觉取证任务）。**

支持证据：

- 覆盖 standard、in-the-wild、emerging 三类评测；
- 提供 PoRL、VaOPD 及三级加权机制的消融；
- 公开代码和检查点，具备较好的复现入口；
- 报告了新能力学习与旧能力保持之间的权衡。

主要限制：

- 只验证 Qwen3-VL-8B 和 AIGI 二分类，不能直接证明方法对文本 verifier、Agent 轨迹或序数评分同样有效；
- teacher 与 student 是同模型/同 tokenizer 的 EMA self-distillation，没有解决跨模型、闭源 teacher 或 logit 不可得问题；
- 推理质量只在 100 条响应上由单一 MLLM judge 评估，论文也承认缺少系统的解释质量评测；
- 三阶段训练共同贡献较大，VaOPD 的独立外部有效性仍需跨任务复验。

## 与相关工作的关系

相较于 vanilla OPD 对每个 student token 等权匹配 teacher，VaOPD 把“哪些轨迹值得纠正、哪些 token 含有新信息、该位置应 mode-seeking 还是 mode-covering”显式拆开。它与 privileged on-policy self-distillation 同属“teacher 在 student state 上获得额外信息”的路线，但进一步引入了价值估计和动态散度方向。

它和 LLM-as-a-Verifier 的联系主要是**结构性**而非任务等价性：二者都在利用分布而不是 hard label，并都需要处理不确定性与信号质量；但本文蒸馏的是生成 token 分布，不是 verifier 的评分分布。

## 对 Agent verifier × OPD 的启示

### 可直接迁移的设计

1. **轨迹级权重**：优先蒸馏 student verifier 判断错误或校准误差高的轨迹，而不是平均使用所有轨迹。
2. **状态/token 级权重**：把 teacher–student 的评分分布差异、teacher 熵变化或 evidence sensitivity 作为“该状态是否值得蒸馏”的依据。
3. **动态散度方向**：当 teacher 提供多种合理评分解释时偏向 mode covering；当 teacher 置信度高且需要明确纠错时偏向更强的定向匹配。
4. **防遗忘约束**：保留一部分已正确轨迹，监测旧 benchmark 上的 verifier calibration 与 ranking 能力。

### 不能直接照搬的部分

目标方案是 **Agent-on-policy / Score-level On-Policy Distributional Verifier Distillation**：Qwen student 先生成自己的 critique/state，teacher 在这些状态上输出 A/B/T 或序数评分分布，再在评分空间蒸馏。Veritas++ 则在同 tokenizer 的生成 token 空间中进行 dense OPD。因此，它支持的是“student-state + privileged teacher + value-aware weighting”这一设计原则，而不是 score-level verifier distillation 的完整实现。

### 建议增加的实验

- Uniform OPD vs. trajectory weighting vs. state/token weighting vs. dynamic divergence；
- hard label、soft score distribution、score distribution + privileged evidence 三组比较；
- 将 teacher–student entropy gap、评分 KL、最终 verifier error 分别用作 gating 信号；
- 同时报告 accuracy/ranking、ECE/Brier/NLL、旧任务遗忘和单位有效样本成本。

## 结论

**建议精读方法与消融。** 对当前研究最有价值的是三级价值建模，以及“privileged teacher 只在可纠正的位置提供更强监督”的思路。论文不是 verifier 蒸馏的直接 prior art，但可以成为 value-aware Agent-on-policy verifier distillation 的重要邻近工作。
