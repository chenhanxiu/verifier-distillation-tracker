# JudgeStealer：跨评估协议的 Judge 能力蒸馏

## 基本信息

- **论文标题**：JudgeStealer: Extracting LLM Judging Capabilities across Evaluation Protocols
- **作者**：Chen Chen、Yaolin Chen、Xuehan Sun、Juan Lin、Xueluan Gong、Yuhang Zheng、Qian Wang、Kwok-Yan Lam
- **首次公开日期**：2026-08-27
- **版本日期**：2026-08-27（v1）
- **原始论文**：[arXiv:2608.26982](https://arxiv.org/abs/2608.26982)
- **DOI**：[10.48550/arXiv.2608.26982](https://doi.org/10.48550/arXiv.2608.26982)
- **代码链接**：论文未提供公开代码仓库

## 一句话结论

JudgeStealer 证明只查询黑盒 Judge 的 pointwise 分数，也能通过序数平滑和跨协议转换蒸馏出同时支持 pointwise、pairwise、listwise 的小 Judge；其攻击视角恰好提供了低预算 verifier distillation 的工程模板。

## 真正新增的内容

**论文原文结论：**

- 首个针对 LLM Judge 的 query-efficient model extraction 框架，同时复刻 pointwise scoring、pairwise comparison 和 listwise ranking。
- 利用不同协议间的一致性，把 pointwise 查询自动转换为 pairwise/listwise supervision，无需增加 victim query。
- 依据语义多样性、surrogate 不确定性和潜在 Judge bias 动态挑选查询样本。
- 用 score smoothing 保留 ordinal structure，用 multi-protocol review 缓解多协议适配时的灾难性遗忘。
- 在多种闭源 LLM Judge 和 reward model 上明显优于通用 extraction/KD 基线。

**分析推断：**

虽然论文目标是安全攻击而非良性蒸馏，但它直接回答了现有路线中的关键问题：pointwise 0–3 分如何低成本派生 A/B/T 和 listwise 数据，以及如何让一个 student verifier 同时保持多协议一致性。使用时必须注意授权、数据治理与 Judge IP 边界。

## 核心方法

1. 建立候选池，使用 pointwise 接口查询 victim Judge。
2. 根据语义覆盖、student predictive uncertainty 与已知 bias 风险动态选样。
3. 对离散 pointwise 分数做平滑，保留邻近等级的 ordinal 关系。
4. 将平滑分数转换为 pairwise 胜负与 listwise 排序监督。
5. 以 multi-protocol review 在训练中回看不同协议，减少新协议覆盖旧能力。

## 关键实验结果

**论文原文结果：**

- 最高达到 pointwise 73.3%、pairwise 87.0%、listwise 71.6% accuracy。
- 在 GPT-5.4 / Alpaca、Qwen3-1.7B surrogate 的一个代表性设置中，方法 pointwise accuracy 为 0.383、pairwise 0.771、listwise 0.635；多数通用 baseline 明显更低。
- 在 GPT4All 数据上同一 surrogate 达到 pointwise 0.361、pairwise 0.783、listwise 0.635。
- 对不同 surrogate 规模、适配策略、reasoning 配置和代表性 extraction defense 仍保持有效。

## 证据质量与局限

**证据质量：中高。** 覆盖多个 victim、数据集、surrogate 和协议，指标包含 exact/nearby accuracy、MAE 与排序准确率。局限是目标为模仿 victim 而非人类真值：高 extraction fidelity 可能同时复制 victim bias、reward hacking 和共适应盲点。任务不是长时程 Agent，未验证轨迹证据定位、环境状态或步骤贡献；没有公开代码。

## 最接近的相关工作

- RM-Distiller / generative reward model distillation：蒸馏 reward/judge 能力。
- SARA：单 rubric 到多 rubric Judge 蒸馏。
- Pairwise Bradley–Terry / ordinal reward modeling：从相对比较恢复潜在分数。
- Cross-protocol Judge calibration：统一 pointwise、pairwise、listwise。
- Active learning for reward models：按不确定性挑选 teacher query。

## 如何复用或推进 LLM-as-a-Verifier

- 用强 Judge 的 pointwise 五维分数派生 A/B/T 与 listwise supervision，降低每种协议分别调用 teacher 的成本。
- score smoothing 可替换成完整序数概率分布，避免把相邻等级当作同等严重的错误。
- 选样同时考虑语义多样性、student entropy、Judge disagreement 和线上失败频率。
- multi-protocol consistency 可作为训练 loss，也可作为独立诊断：pointwise 差值与 pairwise verdict 冲突时拒绝进入训练集。
- 将环境真值和人工金标作为不可蒸馏的外部锚点，防止只学到 victim 偏好。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### Score-level on-policy verifier distillation

提供低预算黑盒 teacher 基线：仅收集 pointwise score distribution，在 student 当前轨迹上主动查询并蒸馏。

### Pairwise A/B/T 与序数评分分布

最直接相关。建议不要只转换为硬胜负，而应保留平滑后的 ordinal uncertainty；小分差映射为 Tie，大分差映射为 A/B，并对冲突协议降权。

### 程序化/环境真值门控

victim Judge 不能覆盖程序真值。工具执行、终态和安全规则先门控，跨协议蒸馏仅处理软评价维度。

### Student-generated critique states

原文未使用 critique。可让 student 先产生结构化证据与 critique，再把 teacher 查询预算集中到高不确定 critique；teacher 反馈不必逐协议重复查询。

### 高熵分叉下保留探索

主动学习会偏向高不确定样本，适合发现分叉；但不能把 teacher 单次 verdict 当真值，应保留平滑分布和 Tie。

### 独立 sealed eval

必要性极高。student 可能高保真复制 victim 的 bias；sealed eval 必须使用不同模型家族、人工与环境证据，并测跨协议一致性和 OOD 轨迹。