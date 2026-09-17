# REVERSAL-BENCH：不可逆长时程学习与 Reset Oracle

## 元数据

- **论文标题**：REVERSAL-BENCH: A Reversibility Axis and Reset Oracle for Measuring the Reset-Free RL Cliff
- **作者**：Riyaaz Shaik、Chandru Venkataraman
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（v1）
- **原始论文**：https://arxiv.org/abs/2609.17745
- **代码链接**：论文称发布 benchmark suite 与数据集；arXiv 页面未给出可核验代码 URL

## 一句话结论

长时程 Agent 的关键 verifier 不只要预测“是否成功”，还要估计当前状态是否仍可恢复；不可逆性上升会使 reset-free 学习出现突变式失败。

## 真正新增的内容

**论文原文结论**：REVERSAL-BENCH 用连续参数控制环境可逆性，并提供检测状态可恢复性的 ground-truth reset oracle；跨八个 manipulation 设置和五个物理引擎，reset-free Agent 随不可逆性增加出现稳定的吸收式失败，而 episodic Agent 相对稳定。

**分析推断**：recoverability 应作为长轨迹 distributional verifier 的独立序数轴。对高熵分叉，不应只比较即时 reward，还应保留能维持可恢复性的分支，并在不可逆动作前提高 teacher/环境验证预算。

## 核心方法

- 用连续参数 ρ∈[0,1] 控制不可逆性。
- reset oracle 提供状态可恢复性的环境真值。
- 在几何相同的可逆/不可逆对照环境中比较多类 actor–critic、safe RL 与 reset-free 方法。
- 评估在不可逆失败前介入的 safety shield。

## 关键实验结果

**论文报告**：八个 manipulation 设置、五个物理引擎均出现 reversibility cliff；reset-free 方法进入不可恢复状态后被永久吸收，而 episodic 方法保持较稳定学习。几何匹配对照支持失败由不可逆性而非障碍复杂度导致。可恢复性可被准确预测，但主动恢复主要只在 agent 尚能绕开陷阱时成功。

## 证据质量与局限

- 优点：多引擎、连续可逆性轴、几何匹配因果对照、环境 oracle 标签。
- 局限：集中于机器人/物理模拟；摘要未给统一绝对准确率；oracle 在开放 Web/代码 Agent 上难以直接获得；预测可恢复不等于能够恢复。

## 最接近的相关工作

Persistent Teacher Anchoring 处理副作用前承诺，BLINDSPOT 区分安全执行与过度拒绝，SAGE 在高熵状态调用 teacher。本文补充可恢复性真值与不可逆 cliff。

## 如何复用或推进 LLM-as-a-Verifier

为工具 Agent 定义近似 reset oracle：快照可回滚性、外部副作用、权限升级、数据删除、未提交事务等。训练 verifier 输出成功概率、失败概率、可恢复概率及其不确定性；生成式 critique 必须指出导致可恢复性下降的具体动作。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把 recoverability distribution 纳入分数；不可逆动作前只接受真值锚定的 teacher 方向。
- **A/B/T**：同前缀构造可恢复 A、不可恢复 B、oracle 不确定 T。
- **真值门控**：能快照/重放时由环境 oracle 定方向，Judge 不得覆盖。
- **critique states**：记录“恢复条件、剩余回滚路径、不可逆副作用”。
- **高熵探索**：优先保留多条可恢复分支；对不可逆分支隔离执行。
- **sealed eval**：隐藏 ρ、陷阱位置与恢复判定实现，防止 policy/verifier 针对固定 oracle 共适应。