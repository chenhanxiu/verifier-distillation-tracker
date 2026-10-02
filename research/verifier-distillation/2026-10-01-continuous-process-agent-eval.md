# Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills

- **作者**：Ngoc Phuoc An Vo, Aarya Doshi, Vadim Sheinin
- **首次公开日期**：2026-10-01
- **版本日期**：2026-10-01（v1）
- **原始论文**：https://arxiv.org/abs/2610.01833
- **代码**：未发现公开代码链接

## 一句话结论

即使最终数值检查通过，92% 以上企业 Agent 运行仍存在其他 evaluator 可检测的轨迹偏差，说明终局正确远不足以代表过程可靠。

## 真正新增的内容

【论文原文】框架独立计算每次运行的 ground truth，生成可复用 template test，并用程序检查与窄范围 LLM Judge 评估工具选择、参数、执行顺序和数据库完整性；dependency attribution 把多项失败归并为根因。

【分析推断】这与用户现有“最终状态＋步骤边际贡献”双层评估高度吻合，并强调 API/spec 变化下 regression template 必须运行时解析。

## 核心方法

组合 outcome/process checks；每次运行重新计算真值；跨 skill、spec、harness 与 model 做矩阵评测；用依赖图把派生失败归因到少量根检查。

## 关键实验结果

【论文原文】240 次 trial 中，175 次通过全部适用最终数值检查，其中 162 次（92.6%，95% CI 87.7–95.6%）仍有其他偏差；更宽的七项 final-state 定义下，164 次通过中 151 次（92.1%）违反 trajectory check。每次平均 6.34 个失败检查被归为 2.65 个根因。

## 证据质量与局限

报告置信区间、240 次运行和多配置交互；但仅两个企业 skill，论文也明确尚未完成真实 API 长期演化验证。

## 最接近的相关工作

Dr.Credit、DynSTEER、GCAC、Ground-truth-as-code、Executable-Contract Audit。

## 如何复用或推进 LLM-as-a-Verifier

将五维 rubric 拆成可执行检查优先、窄 Judge 补充；评分前输出 failure dependency graph，避免同一根因重复扣分。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：根因级分数优于把多个派生检查重复累加。
- **A/B/T 与序数分布**：程序检查定硬标签，开放语义项保留序数分布或 T。
- **硬真值门控**：每次运行动态计算 GT，并验证工具参数、顺序和数据库状态。
- **student-generated critique states**：critique 应引用根检查及状态证据。
- **高熵分叉**：多条合格路径可通过 template invariants，而非固定参考轨迹。
- **sealed eval**：冻结 regression template 生成规则、依赖图和窄 Judge 版本。
