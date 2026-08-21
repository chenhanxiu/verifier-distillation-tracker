# SafeBranch: Branch-Pair Safety Alignment for Embodied Agents

## 基本信息

- **作者**：Hyunse Lee、Jiwoo Jeong、Haneul Lee、Kyochul Jang、Youngjae Yu、Woojin Lee
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.19729
- **DOI**：10.48550/arXiv.2608.19729
- **原始论文**：https://arxiv.org/abs/2608.19729
- **代码**：截至该版本未发现公开代码

## 一句话结论

从 Agent 自己的不安全轨迹回滚到同一决策状态，再生成只在安全关键动作上不同的成对分支，比对整条任意安全/不安全轨迹更能隔离安全因果信号并保留任务完成能力。

## 真正新增的内容

**论文原文结论**：SafeBranch 用环境 rollback 从 actor 自身失败状态构造共享历史前缀的 safe/unsafe branch pair，经 critic 与任务成功过滤后用 BranchPO 做偏好优化；这种“同锚点、单关键分叉”监督在分布外和跨模拟器安全上明显优于轨迹 SFT、任意 pairwise preference 和推理时 critic。

**分析推断**：这是 Agent verifier × OPD 的高质量 A/B 构造原型。若加入“两个分支均可接受但风险/恢复性不同”的 T 桶和序数概率，就能从安全偏好扩展为一般长轨迹的局部可恢复性 verifier distillation。

## 核心方法

1. 运行当前 actor，定位导致安全违反的轨迹和安全关键决策点。
2. 将环境回滚到该状态，保留相同历史与任务上下文。
3. 由生成/critic 流程提出安全替代动作并继续执行，形成只在锚点处分叉的 branch pair。
4. 通过安全 Judge、任务成功和 human-usability 相关过滤，剔除虽然“安全”但停止任务、或差异混杂的 pair。
5. 使用 BranchPO 对共享前缀下的安全/不安全分支做偏好优化；部署时不再调用 critic。

## 关键实验结果

**论文原文结果**：

- 在 IS-Bench 上，BranchPO 将 safe success rate 从未训练基线的 0.031 提高到 0.281，safety recall 从 0.273 提高到 0.467。
- 在 ObjectShift 和 TaskShift 的 OOD 测试中，safety recall 分别提升 34.6 和 50.0 个百分点；推理时 critic 在 OOD 上没有表现出相同迁移。
- 跨模拟器 SafetyALFRED 上，总体 hazard accuracy 从 0.274 提升到 0.438；Property Damage 和 Appliance Misuse 分别提高 39.4、15.4 个百分点。
- 过滤消融显示只有最终同时保证 pair 质量与任务成功的分支对，才带来明显的安全率、safe success 和 recall 提升。

## 证据质量与局限

- **证据质量：中高。** 包含 in-distribution、两种 OOD、跨模拟器、SFT/偏好/critic 基线及数据过滤消融。
- 训练期仍依赖 critic，成本只是从部署期转移到数据构造期；critic 偏差可能进入 actor。
- 必须能精确 rollback；真实物理环境可能需要昂贵人工复位或不可靠世界模型。
- 主要验证交互安全，不代表同样机制在一般业务、推理或开放式 Agent 目标上成立。
- pair 仍是二元偏好，未直接建模 tie、恢复概率或评分分布；sealed evaluator 的独立性也未成为核心实验变量。

## 最接近的相关工作

最接近 DPO/偏好优化、DAgger 式从当前策略失败状态收集数据、counterfactual branch comparison、interactive safety 与推理时 safety critic。相较任意正负轨迹，本工作通过共享状态锚点减少任务内容和历史差异造成的混杂。

## 如何复用或推进 LLM-as-a-Verifier

- 用程序化环境约束先定位违规，再让 LLM critic 解释“为何危险”并提出替代分支。
- 训练本地轻量 verifier 对同状态候选动作给出 A/B/T 和风险序数分布，而非单一安全标签。
- 对安全分支的后续可完成性进行真实 rollout 验证，防止 verifier 只奖励停滞或拒绝。
- 将 critic 生成的解释作为 student-generated critique state，再用环境结果过滤自洽但错误的解释。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：在同一 state prefix 上蒸馏安全/任务成功联合 score，比整轨迹 likelihood 更接近局部因果 credit。
- **A/B/T 与序数分布**：A=安全且完成，B=不安全，T=两者同样安全或安全但无法完成；进一步用多次续跑估计恢复概率分布。
- **程序化真值门控**：环境安全规则和最终成功必须共同门控，避免“停止行动”成为虚假安全 teacher。
- **student-generated critique states**：学生先指出风险点，teacher/环境只在该分叉生成反事实续跑，可降低无关 teacher token。
- **高熵探索**：只修正已证实危险的局部分支，保留其他可行探索；不应把与 teacher 不同等同于不安全。
- **sealed eval**：用未参与 pair 生成的安全场景、规则和独立 evaluator 测试，防止 actor 学会 critic/过滤器的表面模式。