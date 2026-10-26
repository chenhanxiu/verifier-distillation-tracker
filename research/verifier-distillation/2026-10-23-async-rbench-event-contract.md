# Async-RBench：异步 Agent 的事件响应契约评估

- **论文标题**：Async-RBench: Benchmarking Asynchronous Task Execution in LLM Agents
- **作者**：Detao Zeng、Guilin Ou、Nuo Chen、Yunhao Feng、Hongliang Wang、Qinli Yang、Junming Shao、Zhong Zhang
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32429
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32429
- **代码**：https://github.com/pope8zdt/Async-RBench

## 一句话结论

Async-RBench 用可执行事件控制器和私有 Event Response Contract 同时检查“该改、该保留、不得改、需重验”，为异步 sub-agent 长轨迹提供了比终局成功更细的程序真值 verifier。

## 真正新增的内容

**论文原文结论**：200 个可执行任务覆盖八类异步场景；controller 按预定义状态条件释放 sub-agent 结果，ERC 规定每次响应的更新、保持、禁止和复验义务，DRS 将过程与终局各占一半。

**分析推断**：ERC 可直接转成事件级序数 verifier 与 hard gate，尤其适合陈旧结果、重复报告和 sub-agent 失败等长时程分支。

## 核心方法

1. 控制异步结果到达时机，保证可复现。
2. 为每个事件定义私有响应契约。
3. 分别检查变更、保留、禁止动作与重新验证。
4. DRS 将过程履约与最终结果分开并等权汇总。
5. 公开信息与 evaluator 私有证据边界明确隔离。

## 关键实验结果

**论文原文结论**：九个 Agent 的 DRS 为 19.2–45.1；重复报告和 sub-agent 失败最弱。异步交付的平均任务成功率低于批量交付（26.0% 对 29.7%）。对三个 Agent 强制每次结果后重建计划，只提高 DRS 2.6–3.5 点。

## 证据质量与局限

环境可执行、事件可控、代码公开，适合复现；但仅 200 任务，DRS 的过程/结果 50:50 权重带有人为选择。私有 ERC 提高 sealed 性，同时限制外部检查；未研究训练时反复访问 evaluator 的共适应。

## 最接近的相关工作

接近 GCAC、ContrAgent、DynaWeave、Ground-truth-as-code、AuditKIT 与 DynSTEER。区别是专门建模异步结果导致的状态陈旧和复验义务。

## 如何复用或推进 LLM-as-a-Verifier

把 ERC 编译成 verifier feature：每个事件输出四类履约分布及证据；硬违反直接 fail，剩余维度形成序数分布。LLM Judge 只解释原因，程序检查器负责事实。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：按事件而非整轨迹蒸馏，硬违约决定方向、DRS 子分控制幅度。
- **A/B/T**：同一异步事件的两种响应构成 A/B；证据尚未到达时标 T。
- **真值门控**：ERC 和环境快照充当不可绕过的 teacher 层。
- **critique states**：保存待处理义务、陈旧状态和必须重验项。
- **探索保留**：允许多个并行 sub-agent 分支，直到依赖条件满足再裁剪。
- **sealed eval**：隐藏事件调度、ERC 与 verifier state，防止 Agent 适配固定到达顺序。
