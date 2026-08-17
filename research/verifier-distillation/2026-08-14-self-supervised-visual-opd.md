# S²VOPD：自监督视觉 On-Policy Distillation

## 基本信息

- **论文标题**：Self-Supervised Visual On-Policy Distillation
- **作者**：Yijiang Li, Yijun Liang, Yunjie Tian, Bingyang Wang, Ke Zhang, Zhenfei Yin, Di Fu, Philip Torr, Nuno Vasconcelos
- **首次公开日期**：2026-08-14
- **版本日期**：2026-08-14（arXiv v1）
- **arXiv ID / DOI**：2608.14144 / 10.48550/arXiv.2608.14144
- **原始论文**：https://arxiv.org/abs/2608.14144
- **项目页**：https://williamium3000.github.io/s2vopd/
- **代码**：项目页标有 Code，但截至本次记录未解析到独立代码仓库 URL

## 一句话结论

S²VOPD 不给 teacher 增加特权标签，而是让 EMA teacher 看原图、student 看适度退化图，从同一模型中制造任务一致的信息不对称；它提示 Agent verifier 可通过“teacher 看完整轨迹、student 看受控删减轨迹”获得无需人工标签的 on-policy 信号，但该迁移尚属分析推断。

## 真正新增的内容

**论文原文结论：**

- 信息不对称不一定来自更大 teacher、答案或 ROI 标注，也可来自对 student 输入的受控信息削减。
- 对称自蒸馏会退化；teacher/student 预测差距与收益呈倒 U 形，适中增强最好。
- 若增强移除了回答问题所需的关键证据，虽能制造很大差异，却成为无信息监督。
- 默认方案为将 student 图像降采样至 0.3–0.6 倍，并以 0.5 概率加入约 `σ=0.11` 的 Gaussian noise。

**本文分析推断：**

对长时程 Agent，可把视觉增强替换为轨迹视图退化：隐藏部分工具输出、延迟观察、压缩历史或遮蔽中间 critique，让 teacher 在完整轨迹上给 student 自生成状态评分。关键不是差距越大越好，而是被遮蔽信息仍可由上下文合理恢复，且不能改变任务真值。

## 核心方法

student 在增强图像上生成 on-policy rollout；同一模型的 EMA teacher 在原始图像和相同生成前缀上产生 token 分布。训练最小化 teacher 与 student 的逐 token generalized Jensen–Shannon divergence（`α=0.5`），只在 teacher top-k token 上归一化。

该损失是全部训练信号：没有 reward、value function、reference-policy KL、外部强 teacher 或人工标注。

## 关键实验结果

**论文报告：**

- 六个细粒度感知基准上，Qwen3.5-4B 平均准确率从 70.68% 提升到 77.44%（+6.76）。
- 在论文比较范围内，4B 模型超过 Qwen3-VL-Instruct-235B 的 75.75%，与 Qwen3.5-397B 的 77.44% 持平，并高于 GPT-5.4 的 72.77%。
- 固定训练数据时，恢复最佳 privileged-information 方法增益的 96%。
- 对称、无增强自蒸馏降到 65.21%；四类非对称增强均有提升，其中适度信息削减最好。
- 同数据公平比较中，4B 模型在感知和数学推理综合平均达到 75.33；论文报告感知 +5.7%、数学 +3.7%。
- 过强 crop 随强度增加由 71.53 降至 68.76、67.44，支持“任务一致性”条件。

## 证据质量与局限

证据包含四类增强、强度扫描、EMA 和 divergence 消融、4B/9B 规模及多组基准，方法因果链较清晰。

局限是：

- 仅验证 VLM 感知/视觉数学，未验证文本 verifier、工具 Agent 或长轨迹；
- teacher 是 student 的 EMA，长期可能累积共同偏差，缺少独立真值时不能保证“clean-view teacher”正确；
- 与闭源模型的比较依赖特定基准与评测时间，不能泛化为总体能力排序；
- 项目页提供丰富结果，但独立代码仓库链接尚未确认；
- 未展示 sealed evaluator 下的长期共适应风险。

## 最接近的相关工作

- Vision-OPD、OPSD、ZwZ：依赖答案或 ROI 等 privileged supervision 的视觉 OPD
- TTRL、RENT、Intuitor：无需标注的自奖励/内在奖励 RL
- VOLD：从 LLM 向 VLM 的 reasoning transfer
- On-Policy Distillation（Agarwal et al., 2024）
- consistency/self-distillation 与 teacher–student augmentation 学习

S²VOPD 的核心差异是把“受控减信息”本身作为 teacher–student 不对称来源，并系统刻画差距强度的倒 U 关系。

## 如何复用或推进 LLM-as-a-Verifier

- teacher 输入完整轨迹与环境证据，student 仅看压缩/遮蔽版本，在 student 自生成轨迹上蒸馏 ordinal score distribution。
- 用程序检查器验证删减前后任务答案、可达状态和环境后果一致；不一致样本直接拒绝。
- 训练目标可从 token JSD 改为 A/B/T 分布 JSD 或分档分数的 Earth Mover/ordinal KL。
- 把 teacher–student divergence 当作“可学习难度”，但仅在门控通过后采样；过高 divergence 很可能是证据被破坏，而非高价值学习信号。

## 对现有 Agent verifier × OPD 实验路线的具体影响

1. **score-level OPD**：新增“完整视图 teacher / 受控视图 student”条件，用同一 verifier 的 EMA 副本即可构造信号，降低昂贵 teacher 依赖。
2. **pairwise A/B/T 与序数分布**：让 teacher 看到两条完整分支，student 看到各自压缩视图；蒸馏完整 A/B/T 概率而非 argmax。
3. **程序化/环境真值门控**：这是迁移能否成立的硬条件。遮蔽后若改变任务语义、工具结果或可恢复性，必须丢弃。
4. **student-generated critique states**：由 student 在退化视图下生成 critique，teacher 在完整视图下评分，可集中产生“学生会犯、teacher 有额外证据纠正”的状态。
5. **高熵分叉保留探索**：按倒 U 原则使用中等不对称；极高 gap 分支不应被直接强化或剪除，而应保留并交给环境真值复核。
6. **sealed eval**：EMA teacher 不能兼任最终 evaluator；使用冻结、未参与训练的 verifier 加环境成功指标做 sealed evaluation，检测共同漂移。

## 结论边界

论文原文支持视觉域中的无标签非对称 OPD，不支持其已能训练文本或 Agent verifier。对轨迹遮蔽、序数分布和环境门控的建议均是跨模态方法迁移假设，应单独做消融验证。
