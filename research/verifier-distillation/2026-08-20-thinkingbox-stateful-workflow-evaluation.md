# One Success Isn't Reliability: Thinkingbox, a Sandbox and Benchmark for Agents in Stateful Business Workflows

## 基本信息

- **作者**：Zhuochun Li、Youngmin Ko、Ali Keramati、Nicola Ferri、Susana Palmaz Lopez Pelaez、Liang-Chun Tsai、Calvin Wang、Mirco Milletari、Tuhin Kundu、Vadim Smolyakov、Kjartan Olafsson、Tommy Guy
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.19741
- **DOI**：10.48550/arXiv.2608.19741
- **原始论文**：https://arxiv.org/abs/2608.19741
- **代码**：https://github.com/microsoft/thinkingbox

## 一句话结论

对于带持久状态和副作用的长时程工具 Agent，“正常结束、调用过写工具、最后没有报错”都远不足以证明任务完成；必须对最终后端状态、遗漏效果和额外副作用做可执行检查，并用重复试验区分偶然成功与可靠成功。

## 真正新增的内容

**论文原文结论**：Thinkingbox 提供隔离的 MCP 工具会话、完整执行轨迹和后端终态检查；Thinkingbox-bench 覆盖 507 个受政策约束的业务工作流，并引入 pass@k 与“k 次全部成功”的 pass^k 对照，揭示可发现成功路径与稳定复现之间的巨大差距。

**分析推断**：该框架提供了 Agent verifier × OPD 所需的高质量 outcome teacher：可以从同一初态重复采样学生轨迹，以可执行终态和副作用差异构造 A/B/T、序数可靠性和局部 credit 数据。论文自身不是蒸馏算法。

## 核心方法

1. 为零售、预订、保险、neobank、咨询 IT/HR 等业务域构造隔离后端、MCP-compatible 工具和持久数据库。
2. 每个任务以 task-specific executable checks 验证预期状态、字段值、集合长度、缺失效果和额外副作用；部分任务同时检查最终回复要求。
3. 对 12 个模型、每任务 20 次重复试验，分别报告单次成功率、至少一次成功的 pass@20 和 20 次全部成功的 pass^20。
4. 保留完整轨迹和后端差分，用于区分工具使用表面正确与真正业务完成。

## 关键实验结果

**论文原文结果**：

- 数据集含 507 个任务；每个任务 20 次试验。最强 GPT-5.4 的 pass@1 为 65.36%（95% CI 62.23%–68.51%），pass@20 达 91.12%，但 pass^20 仅 25.25%。
- Claude Sonnet 4.6 的 pass@1/pass@20/pass^20 分别为 58.45%/88.56%/20.12%；多个模型的 pass@20 较高但 pass^20 接近零。
- 在 79,853 条最终被可执行检查判失败的轨迹中，84.86% 看起来“正常结束”，80.88% 还执行过状态修改工具，67.24% 的最后工具响应没有显式错误。
- 可执行检查在失败轨迹中发现：98.95% 数据库哈希不匹配、77.61% 字段值错误、25.36% 缺少预期状态/副作用、43.30% 存在额外非预期副作用。

## 证据质量与局限

- **证据质量：高（作为评估基础设施证据）。** 任务数量较大、12 个模型、20 次重复、任务簇 bootstrap 区间，并有清晰的弱 evaluator 消融。
- 业务域由沙箱实现，尚不能保证覆盖真实企业系统的权限、并发、延迟和不可逆副作用。
- task-specific checks 仍由 benchmark 作者定义，检查遗漏会形成 verifier blind spot。
- 公开任务和 evaluator 可能被后续系统针对性优化；长期使用需要隐藏任务和独立测试版本。
- 论文证明了 outcome verifier 的必要性，但没有验证如何将其蒸馏为轻量过程 verifier。

## 最接近的相关工作

最接近 τ-bench、ToolBench/BFCL、SWE-bench、Terminal-Bench 及执行式 Agent benchmark。关键差异是把终态持久变更、额外副作用和重复可靠性作为一等评估对象，而非只看回答、单次工具调用或至少一次成功。

## 如何复用或推进 LLM-as-a-Verifier

- 以可执行终态为最高优先级真值，用 LLM Judge 解释失败原因而非替代终态判定。
- 从数据库差分生成结构化 critique：错误字段、遗漏效果、额外效果、政策违规和回复缺陷。
- 训练轻量 verifier 预测完整 executable verdict，同时保留分项概率，避免只有单一 pass/fail。
- 对无法程序化的沟通质量使用独立 LLM Judge，但必须与后端状态分开报告和校准。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：将后端分项检查转换为多维 outcome score，再从学生自身 rollout 蒸馏到过程 verifier。
- **A/B/T 与序数分布**：同一初态的多次轨迹可按“完全正确/部分正确但有副作用/失败”形成 T 桶和序数分布；pairwise 比较应以状态差分为依据。
- **程序化真值门控**：可执行检查应门控 teacher 信号方向；LLM critique 只能补充 credit assignment。
- **student-generated critique states**：让 student 根据状态差分生成失败解释，再由隐藏检查验证解释是否覆盖真实错误。
- **高熵分叉探索**：pass@20 高而 pass^20 低说明可行路径存在但策略不稳定；训练应保留成功少数分叉，不能因多数失败而抹掉。
- **sealed eval**：保留隐藏后端 schema、任务变体和检查器；训练只接触可解释的公开子集，最终用独立环境与多次重复评估可靠性。