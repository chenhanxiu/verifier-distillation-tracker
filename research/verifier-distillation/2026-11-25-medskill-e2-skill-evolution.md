# MedSkill-E²：从执行反馈蒸馏可复用的 Agent skill 指引

- **论文标题**：MedSkill-E²: Evaluating and Evolving Skills for Medical Agents
- **作者**：Jingjing Hua, Shaocong Wei, Jianghan Shen, Junzhi Ning, Min Cen, Cheng Tang, Ziyan Huang, Jiepeng Li, Fengshuo Liu, Kangkun Mao, Mouxiao Bian, Yirong Chen, Ming Hu, Jiyao Liu
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.34250
- **DOI**：https://doi.org/10.48550/arXiv.2611.34250
- **代码链接**：未见公开代码

## 一句话结论

Agent 即使打开正确 skill 也常不会用；EBU-Evolve 把自主执行与显式引导执行的反馈差异蒸馏回 skill 指令，使改进跨模型和 harness 迁移。

## 真正新增的内容

**论文原文结论**：提出 Enable But Underuse（EBU）并以同一 skill 的自主/显式引导差距测量；再利用两种执行反馈重写可复用指令。**分析推断**：这可转化为 student-generated critique 的准入机制：只有能解释并修复真实执行差距的 critique 才进入 skill/memory。

## 核心方法

EBU-Bench 覆盖 12 组医疗任务；在模型与 skill 固定时比较自主使用和强制阅读应用。EBU-Evolve 根据失败轨迹与引导成功轨迹提炼诊断指导，更新 skill 后在未见任务、模型和 harness 上验证。

## 关键实验结果

所有模型—harness 组合均出现 EBU，平均差距 43.94 个百分点；同模型跨 harness 的自主 skill 使用准确率相差最高 38.96 点。演化后准确率提升 33.33–55.17 点，并能跨模型与 harness 迁移。

## 证据质量与局限

配对设计隔离了“有无知识”和“是否执行”，跨 harness 结果有说服力。局限是医疗任务风险高、评分与 skill 更新可能共享偏差；未公开代码时难复核反馈过滤与数据泄漏。

## 最接近的相关工作

与 SkillAA 的归因—验证—回滚、RSIAgent 的验证记忆、Grounding Agent Memory 和 DENSE 的证据化轨迹蒸馏最接近。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出“skill 已访问/规则已识别/约束已执行/结果已验证”的序数分布；只有环境或程序检查确认的差异可生成 critique-state 更新，证据不足则为 T。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：增加自主与显式引导的 paired A/B 轨迹，并蒸馏其 score 差与归因；跨 harness 作为 sealed eval。高熵分叉中保留不同 skill 应用策略，避免将单一引导路径误当唯一正确解。
