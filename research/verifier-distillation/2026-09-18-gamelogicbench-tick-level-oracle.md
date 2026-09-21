# GameLogicBench：用逐 Tick 状态断言评测长时程 Coding Agent

- 论文标题：GameLogicBench: Evaluating Coding Agents on Runtime Game Logic with Tick-Level State Assertions
- 作者：Xinyu Che；Yunfei Ge；Shihao Li；Yanchen Liu；Hang Yan；Xinping Lei；Yanghai Wang；Zixuan Dong；Yifan Yao；Qianqian Xie；Letian Zhu；Jiaheng Liu
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21562
- DOI：https://doi.org/10.48550/arXiv.2609.21562
- 代码与 benchmark：https://github.com/NJU-LINK/GameLogicBench

## 一句话结论

GameLogicBench 证明终态正确会掩盖执行过程中的规则违规；逐 tick、可复现、经 mutant 验证的环境 oracle，适合作为长轨迹 verifier 蒸馏中不可覆盖的硬真值层。

## 真正新增的内容

- 【论文原文】构建 72 个 Godot gameplay-logic 任务、403 个手工场景，并通过 seeded 参数变化形成 1,451 个测试。
- 【论文原文】evaluator 在每个 simulation tick 检查规则，而不只检查最终状态；同一标准允许不同正确实现。
- 【论文原文】用删除一个必要能力的 mutant 验证每项 criterion 确实能拒绝错误实现。
- 【论文原文】将网络出口密封纳入评测协议，发现开放网络时 Agent 会复制公开仓库代码，污染能力测量。
- 【分析推断】它提供了“过程真值”而非 LLM Judge 的过程印象，可用于给每步动作、违规时刻和可恢复性生成监督。

## 核心方法

任务按 Atom、Combo、Repo 三个集成层级组织。Agent 修改项目并运行游戏；评测器选择场景、固定随机种子，在运行期逐 tick 读取状态并执行规则断言。每个标准同时在正确实现与 mutants 上验证。模型和 scaffold 组合在密封出口条件下运行，记录成功率、轮数、费用和工具行为。

## 关键实验结果

- 【论文原文】20 个 model–scaffold 组合中，最佳 Claude-Opus-5 + Claude Code 解决 52.78% 任务；Atom、Combo、Repo 分别为 61.90%、53.57%、43.48%。
- 【论文原文】74.3% 的失败场景可以运行，但违反了必需行为，说明只看可运行性或终态会漏掉主要失败。
- 【论文原文】没有 mutant validation 的 evaluator 会放过错误 Agent 提交。
- 【论文原文】同一 Qwen-3.8-Max 在不同 scaffold 的解题率为 26.39%–44.44%；相同成功率的配置成本最多相差 25 倍。
- 【论文原文】99.0% 会话至少启动一次引擎；任务范围越大，Agent 工具调用和检查行为越多。

## 证据质量与局限

- 【论文原文】真实项目、逐 tick oracle、mutant adequacy、20 个配置及网络污染分析，工程证据强，且代码/benchmark 已公开。
- 【论文原文】只覆盖可确定性断言的 gameplay logic，不评估内容深度、美术、呈现和整体玩家体验；未来才会覆盖更长交互和更多 runtime signals。
- 【论文原文】每个配置只运行一个 sample，随机波动和 pass@k 稳定性证据不足。
- 【分析推断】逐 tick 断言本身也可能 specification incomplete；mutant set 只能证明对已设计错误的敏感度，不能证明 oracle 完备。
- 【分析推断】它是 Agent verifier 的训练/评测环境，不是 verifier distillation 算法；价值在于提供硬标签与 sealed protocol。

## 最接近的相关工作

最接近 SWE-bench、Terminal-Bench、GameCraft-Bench、V-GameGym、WebGameBench 和 mutation testing。与 Ground-truth-as-code、ContrAgent、MAGS 的共同点是把规范编译为可执行真值；本工作特别强调运行全过程而非终态。

## 如何复用或推进 LLM-as-a-Verifier

将逐 tick 断言输出转换为结构化事件：首次违规 tick、违反规则、前置状态、触发动作、后续是否恢复、最终状态。LLM verifier 只负责把事件映射为人类可读 critique、能力维度和 0–3 序数分；不得覆盖 oracle verdict。训练时可蒸馏“何时将失败”的分布，推理时用于早停或分叉。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：使用首次违规时间、违规严重度和恢复结果构造 dense score；硬 oracle 决定正负方向。
- pairwise A/B/T：同一状态分叉后比较首次违规、完成度和恢复性；均满足规范但路径不同则标 T/等价成功。
- 真值门控：逐步断言和 mutant adequacy 作为 teacher signal 的不可覆盖层，LLM Judge 只补充目标推进与效率。
- student-generated critique states：critique 必须引用具体 tick 与状态差分，经 replay 后才可写入记忆。
- 高熵探索：只剪掉已确定进入不可恢复违规的分支；尚未违规且可恢复的多路径继续保留。
- sealed eval：冻结 evaluator、mutants、seed 和网络出口；隐藏一部分场景与 mutants，分别报告模型、scaffold、成本、pass@3 和 pass^3，避免 evaluator 与 Agent 共适应。
