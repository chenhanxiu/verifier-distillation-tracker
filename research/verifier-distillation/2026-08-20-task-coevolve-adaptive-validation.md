# Task-CoEvolve: Efficient Harness Optimization via Adaptive Validation Task Selection

## 基本信息

- **作者**：Atsuyuki Miyai、Kiyoharu Aizawa、Toshihiko Yamasaki
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.20169
- **DOI**：10.48550/arXiv.2608.20169
- **原始论文**：https://arxiv.org/abs/2608.20169
- **代码**：https://github.com/Agent4Science-UTokyo/Task-CoEvolve

## 一句话结论

在反复优化 Agent harness 时，应优先评估能区分候选 harness、且位于当前能力边界附近的任务，并用采样概率校正估计全验证集表现，从而减少大量已经饱和或持续失败的低信息评估。

## 真正新增的内容

**论文原文结论**：Task-CoEvolve 不仅演化 harness，也动态更新验证任务的采样分布；利用历史候选结果方差识别高判别力任务，并用 Hájek 采样加权估计器在不同迭代使用不同子集时保持候选可比性。

**分析推断**：这相当于为 Agent verifier/OPD 建立“主动选轨迹”层：不是平均采样 rollout，而是把评估与 teacher 调用预算投向候选策略最易分叉的位置。不过这种共演化只适合训练/开发集，不能替代独立 sealed eval。

## 核心方法

1. 在历史候选 harness 的任务成败矩阵上估计每个任务的结果方差；候选越容易在该任务上分歧，采样概率越高。
2. 每轮只评估一个按自适应分布抽出的任务子集，重点覆盖接近能力边界的样本。
3. 使用已知包含概率的 Hájek 估计器恢复候选在完整验证集上的总体分数，减少因每轮子集不同造成的偏差。
4. 用估计分数选择下一轮 harness 变体；任务采样分布随 harness 能力变化而更新。

## 关键实验结果

**论文原文结果**：

- 在线文本分类上，7% 评估预算已接近完整验证集搜索，20% 预算的平均 held-out test accuracy 达 49.3±0.8，高于完整搜索的 48.6±0.8。
- 在 Terminal-Bench 2.1 上，以约 20% 的评估量达到与完整搜索相近的最终表现，总搜索成本降低 67%–80%。
- 对 GPT-5.6-Luna，输入 token 从完整搜索的 2,888M 降至 579M，时间从 22.2 小时降至 11.5 小时；对 Qwen3.6，输入 token 从 741M 降至 246M，时间从 38.0 降至 20.5 小时。
- 去掉采样感知估计、改用 difference estimator 后，20% 预算平均准确率从 49.3 降至 46.0，说明校正并非可省略细节。

## 证据质量与局限

- **证据质量：中。** 同时有合成/分类和真实 Agent benchmark，报告多预算、多个模型与估计器消融。
- Terminal-Bench 的最终性能“相近”不等于证明对所有 Agent 域泛化；任务规模和 harness 搜索器仍有限。
- 当前每个候选的评估数预先固定，不能对明显较差候选早停，也不能在两个候选难区分时自动追加样本。
- 采样校正依赖包含概率正确记录及历史结果足够稳定；强分布漂移时方差估计会滞后。
- 验证任务与 harness 共演化会增加 evaluator 共适应风险，论文的 held-out test 仍需在真实长期开发流程中进一步密封。

## 最接近的相关工作

最接近 Meta-Harness、ACE/MCE、自动 prompt/context/harness 演化，以及主动测试选择和重要性采样评估。区别在于它显式优化“哪些任务值得评估”，并对非均匀采样后的全集分数做统计校正。

## 如何复用或推进 LLM-as-a-Verifier

- 将“任务方差”扩展为 verifier 分歧、A/B/T 熵、outcome 与 process score 冲突度，主动选择最有信息量的轨迹。
- 对昂贵 LLM verifier 采用非均匀调用，并用包含概率加权恢复总体校准指标。
- 把持续全对/全错样本降频，但保留小比例哨兵采样，防止能力边界移动后无法被重新发现。
- 对 verifier 自身也维护独立审计集，避免只围绕当前 harness 的薄弱点优化后失去全局可靠性。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：按 rollout 间 score 方差和 teacher–verifier 冲突主动分配蒸馏预算，并用采样权重校正总体训练目标。
- **A/B/T 与序数分布**：优先抽取 A/B/T 概率接近、序数分布熵高或不同 verifier 排序不一致的分叉。
- **程序化真值门控**：程序检查稳定通过/失败的任务可降频；边界任务保留完整环境验证。
- **student-generated critique states**：把不同 student critique 导致的 verifier 分歧视为任务信息量，而非只看最终成败。
- **高熵探索**：高方差任务应增加观察而不是直接压制，使探索分叉获得更多 teacher/verifier 预算。
- **sealed eval**：训练期可让任务与 harness 共演化，但最终结论必须来自完全不参与任务采样、harness 改写和 verifier 调参的独立密封集合。