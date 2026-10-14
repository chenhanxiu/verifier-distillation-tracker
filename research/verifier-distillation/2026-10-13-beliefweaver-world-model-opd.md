# BELIEFWEAVER：用信念更新、世界模型与 OPD 做长时程失败恢复

- **论文标题**：Failure Recovery via Belief Updates and World Modeling for Long-Horizon Agents
- **作者**：Xiyang Wu, Zhichao Liu, Shengxin Zhang, Zongxia Li, Ming Li, Tianyi Zhou, Dinesh Manocha
- **首次公开日期**：2026-10-13
- **版本日期**：2026-10-13（v1）
- **原始论文**：https://arxiv.org/abs/2610.18082
- **代码**：论文摘要未给出公开链接
- **标识符**：arXiv:2610.18082；DOI: https://doi.org/10.48550/arXiv.2610.18082

## 一句话结论

BELIEFWEAVER 将跨尝试执行证据、诊断门控和前瞻世界模型组织成持久信念状态，再把反复出现的世界模型推理通过 SFT+OPD 蒸馏到 9B student，兼顾恢复能力与 teacher 成本。

## 真正新增的内容

**论文原文结论**：框架维护 frontier、attempt、observation、checkpoint 的关系信念；执行证据跨回滚更新 frontier 优先级，诊断证据门控执行，隐式世界模型评估修复假设和进展。三个 terminal benchmark 上总体最终分比原生 Terminus-2 continuation 高 5.1 点；蒸馏 9B student 比报告的原生基线高 9.8 点，并比匹配 teacher 降低估算 API 成本 54.8%。

**分析推断**：这几乎直接给出 student-generated critique states 的结构：假设、证据、frontier、预期进展和回滚点，而非自由文本反思。

## 核心方法

1. 跨尝试保留关系化 belief state。
2. 用环境执行证据更新 frontier，用诊断证据决定是否执行。
3. IWM 评估修复假设、预测进展并关联不同 frontier。
4. 将重复 IWM 推理以 SFT + on-policy distillation 内化到 9B student。

## 关键实验结果

- 三个 terminal benchmark：总体最终分 +5.1 个百分点。
- 9B student：较报告原生基线 +9.8 点。
- 相对匹配 teacher：估算 API 成本 -54.8%。
- 探索效率呈正向趋势，但摘要未给显著性区间。

## 证据质量与局限

跨三个终端环境且包含成本比较，和长轨迹 Agent 高度贴合。局限是结果相对“报告的原生基线”，摘要未说明完整 matched ablation、真值覆盖率及 sealed evaluator；IWM 预测错误可能通过 OPD 固化。

## 最接近的相关工作

与 DENSE、RSIAgent、SkillAA、Continual Search for Long-Horizon RCA、The Tasteful Agent 和 FLARE 最接近。

## 如何复用或推进 LLM-as-a-Verifier

- 将 verifier state 明确拆成：当前 frontier、证据、修复假设、进展分布、回滚可恢复性。
- 只有经环境执行确认的 belief update 才进入高权重蒸馏。
- 把多个修复 frontier 形成 pairwise A/B/T；证据不足时保留 T 和探索。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：可直接新增“自由文本 critique”与“关系 belief-state critique”的对照。score-level OPD 蒸馏每个 frontier 的成功概率分布，而非单一全轨迹分；环境结果定方向，IWM 只定幅度。高熵分叉按预期信息价值和可恢复性分配预算。最终用未见 terminal 任务、冻结执行检查器与独立 evaluator 做 sealed eval，单独报告恢复率、错误回滚率、teacher 调用成本和探索多样性。