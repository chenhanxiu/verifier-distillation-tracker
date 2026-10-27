# ST-OPSD：通过激活引导修复 Privileged Teacher 的行为偏差

## 基本信息

- **论文标题**：Steering the Teacher: Improving On-Policy Self-Distillation for Thinking Models
- **作者**：Tiejin Chen, Xiaoou Liu, Hanyang Chen, Hua Wei
- **首次公开日期**：2026-10-25
- **版本日期**：2026-10-25（v1）
- **论文链接**：https://arxiv.org/abs/2610.34005
- **代码链接**：未发现公开代码

## 一句话结论

Privileged teacher 看到参考答案后可能诱导“引用不可见参考”和压制自我复核；ST-OPSD 在生成蒸馏目标时对 teacher hidden state 做定向 steering，而不改 student。

## 真正新增的内容

**论文原文结论**：识别 reference hallucination 与 reconsideration suppression 两类 OPSD teacher failure；从模型轨迹中提取两个 activation direction，在 teacher 计算 target distribution 时抑制引用参考、鼓励复核，并做 marker-family calibration。

**分析推断**：teacher 具有额外信息不等于 teacher 的全部行为都应复制。对 verifier distillation，应把“知道真值”与“表达/推理方式”解耦，只迁移与能力和校验相关的方向。

## 核心方法

- 从带/不带目标行为的推理轨迹提取 steering directions。
- 在 privileged teacher 前向时修改隐藏状态。
- 产生经 steering 的 token distribution 作为 on-policy student 轨迹监督。
- student 本身不加载 steering vector；以行为率和最终准确率联合评价。

## 关键实验结果

**论文报告**：在 AIME 与 HMMT 上，ST-OPSD 比 vanilla OPSD 和其他干预获得更高准确率，同时把 reconsideration 与 reference-hallucination rate 恢复到 base-model 水平。摘要未披露统一绝对增益。

## 证据质量与局限

针对具体可观察失败并同时测任务表现和行为，设计合理。局限是仅数学 benchmark、单类 privileged reference；activation direction 的跨模型与跨 Agent 任务迁移尚未证明。

## 最接近的相关工作

OPSD、DOPD 的 privilege illusion、contrastive self-distillation、Projected Distillation。本文不更换 loss，而是直接改变 teacher 产生监督的内部行为方向。

## 如何复用或推进 LLM-as-a-Verifier

可为 verifier teacher 提取“引用证据”“承认不确定”“主动复核”与“迎合答案”等方向；只在 teacher target 生成时应用，并以独立执行结果检查 steering 是否改善校准而非只改变话术。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher score/logits 应先经行为偏差审计再蒸馏。
- **A/B/T**：鼓励 teacher 在证据不足时输出 T，而非借 privileged answer 强判。
- **硬真值门控**：reference 仅决定正确方向，不能授权引用不可见信息。
- **critique states**：过滤依赖未来信息、用户不可见证据的 critique。
- **高熵探索**：保留 reconsideration，防止 teacher 压制探索。
- **sealed eval**：测试 student 在没有 privileged reference 时能否独立复核。