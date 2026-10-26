# Self-Direction：把失败轨迹反思蒸馏为可路由 LoRA

- **论文标题**：Don't Forget What You Just Learned: Self-Directed Repair Turns Agent Mistakes Into Lasting Lessons
- **作者**：Yuval Kansal、Karen Ullrich、Polina Kirichenko、Ilia Kulikov、Niraj K. Jha、Mohammad Pezeshki、Mark Ibrahim
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.31846
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.31846
- **代码**：未发现公开代码链接

## 一句话结论

Self-Direction 将失败轨迹生成的“教训”立即蒸馏进约 0.02% 参数量的独立 LoRA，并在未来任务中路由复用，是 student-generated critique state 从文本记忆升级为持久策略增量的直接方案。

## 真正新增的内容

**论文原文结论**：失败后 agent 自主反思轨迹、提炼 lesson、训练小型 adapter；基座冻结，每条 lesson 独立保存并自动路由到相关任务。

**分析推断**：它解决了 critique 只在当前上下文有效的问题，但也把“错误 critique”固化成参数，因此比文本记忆更需要环境真值准入、回滚和 sealed eval。

## 核心方法

1. 失败 episode 触发自反思与 lesson 提取。
2. 将 lesson 立即蒸馏到低秩 adapter，基座权重不变。
3. adapter 进入持久库，由路由器在相似任务上加载。
4. 通过独立 adapter 隔离干扰，并允许复用少量 lesson 覆盖多任务。

## 关键实验结果

**论文原文结论**：在 GAIA、Claw-Eval、Terminal-Bench 2.1 上，Qwen 系 agent 总成功率提高 8.9–17.0 个百分点；重复错误的修复可靠性接近翻倍；少量 adapter 可迁移到数十个新任务。

## 证据质量与局限

覆盖研究、工具工作流和终端三类任务，幅度较大；但摘要未说明全部失败诊断是否经硬 oracle 验证。adapter 数量增长、路由错误、跨 lesson 冲突和长期遗忘尚需审计；“不改基座”不等于不会产生组合性副作用。

## 最接近的相关工作

接近 Reflexion、SkillAA、RSIAgent、AtomSD、DENSE、Grounding Agent Memory 与可组合 adapter/continual learning。区别是把反思直接参数化并持久路由。

## 如何复用或推进 LLM-as-a-Verifier

在训练 adapter 前增加三道 gate：失败由环境真值确认；critique 指向具体证据和责任步骤；重放显示采用 lesson 后净收益为正。verifier 还应输出适用域和反证条件，支持 adapter 退休。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：将高置信 critique 对应的 score shift 蒸馏到小 adapter，而非立刻改全模型。
- **A/B/T**：原轨迹、修复轨迹与不可判定轨迹形成 A/B/T；仅 A/B 间有硬结果差时更新。
- **真值门控**：失败与修复都必须由程序/环境验证。
- **critique states**：采用“lesson + 证据 + 适用域 + 反证条件 + adapter ID”结构。
- **探索保留**：路由不确定时并行保留无 adapter 与多个候选 adapter 分支。
- **sealed eval**：冻结未用于反思、路由和 adapter 选择的任务，检测错误固化与跨域负迁移。
