# Crucible：用隔离可执行化学环境与沙箱 grader 评估研究 Agent

- **论文标题**：Crucible: Evaluating LLM Agents in Executable Chemistry Research Environments
- **作者**：Yinjun Liu, Xinye Li, Ruisen Peng, Lang Gao, Zixiang Xu, Zirui Song, Xiuying Chen
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.34254
- **DOI**：https://doi.org/10.48550/arXiv.2611.34254
- **代码链接**：未见公开代码

## 一句话结论

Crucible 用 7 个隔离环境、75 个专业工具和沙箱 grader 覆盖完整 DMTA 研究闭环，展示了长轨迹 Agent 的程序化/环境真值层。

## 真正新增的内容

**论文原文结论**：基准不再只测问答，而验证设计、合成、实验、闭环优化、模拟和分析的实际产物；工具调用成功并不保证化学有效。**分析推断**：这正是 verifier teacher 应分离“工具执行成功”和“科学结果有效”的证据。

## 核心方法

1,078 个任务、12 个任务族、18 个公开数据源；Agent 通过 MCP 访问工具，沙箱 grader 验证路线、协议和产物。实验任务使用机器人模拟器或已测量数据，减少纯语言 Judge 依赖。

## 关键实验结果

14 个模型中最佳总体分数为 0.545；合成规划和闭环优化最难。总体排名不能预测优化能力，第 12 名模型反而在闭环优化最高；Agent 常在工具成功后提交化学无效结果。

## 证据质量与局限

任务覆盖广、环境隔离且 grader 可执行，适合作为硬真值 benchmark。局限是沙箱与历史数据仍是现实近似，科学有效性和 grader 完备性需专家审计；论文未研究 verifier 蒸馏。

## 最接近的相关工作

与 AutoGym、Ground-truth-as-code、GameLogicBench 和 Reality Is the Final Verifier 相近。

## 如何复用或推进 LLM-as-a-Verifier

将环境断言蒸馏为过程 verifier：每个阶段输出成功概率、未满足义务和证据指针。程序结果决定硬门控，generative verifier 负责解释和归因；无法执行的结论保留 T。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：在长轨迹中分别监督 tool success、domain validity 与终局目标，避免单一总分；对共享状态分叉保留多条有效路线。sealed eval 使用隐藏输入、独立沙箱和未见工具组合，检查 evaluator 共适应。
