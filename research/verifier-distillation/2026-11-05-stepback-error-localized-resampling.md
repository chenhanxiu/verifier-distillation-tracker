# StepBack: Step-Level Error-Localized Resampling for Efficient Test-Time Reasoning

- **作者**：Yang Ouyang, Jung-Eun Kim
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08403
- **DOI**：https://doi.org/10.48550/arXiv.2611.08403
- **会议**：NeurIPS 2026
- **代码**：论文页面未给出公开代码链接

## 一句话结论

StepBack 先定位推理轨迹的首个疑似错误，再仅重采该步骤及后缀，以最多 41.26% 更少 token 达到完整 self-consistency 的平均准确率。

## 真正新增的内容

相较于按题目分配完整轨迹采样预算，StepBack 把预算下沉到轨迹内部：复用正确前缀，只在首错附近产生反事实后缀，形成更细粒度的 test-time branch allocation。

## 核心方法

从少量 draft trajectories 出发，用轻量信号定位可能的首错位置；固定此前前缀，重采错误步骤及其后续；最终对答案多数投票。方法可与 Adaptive Consistency 等题目级动态预算方法组合。

## 关键实验结果

在 7 个数学推理与 multi-hop QA benchmark 上，StepBack 平均匹配 self-consistency 准确率，同时最多减少 **41.26%** token 使用。

## 证据质量与局限

**论文原文结论**：多 benchmark、与 SC 直接对比且报告计算节省；已被 NeurIPS 2026 接收。  
**局限**：主要是静态推理而非有副作用的交互 Agent；轻量首错信号可能误定位；多数投票不提供校准的 ordinal 分布，也未证明局部分支在环境状态变化下安全。

## 最接近的相关工作

最接近的是 self-consistency、Adaptive Consistency、process verifier、belief-shift branching、EPIG-Tree、STRIDE 与局部 repair/reselection 方法。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出首错位置分布而非单点；对高置信首错做局部重采，对多峰或高熵分布保留多个候选分叉。对于 Agent，重采前需用环境 snapshot/rollback 保证前缀状态可复现，并由程序 oracle 验收后缀。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 可只作用于首错邻域，减少无关正确前缀上的 teacher 计算。
2. pairwise A/B/T 样本可由同一前缀的原后缀与局部修复后缀构造；定位不确定时标 T。
3. student-generated critique state 应包含首错候选、证据和可回滚环境快照。
4. 高熵首错分布应触发多分支而非单点覆盖，避免抹去探索。
5. sealed eval 要使用不可见 locator/verifier，并独立评估“定位准确率、修复成功率、总环境成本”，防止多数投票掩盖错误定位。