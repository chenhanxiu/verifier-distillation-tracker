# ReplayRCA：以环境回放测量 Agent 失败诊断与实时监督

- **论文标题**：ReplayRCA: Measuring Post-hoc Diagnosis and Live Oversight of Agent Failures by Counterfactual Replay
- **作者**：Jeremy Canale, Fabien Soulis
- **首次公开日期**：2026-10-29
- **版本日期**：2026-10-29（v1）
- **原始论文**：https://arxiv.org/abs/2610.41025
- **DOI**：https://doi.org/10.48550/arXiv.2610.41025
- **代码与环境**：https://github.com/jeremy1392/RCAreplay

## 一句话结论

ReplayRCA 不按标注一致率评价诊断，而是把环境恢复到被指认步骤前、替换一次动作并继续执行，以相对 placebo 的成功率增量测量真正的因果修复。

## 真正新增的内容

**论文原文结论**：post-hoc 根因定位与 live oversight 不是同一能力；只有实际替换动作后的 continuation success 才能检验诊断是否有因果价值。

**分析推断**：这是 long-horizon verifier 的强真值接口：teacher critique 是否值得蒸馏，应由“回滚—替换—继续”的环境结算验证，而不是由另一个 Judge 判断解释是否像样。

## 核心方法

对失败轨迹选定一个步骤，恢复到该步骤前状态，以诊断器建议动作替换原动作，再由同一 Agent 继续。指标 causal repair 为替换后的成功率减去配对 placebo（通过同一机制重放原动作）的成功率。设置 post-hoc autopsy 与只能提前干预一次的 live oversight 两条赛道。

## 关键实验结果

**论文原文报告**：

- OpsWorld 的 62 个校准系统性失败上，13 个 frontier models 中最佳 causal repair 为 +51.3 点；前八名统计上不可区分，5 个项目无人修复。
- 强模型被迫在最后一步干预时损失 17.1 点，说明 annotation benchmark 的 last-step shortcut 不成立。
- 87 条 live runs 上，最佳两名统计持平，其中之一是小型开放权重模型。
- GPT-6.1 Sol 属于最佳 post-hoc 诊断器之一，却是同组 live supervisor 中最弱者（-14.5 点，p=0.002）。

## 证据质量与局限

环境确定、可程序生成、placebo 配对且公开代码，因果识别明显强于文本标注一致率。局限是样本量 62/87、单一 back-office 环境和一次干预协议；恢复机制可能不覆盖不可逆真实世界副作用。模型排名随提示、预算和环境族变化，不能泛化为总体能力排序。

## 最接近的相关工作

最接近 Continual Search for Long-Horizon RCA、REVERSAL-BENCH、SkillAA、PaperDoctor、DynSTEER 与 process reward / failure attribution benchmarks。ReplayRCA 的关键增量是用环境干预后的差分结果定义 ground truth。

## 如何复用或推进 LLM-as-a-Verifier

- 将 verifier 输出拆成“失败步骤分布、建议替换动作、置信度/弃权”。
- 用 causal repair 作为 teacher 信号的硬门控；文本 critique 只在修复成功时进入训练。
- 对 pairwise A/B/T，比较候选替换动作相对 placebo 的区间；区间重叠或状态不可恢复时标 T。
- 把 post-hoc 与 live verifier 分开训练和报告，避免用事后可见信息污染在线监督。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析推断**：新增 replay-gated on-policy verifier distillation：从 student 失败轨迹抽取高熵分叉，生成多个 critique/action，环境回放得到分布式 causal-repair 标签，再蒸馏到轻量 verifier。应保留多成功修复分支，避免只学习单一路径；不可回放状态必须弃权。sealed eval 要冻结环境生成器、隐藏失败模板与回放种子，并确保 evaluator 不读取训练期 critique，防止共适应。