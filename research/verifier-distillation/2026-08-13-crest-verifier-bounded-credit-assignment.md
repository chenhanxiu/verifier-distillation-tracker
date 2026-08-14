# CrEST：Verifier-Bounded Credit Assignment for Multi-Turn Multi-step LLM Agents

## 基本信息

- **论文标题**：Teach the Magnitude, Not the Direction: Verifier-Bounded Credit Assignment for Multi-Turn Multi-step LLM Agents
- **作者**：Zechuan Wang、Siyuan Lu、Hongxuan Zhang、Linjian Mo、Chenyi Zhuang、Leilei Gan
- **首次公开日期**：2026-08-13
- **版本日期**：2026-08-13（arXiv v1）
- **arXiv ID**：2608.13179
- **DOI**：10.48550/arXiv.2608.13179
- **原始论文**：https://arxiv.org/abs/2608.13179
- **代码**：未发现公开链接

## 一句话结论

CrEST 将 privileged self-teacher 限制为“调节 verifier 决定的 policy-gradient 幅度，而不改变方向”，并用 turn-segmented verified advantage 与 entropy gate 细化多轮 Agent 信用分配，目标是在获得密集 token 信号的同时保留 RLVR 的 verifier-bounded 性质。

## 真正新增的内容

**论文原文结论**：多轮工具 Agent 的轨迹级 reward 会把不同 turn 的结果混为一个优势，而直接 OPD 又可能被 teacher ceiling 限制或发生梯度集中坍缩。CrEST 提出层级信用分配：

- turn 间：按 turn 分段的 verified advantage 缓解长轨迹中的信号稀释；
- turn 内：privileged self-teacher 结合 entropy gate 只调制 token 更新幅度；
- 最终方向仍由 verifier-grounded RL advantage 决定。

“Teach the magnitude, not the direction”是其与把 teacher KL 当作独立 actor loss 的关键区别。

## 核心方法

1. 将多轮、多步 Agent trajectory 按 turn/segment 拆分，并从可验证结果构造分段优势，减少单个 terminal reward 对所有 token 的无差别广播。
2. privileged self-teacher 在 student 实际访问的 prefix 上产生密集 token-level 信息。
3. teacher 信号不直接指定正负更新方向，而以有界权重调节由 verified advantage 决定的梯度大小。
4. entropy gate 在 turn 内选择或缩放 teacher 调制，抑制不可靠或过度集中的 dense signal。
5. 由此保留“性能上限由 verifier/reward 定义”这一设计意图，同时改善长轨迹 credit assignment。

## 关键实验结果

**论文摘要可确认的结果**：

- 在 BFCL V3 与 WildToolBench 上、两个模型规模中，CrEST 一致超过 RL 与 distillation baseline。
- 最大收益出现在长轨迹和严格 session-level 指标上，符合其针对 inter-turn dilution 的设计动机。

**证据边界**：当前公开摘要没有列出各表的具体分数、方差、显著性或训练预算，因此不能据此给出精确增益；在完整表格可稳定核对前，本记录不把“一致优于”升级为定量结论。

## 证据质量与局限

- **证据质量：中等偏低（当前可核对材料）。** 主题与方法高度直接，且覆盖两个 Agent benchmark 和两个规模，但可访问公开信息缺少完整数字与消融细节，代码也未公开。
- 摘要没有说明 turn-level verifier 如何处理部分可观测、错误恢复、工具副作用和延迟奖励；这些因素会影响“分段真值”是否可靠。
- entropy gate 可能把策略探索所需的高熵与 teacher 不确定性混为一谈。
- “verifier-bounded ceiling”依赖 verifier 本身正确；若 verifier 可被 reward hacking，限制 teacher 方向并不能修复错误目标。
- 未见独立 sealed evaluator、跨环境泛化或超长 horizon 的专门共适应审计。

## 最接近的相关工作

最接近 RLVR 的细粒度信用分配、SDPO/OPSD 的反馈条件 self-teacher、Skill-SD/SDAR 等 Agent 自蒸馏，以及“distillation 只做 bounded credit weighting”的 SGCD/H²SD 一类方法。CrEST 的差异在于同时显式处理 turn 间分段优势与 turn 内 entropy-gated 幅度调制。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：

- 将 verifier 从单一 terminal scorer 扩展为 turn-level distributional verifier，但每个 turn 分数必须受环境状态变化、程序执行或可检查约束门控。
- teacher verifier 可输出 A/B/T 与序数评分分布；这些分布用于估计 token/turn 的权重与不确定性，而最终更新方向由 sealed 或程序化 outcome 决定。
- “只教幅度”适合蒸馏高容量 generative verifier 的 critique：critique 决定关注哪些 state/action，不直接覆盖真值的正负方向。
- 需要显式校准 entropy gate：高 entropy 可能表示证据不足，也可能表示真实多解；可结合反事实 recoverability 或 sibling rollout 结果区分。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：将 teacher ordinal distribution 转为有界 magnitude coefficient，student policy/verifier 的符号仍由环境真值或程序检查确定；这是避免 evaluator 共适应的强基线。
- **pairwise A/B/T 与序数评分**：先由 verifier 给 turn/segment 级分布，再聚合到轨迹 A/B/T；保留 tie 概率和方差，不强行把所有 turn 压成标量。
- **真值门控 teacher 信号**：只有可验证 turn 才允许 teacher 调制；不可验证 turn 的系数应有上限并记录来源，防止自然语言 critique 冒充真值。
- **student-generated critique states**：teacher 可在 student 自己生成的 critique prefix 上指出高价值 token/turn，但不提供更新方向；这样利用 on-policy critique 又不让 teacher 接管目标。
- **高熵分叉保留探索**：对高 entropy 且尚无环境证据的分叉设置“不过度缩小”的下限，或仅延迟蒸馏；对已验证的高熵成功分叉保留多个策略模式。
- **sealed eval**：训练用 verifier、teacher self-verifier 与最终 sealed evaluator 三者分离；专门报告长轨迹 session success、recoverability、reward-hacking 率及 evaluator disagreement，而不仅是同一 verifier 下的训练回报。
