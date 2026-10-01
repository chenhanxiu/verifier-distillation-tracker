# Learning When and How to Intervene: A Hindsight-Distilled Sentinel for Coding Agents

- **作者**：Jiangrui Zhao, Chenglong Li, Meng Zhang, Xiaoting Du
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.39957
- **代码**：未发现公开代码链接

## 一句话结论

HiSentinel 将看过执行结果的 privileged teacher 蒸馏为仅看动作前上下文的轻量 sentinel，学习放行、自动重定向或请求人工协助。

## 真正新增的内容

【论文原文】目标不是纠正每个不完美动作，而是判断执行前干预是否能提高最终任务完成率。SWE-Intervene 提供 allow、redirect、pause-for-human 三类动作级标签及可执行反馈。

【分析推断】这把 hindsight verifier 变成部署时因果干预器，天然对应 A/B/T 中的“放行/替代/不确定升级”。

## 核心方法

privileged teacher 使用记录的执行结果判断干预价值；将其蒸馏给 0.6B/1.7B student，student 只接收 pre-action context 与 proposed action，同时生成可操作反馈。

## 关键实验结果

【论文原文】在 SWE-bench Verified Mini 与 Ask or Assume 上，跨 sentinel 尺寸和 coding-agent 家族稳定提高任务完成率，最高分别提升 14% 和 10%，token 消耗仍具竞争力。

## 证据质量与局限

有不同 agent family 与两类任务，但 intervention 标签源自 privileged teacher，摘要未给人工校准、误拦截成本与真实生产副作用。

## 最接近的相关工作

The Tasteful Agent、Persistent Teacher Anchoring、TwinCheck、BLINDSPOT、Monitoring Reward Hacking。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输出转为三路 policy：allow、redirect、escalate，并要求每次 redirect 附带可验证修改；分别报告阻止错误和错误阻止的成本。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：蒸馏“干预带来的终局增益”，而非动作表面正确性。
- **A/B/T 与序数分布**：allow/redirect/pause 可映射为 A/B/T，保留三类概率。
- **硬真值门控**：不可逆工具动作仍由测试、权限和状态断言硬拦截。
- **student-generated critique states**：redirect feedback 只有执行改善后才进入 critique 训练集。
- **高熵分叉**：高不确定且高风险时升级人工；低风险则保留探索。
- **sealed eval**：使用独立仓库任务与隐藏测试，防止 sentinel 和 actor 共适应。
