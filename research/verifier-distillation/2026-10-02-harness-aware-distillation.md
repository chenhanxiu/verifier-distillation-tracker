# Harness-Aware Distillation for Small Language Model Agents

- 作者：Moonseok Choi、Taehong Moon、Giung Nam、Juho Lee
- 首次公开日期：2026-10-02
- 当前版本日期：2026-10-02（v1）
- arXiv：2610.02858
- 原始论文：https://arxiv.org/abs/2610.02858
- Canonical URL：https://doi.org/10.48550/arXiv.2610.02858
- 项目页：https://moon4sake.github.io
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】HAD 只蒸馏 teacher 相对固定 harness 新增的能力：比较同一 teacher 在有/无 harness 信息时的动作，并用 harness 记录过滤明显无效的偏好对。

## 真正新增的内容

【论文原文】方法把共享 harness 从普通输入提升为对照变量与校验器：有 harness 动作相对无 harness 动作构成偏好，但若“正样本”与 harness 记录冲突则丢弃该偏好项；动作在 student 自己的 reasoning prefix 下评分。

## 核心方法

【论文原文】在 student 访问状态上保留常规响应蒸馏，同时查询 teacher 的 harness-conditioned 与 stripped-history 动作，使用 action-only pairwise logistic loss；硬有效性 mask 只作用于偏好项。方法不需要任务奖励、成功标签或未来信息。

## 关键实验结果

【论文原文】在 ALFWorld 示例中，普通带 harness 的蒸馏将 harness utilization 从 65.7% 提至 73.1%，但成功率仅从 43.1% 到 43.5%；HAD 分别达到 81.0% 和 57.4%。论文还在 WebShop、ScienceWorld及跨模型族设置中报告优于同 harness 的 OPD 基线，并观察到更少无效循环与更多错误恢复。

## 证据质量与局限

【论文原文】对照设计能隔离 harness 的边际作用，并有多环境、多 teacher/student 尺度实验。局限是 harness 信息“通常有帮助”仍是代理假设；有效性过滤只能排除明显冲突，不能识别“合法但错误”的动作；harness 本身未必提供环境真值，且项目页不等于完整代码发布。

## 最接近的相关工作

最接近 Persistent Teacher Anchoring 的副作用前验证、Grounding Agent Memory 的环境探测门控、STRIDE 的 student-state 监督，以及对比式自蒸馏的 privileged/non-privileged 差分。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把“有证据上下文 vs 去证据上下文”的 verifier 分数差作为 evidence-usefulness 信号；只有动作与环境记录一致时才蒸馏该差分。这样可以区分 student 学会读 harness，还是仅模仿 teacher 的表面输出。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：【分析推断】直接蒸馏 Δscore＝verifier(含 harness)−verifier(去 harness)，并与常规绝对分数做消融。
- **pairwise A/B/T 与序数评分分布**：【分析推断】有/无 harness 动作构成 A/B；两者都合法或记录不足时应标 T，并保留差分置信度。
- **程序化/环境真值门控**：【分析推断】把 harness validity check 升级为不可覆盖的环境断言；软偏好不得推翻硬失败。
- **student-generated critique states**：【分析推断】让 student critique 明确引用 harness 字段；引用不存在或陈旧状态时拒绝写入。
- **高熵分叉下保留探索**：【分析推断】只在 harness 真正改变动作且证据充分时施加偏好，其他高熵状态不强行收缩。
- **独立 sealed eval**：【分析推断】隐藏一部分 harness 规则与状态扰动，单独测 harness utilization、环境成功和错误恢复，防止只对可见记录共适应。
