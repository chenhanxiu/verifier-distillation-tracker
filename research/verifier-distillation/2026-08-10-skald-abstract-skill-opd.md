# SKALD：把抽象技能作为特权信号蒸馏进权重

## 基本信息

- **论文标题**：Distill Skills into Weights, Not Prompts: Abstract Skills as Privileged Signals for On-Policy Self-Distillation
- **方法名**：SKALD
- **作者**：Yubo Jiang, Fengying Xie, Zhiguo Jiang, Haopeng Zhang
- **首次公开日期**：2026-08-10
- **当前版本日期**：2026-08-10（v1）
- **arXiv ID**：2608.09826
- **原始论文**：https://arxiv.org/abs/2608.09826
- **代码**：截至记录时未发现与本文对应的公开代码仓库

## 一句话结论

SKALD 让 teacher 额外看到经过答案泄漏过滤的抽象 skill card，而 student 只看原问题并在自身前缀上学习；它尤其改善 RLVR 的全对/全错零方差组，但技能卡的通用提示效应与 Agent 迁移仍需更严格验证。

## 真正新增的内容

**论文原文结论：** RLVR 在一个采样组全部正确或全部错误时缺乏 group-relative 梯度；SKALD 将抽象技能作为仅训练期可见的 teacher 特权信号，通过 on-policy self-distillation 把技能写入 student 权重，推理时不需要技能卡。

**分析推断：** 相比传入完整解答，抽象技能是更紧凑、泄漏风险更低的 teacher side-channel。对 Agent，它可对应从完整成功/失败轨迹抽取的“策略技能”或“修复原则”，再蒸馏给只能访问在线状态的 student verifier/policy。

## 核心方法

1. 同一 Qwen3-Base 模型形成两个视图：student 只输入问题；teacher 额外输入抽象、经过显式答案过滤的 skill card。
2. student 在自己的 on-policy prefixes 上学习，避免仅在 teacher 轨迹上训练造成分布错位；测试时移除 skill card。
3. 使用退火的指数倾斜目标，降低 teacher 偏好但 student 当前概率极低的 token 权重；退火后趋近 teacher 交叉熵/forward-KL 梯度。
4. 通过 verified rollouts 估计 teacher 是否具有正优势；只有正优势时才启用蒸馏门控。
5. 将该监督补充到 RLVR 的零方差组，处理全对或全错导致的 group-relative signal 消失。

## 关键实验结果

**论文报告：**

- 在 MATH500、AMC23、AIME24、AIME25、Minerva 共 872 个数学问题上，以 3 个独立随机种子评估 Qwen3-Base 0.6B/1.7B/4B。
- 相对 GRPO，SKALD 的 avg@8 在 0.6B/1.7B/4B 上分别提升 2.46、4.85、12.01 分。
- 1.7B 上，仅对零方差组蒸馏可恢复完整方法增益的 84.7%；相对 FLOP-matched GRPO 提升 4.06，相对 contextual skill exposure 提升 3.77。
- 论文报告实验中 63%–68% 的 rollout groups 为全对或全错，支持其“补足零方差信号”的动机。
- 泄漏审计中，question-only/empty/random/shuffled/matched/full-solution 的答案恢复率为 2.4%/2.5%/2.6%/3.7%/5.1%/94.2%；200 张卡片未发现完整答案泄漏，标注一致性 κ=0.83。
- 清洗后的技能卡结果为 50.24，原始卡为 50.37，表明显式答案泄漏不是主要解释。
- 但 1.7B shuffled skill card 仍达到 48.83：比 GRPO 高 3.31、比 OPSD 高 0.32，却比匹配 SKALD 低 1.54，说明一部分增益可能来自通用上下文或风格效应，而非严格匹配的技能内容。

## 证据质量与局限

**证据较强处：** 覆盖三个模型规模、五个数学基准、三个随机种子，并报告零方差组、计算量匹配、上下文暴露和泄漏审计消融。

**局限及分析：**

- 证据仍局限于数学推理和 Qwen3-Base，没有长时程 Agent、工具调用或部分可观测环境实验。
- skill card 的生成与过滤可能留下难以完全审计的风格、领域或隐式答案先验；shuffled-card 仍有增益说明匹配技能并非唯一因素。
- 正优势门依赖可验证 rollout；在没有程序化真值的开放 Agent 任务中，门控质量可能成为瓶颈。
- 方法仍以验证后的标量/二元结果为主，没有直接建模序数评分分布或 evaluator 不确定性。
- 截至记录时未发现公开代码，因此复现实证尚待确认。
- 零方差组上的数学收益不能直接证明 Agent 轨迹上的长期信用分配收益。

## 最接近的相关工作

- OPSD：在 student on-policy states 上蒸馏 teacher。
- Privileged-information distillation：teacher 训练时拥有 student 推理时不可见的信息。
- Context distillation：把 prompt/context 中的能力压入模型权重。
- RLVR/GRPO：依赖可验证奖励与组内相对优势。
- H2SD、PAST：分别通过异质 teacher 或完整 student 轨迹改进自蒸馏。

SKALD 的区别是使用“抽象、答案过滤的技能卡”作为 teacher 特权信息，并以优势门控和退火倾斜目标控制蒸馏。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 从成功/失败 Agent 轨迹中抽取不含具体答案的 skill card，例如“先验证权限状态”“调用工具后核对副作用”“遇到冲突证据时继续检索”。
- 让 teacher verifier 同时看到完整轨迹与 skill card，student verifier 只看在线前缀；蒸馏 teacher 的完整序数评分分布。
- 用程序化测试、环境回执或独立执行器估计“skill-conditioned teacher advantage”，只在优势可靠时开启蒸馏。
- 对 student-generated critique states 抽取可复用技能，并使用反事实 rollout 验证该 critique 是否真的提高成功率。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断：**

- **Score-level OPD**：保持 student prefix 不变，只给 teacher 额外 skill；蒸馏失败/部分成功/成功等序数概率，而非只蒸馏 token。
- **Pairwise A/B/T**：比较有无 skill 引导的同状态分支，以环境结果构造 A/B/T；结果不可区分时保留 tie。
- **真值门控**：复用论文的正优势门，但必须由程序化或环境真值驱动，不能由同一个 teacher 自评闭环决定。
- **Critique states**：将学生自生成 critique 压缩成抽象技能，teacher 可见、student 在线不可见，检验其是否能蒸馏为状态评分能力。
- **高熵探索**：退火倾斜可避免强迫 student 学习其支持集外 token；Agent 版还应加熵下限和多策略保留，防止技能模板单一化。
- **Sealed eval**：技能抽取器、训练 verifier 与最终 evaluator 使用不重叠任务和独立评测；否则技能卡可能编码 evaluator 捷径，造成共适应。

建议把 SKALD 加入“特权 critique/skill → score-distribution OPD”实验分支，并将 matched、shuffled、empty skill 与 sealed evaluator 作为必要对照。
