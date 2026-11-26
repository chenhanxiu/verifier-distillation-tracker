# Evaluating More with Less：面向 Agent sealed eval 的黑盒测试选择

- **论文标题**：Evaluating More with Less: Black-Box Test Selection for AI Agents
- **作者**：Ali Asgari, Mitchell Olsthoorn, Arie van Deursen, Annibale Panichella
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.34617
- **DOI**：https://doi.org/10.48550/arXiv.2611.34617
- **代码链接**：未见公开代码

## 一句话结论

无需运行目标 Agent 或读取历史结果，黑盒任务选择就能用 20% 预算较准估计成功率或优先暴露失败，为昂贵 sealed eval 提供预算分配方案。

## 真正新增的内容

**论文原文结论**：首次系统比较 Agent benchmark 的黑盒 test-case selection，区分成功率估计与早期失败发现两个目标。**分析推断**：sealed eval 可以节省成本，但不能只用 LLM Judge 挑“难题”，否则选择器与 evaluator 可能共适应；应保留概率抽样审计。

## 核心方法

用任务描述、元数据、代码片段和 embedding 选择测试；另以启发式或独立 LLM Judge 估计难度。14 种策略在 10 个 benchmark、每个 12–101 个 Agent 上比较，且不执行被测 Agent。

## 关键实验结果

Category Partition 在 20% 预算下于 5 个 benchmark 取得最低中位成功率估计误差。GPT 5.2 Codex 在 SWE-bench Verified 上由 500 题缩至 100 题，成本从 225 美元降至 47 美元，误差 0.8 点；同预算下 Judge 选择暴露失败率 53.0%，随机为 27.4%。

## 证据质量与局限

跨 10 个 benchmark 的规模较强，并明确显示没有单一策略同时支配估计与找错。局限是选择偏差会改变误差分布；摘要未给出对自适应训练循环的 anytime-valid 保证。

## 最接近的相关工作

与 AutoTuneBench、Transport-Safe Evaluation、EPIG-Tree 的信息价值采样和 SealedLoop 的序贯验收相关。

## 如何复用或推进 LLM-as-a-Verifier

将 sealed task pool 分成概率样本和定向难例；概率样本估计无偏整体指标，Judge 选择样本发现失效模式。A/B/T 与序数分布均需记录抽样权重。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：训练期按高熵和 verifier 分歧定向采样，sealed eval 采用“随机主样本+难例补充”双轨；禁止用同一 Judge选择、评分并决定 checkpoint。分别报告总体估计、失败检出率和有效样本量。
