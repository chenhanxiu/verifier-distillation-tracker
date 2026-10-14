# CoEvoke：通过受控扰动诱发可纠错的多智能体轨迹

- **论文标题**：CoEvoke: Evoking Multi-Agent Collaboration for Trajectory Collection
- **作者**：Lin Wu, Shu Yao, Yuheng Wang, Jingru Fan, Huatao Li, Yihan Li, Liu Yixuan, Cheng Liu, Jian Chang, Zeyu Zhao, Aohua Zhang, Huiying Zhao, Shuyuan Zhu, Chen Qian
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2610.14021
- **代码/数据**：论文摘要未给出公开链接
- **标识符**：arXiv:2610.14021；DOI: https://doi.org/10.48550/arXiv.2610.14021

## 一句话结论

通过受控、可恢复扰动主动制造“检查—反馈—修复”状态，比被动收集自然 rollout 更容易获得对 verifier 与协作策略真正有训练价值的轨迹。

## 真正新增的内容

**论文原文结论**：CoEvoke 在跨域任务中注入可恢复困难，并用受限参考指导调查，构造 4,567 条可重建轨迹（4,130 个软件工程与推理任务），把交互、证据、决策和任务原生结果连接起来。相同训练任务、决策记录数与更新次数下，扰动增强的 judge 训练将 ACPBench-Hard 成功率从 35.38% 提高到 42.12%，SWE verifier 提升 7.60–9.40 个百分点。

**分析推断**：贡献不只是“更多数据”，而是把稀缺的纠错状态变成可控数据采样目标；这与 student-generated critique states 的覆盖问题高度同构。

## 核心方法

1. 对原始任务施加可恢复的受控扰动，避免立即通过或无信息重复失败。
2. 允许受限参考指导定位问题，但在最终工作流与后训练评测中移除私有参考。
3. 保留可重建轨迹及证据、决策、环境结果，分别训练 judge/verifier。

## 关键实验结果

- 2,287 个同任务配对中，七类扰动的反馈出现率增加 47.72–100 个百分点。
- ACPBench-Hard：35.38% → 42.12%（+6.73）。
- SWE verifier：较接口匹配、未训练参考提升 7.60–9.40 点。

## 证据质量与局限

**论文原文**提供同任务配对和训练预算匹配，优于只比较不同数据量；任务原生 outcome 也比纯 LLM judge 更可靠。局限是摘要未说明跨模型家族、长期闭环训练后是否仍稳定，受限参考可能带来轨迹分布偏移；“更多反馈”也不自动等于“更正确反馈”。

## 最接近的相关工作

与 GLARE 的 on-policy 负样本更新、DENSE 的证据化恢复状态、PaperDoctor 的证据指针以及 student-generated critique-state 准入最接近。区别在于 CoEvoke 主要解决“如何主动生成纠错轨迹”。

## 如何复用或推进 LLM-as-a-Verifier

- 在 student 高熵或反复失败状态注入可恢复 perturbation，要求 verifier 给出证据指针、错误类型和修复建议。
- 用任务原生 outcome 过滤 critique，再蒸馏为生成式 verifier。
- 把同任务无扰动/扰动轨迹组成 A/B/T：修复优于未修复，证据不足为 T。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：把现有采样器从“按策略熵分叉”升级为“策略熵 × 可恢复扰动价值”分叉；score-level OPD 只在程序/环境真值确认方向后吸收 teacher 幅度。高熵分叉保留多个修复路径，不把单一参考修复硬蒸馏成唯一答案。sealed eval 必须使用未见扰动、冻结任务原生检查器与无私有参考的轨迹，防止 verifier 与扰动模板共适应。