# SkillAA：归因驱动的 Skill Graph 更新、验证与回滚

## 元数据
- **论文标题**：SkillAA: Attribution-Guided Skill-Graph Updating with Targeted Validation and Rollback
- **作者**：Ziqiao Shang、Ling-Yue Ge、Lan-Zhe Guo
- **首次公开日期**：2026-09-17
- **版本日期**：2026-09-17（v1）
- **原始论文**：https://arxiv.org/abs/2609.20455
- **代码链接**：未发现公开代码链接

## 一句话结论
从失败轨迹直接改整段 memory/skill 风险过高；应先用成败对照归因到具体图节点，只局部修改，并经 Local Gate 与 Big Gate 验证后提交或回滚。

## 真正新增的内容
**论文原文结论**：SkillAA 用统一图表示 skill 的适用、执行与组合关系；通过成功/失败执行对照进行 abductive attribution，把修复路由到具体图对象，并做局部和全局两级验证。

**分析推断**：这是 student-generated critique/memory 准入的直接工程模板，可把 critique 从自由文本变成“失败证据—责任节点—局部修复—验证结果”的结构化状态。

## 核心方法
- skill graph 显式表示语义边界、对象地址和拓扑依赖。
- 对比成功与失败执行定位候选责任对象。
- 仅更新选中的局部结构。
- Local Gate 检查局部目标，Big Gate 检查整体回归，不通过则回滚。

## 关键实验结果
**论文报告**：使用 gpt-5.6-sol 时，SearchQA、LiveMath、DocVQA 分别达到 81.5%、66.7%、91.2%，所有主要设置中平均表现最高。

## 证据质量与局限
三类任务和门控消融方向具有工程价值。局限是只报告一个主模型；外部 skill 更新不等于参数级 verifier distillation；门控若与更新共享 evaluator，仍可能共同过拟合。

## 最接近的相关工作
APEx、RSIAgent、Grounding Agent Memory、LongWoF-Bench 与 EDGE 都涉及经验/记忆准入或错误归因；SkillAA 强化了局部地址、两级 gate 与回滚。

## 如何复用或推进 LLM-as-a-Verifier
将 verifier critique 写成 typed patch：证据指针、责任 skill 节点、修改范围、预期效果和回滚条件。Local Gate 用定向重放，Big Gate 用独立回归集；只有两者通过才进入长期 memory 或 OPD 数据。

## 对 Agent verifier × OPD 实验路线的具体影响
- **score-level OPD**：只在责任节点及其依赖范围内更新，降低错误 teacher 信号扩散。
- **A/B/T**：修改前后形成 A/B；局部改善但全局不确定时标 T。
- **真值门控**：环境重放决定 Local Gate，独立回归决定 Big Gate。
- **critique states**：采用结构化、可回滚 patch。
- **高熵探索**：保留多种局部修复，不一次覆盖整个 skill。
- **sealed eval**：Big Gate 必须与修复生成和 Local Gate 隔离。