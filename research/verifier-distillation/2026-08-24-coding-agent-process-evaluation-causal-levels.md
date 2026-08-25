# What Process Evaluation of Coding Agents Actually Measures: Action, Task, and Step Are Three Different Levels

## 基本信息

- 作者：Jiawei He、Mengyu Shi、Jie Jia、Xikai Yang、Dong Sun
- 首次公开日期：2026-08-24
- 版本日期：2026-08-24（v1）
- arXiv：2608.22960
- 原始论文：https://arxiv.org/abs/2608.22960
- DOI：https://doi.org/10.48550/arXiv.2608.22960
- 代码：论文公开页未提供

## 一句话结论

Coding Agent 的下一步动作预测、任务级不确定性和步骤因果贡献并不是同一种测量；完整轨迹 Judge 甚至可能因 collider bias 把语义相关性误当成真实贡献。

## 真正新增的内容

**论文原文结论：** 提出分离 action、task、step 三层测量的框架，并以结构因果模型导出的 replay estimator（SCAE）估计步骤贡献，同时通过控制 Judge 可见信息诊断偏差。

**分析推断：** 这直接挑战“只凭完整轨迹语义判断下一步对最终目标的贡献度”的方案，说明应把 Judge 输出降级为候选信号，并用同前缀干预回放建立因果锚点。

## 核心方法

使用 prefix-conditioned identification 固定历史前缀；从相同状态对步骤或候选动作做 replay/intervention；比较后续结果得到局部因果效应；再系统改变 Judge 可见的轨迹信息，检测完整轨迹条件化造成的偏差。

## 关键实验结果

在 12 个代码仓库的 499 条文件定位 episode 上，下一步动作主要受执行 provenance 而非代码图转移驱动；不确定性主要呈任务级结构，而非稳定的逐步属性；full-trace Judge 出现系统性 collider bias，常测到语义相关性而非经干预认证的因果贡献。

## 证据质量与局限

证据质量中等偏高：有明确因果假设、回放干预和受控 Judge 信息实验。局限是只覆盖文件定位、499 条 episode；结论能否推广到 GUI、Web 和开放工具 Agent 尚待验证，摘要未给出跨 Judge 稳定性及完整效应量。

## 最接近的相关工作

最接近 TRACE、COTA、Wrong but Useful、AgenticRAG-FP，以及基于同状态续跑的反事实信用分配。本文特别强调测量对象分层和 collider bias。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 拆成三头：动作可行性、任务级不确定性、步骤反事实贡献；禁止用同一个 full-trace prompt 同时承担三种标签。以回放结果校准步骤头，并记录 Judge 在不同可见信息条件下的稳定性。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 仅蒸馏由干预或环境结果校准的 step score，避免蒸馏语义相关性。
- **A/B/T：** 从同一 prefix 做候选动作 A/B/T 续跑，是比完整轨迹主观排序更干净的监督。
- **真值门控：** 执行结果决定方向，Judge 只补充不可程序化维度。
- **Student critique states：** critique 应针对已定位的因果步骤生成，而非对整条失败轨迹泛化归因。
- **高熵探索：** 不确定性主要是任务级时，不应把单步高熵自动解释为错误。
- **Sealed eval：** 评测 Judge 不接触训练期选择变量和后验结果，降低 collider/selection bias。
