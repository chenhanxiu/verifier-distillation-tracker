# MC-EvoBench: Auditing Experience-Driven Self-Improvement in Minecraft Agents

- **作者**：Jingwei Song；Zhisheng Chen；Bingfan Zeng；Jing Tang；Yubo Hou；Jinhao Jing；Zhengwei Xie；Linfeng Zhang
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13829
- **Canonical URL**：https://arxiv.org/abs/2610.13829
- **代码与数据**：https://github.com/xzw-ustc/mc-bench-open-source

## 一句话结论

MC-EvoBench 通过重置目标世界、限制只有声明的 Agent artifact 能跨越 source–target 边界，并使用阶段级环境 verifier，证明“保存了 memory 或完成过任务”并不等于获得了可迁移能力。

## 真正新增的内容

【论文原文】基准注册 19 条 evolution chain，其中 12 条主评测链、7 条校准/探测链，并构造 3 组图对齐的迁移 probe；每个任务用 task-state graph 表示，定义阶段级环境 verifier，在 matched budget 与 5 个随机种子下比较 no-prior、related、unrelated 和 shuffled source。

【分析推断】这是 sealed eval 防止 evaluator/agent 共适应的完整模板：清空环境资源、隔离训练经历、只允许明示 artifact 迁移，并用结构匹配的负对照区分真实能力与携带资源。

## 核心方法

1. 用 task-state graph 描述阶段、依赖和可验证里程碑。
2. 在 source world 中允许 Agent 形成 memory/skill/artifact。
3. 重置 target world，只让预先声明的 artifact 跨越边界。
4. 设置 related、unrelated、shuffled 与 no-prior 对照，保持环境步预算一致。
5. 以 stage verifier、五种子和 provenance records 评估 transfer，并区分早期执行失败导致的未观测能力。

## 关键实验结果

【论文原文】基准发现 controller 与 planner-backed variant 存在稳定的直接能力差距，但 related experience 没有稳定迁移收益：两个工具 probe 均无改善，小幅 wood-species 收益依赖单一种子，所有区间都包含零。阶段审计显示，早期木材收集和合成瓶颈经常使后续能力根本未被观察。

## 证据质量与局限

【论文原文】配对 probe、多个负对照、世界重置、matched budget、五种子和 provenance 提供了较强的因果审计结构。  
【局限】Minecraft 的离散状态和可重置环境比真实办公/移动端简单；仅允许单一声明 artifact 可能低估分布式 scaffold 的真实迁移。未观测后期能力与真正不会之间仍需选择性测试区分。

## 最接近的相关工作

与 AutoTuneBench、Harness or Model?、Agents Are Systems, Not Models、GameLogicBench、SkillAA、RoboRSI、RSIAgent 和 A Trust Layer for Agent Evaluation 最接近。MC-EvoBench 的突出贡献是对自改进声明进行 source–target 隔离审计。

## 如何复用或推进 LLM-as-a-Verifier

将现有 Agent 能力评测改成 paired transfer：在 source case 中允许生成 memory/critique/skill，在同构但重置的 target case 中只注入指定 artifact。阶段 verifier 记录每个能力是否真正被访问；未到达阶段输出 T/不可观测，而不是判负。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：只有能在重置 target 中改善结果的 critique/skill 才获得正蒸馏权重；source 内成功不够。
- **A/B/T 与序数分布**：A/B 比较 related 与 matched controls；未访问目标阶段的轨迹标 T，并报告可观测性后验。
- **程序化/环境真值门控**：task-state graph 与阶段检查器提供硬真值；memory 中的自我声明不计分。
- **student-generated critique states**：critique 跨 source–target 迁移后仍能复现修复，才允许进入长期库。
- **高熵分叉**：对早期瓶颈进行分层 rollout，确保后期能力获得评测机会，避免只因未到达而被裁剪。
- **sealed eval**：重置目标环境、限制跨界 artifact、加入 unrelated/shuffled 对照并保留 provenance，直接防止 evaluator 与训练轨迹共适应。

总体判断：【分析推断】这篇工作可直接转化为用户现有 3,800 case 体系中的“能力迁移验收层”，尤其适合验证自动评测 Agent 生成的 memory 和 critique 是否真正可复用。