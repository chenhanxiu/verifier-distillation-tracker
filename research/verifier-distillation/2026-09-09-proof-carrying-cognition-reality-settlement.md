# Proof-Carrying Cognition：用现实结算奖励弥合验证缺口

- **论文标题**：Proof-Carrying Cognition: Closing the Verification Gap with Reality-Settled Reward
- **作者**：Eshwar Reddy M, Sourav Karmakar
- **首次公开日期**：2026-09-09
- **版本日期**：2026-09-09（v1）
- **原始论文**：https://arxiv.org/abs/2609.09776
- **代码**：截至本次记录未发现公开代码

## 一句话结论

论文把 verifier 的关键指标从静态准确率改为优化压力下的 soundness，并用少量 on-policy 现实结算持续重拟合 reward model，实证表明这能显著抑制 Goodhart 漂移。

## 真正新增的内容

**论文原文结论**：提出 Soundness-under-Pressure（Snd@N）、typed probabilistic claims、严格 proper scoring 与 reality settlement；在程序合成、真实代码/LLM Judge 及 GRPO 实验中比较冻结 proxy 与执行真值锚定。作者还预注册、报告并修正了两项失败的定量预测。

**分析推断**：这是 sealed eval 与程序真值门控 OPD 的高价值理论/实验框架：硬真值不必覆盖全部步骤，但必须持续抽样结算 student 当前最容易利用 verifier 的 on-policy 尾部。

## 核心方法

Reasoner 输出带类型和概率的可结算 claim；world/reward model 给密集价格，但唯一学习目标是预测未来持出现实；部分 claim 被真实执行或事后事件结算，并以 proper scoring 更新。Snd@N 衡量 proxy 从 N 个样本中选择的候选相对于 gold 最优选择能保留多少真实价值。

## 关键实验结果

浅层 learned verifier 的 Snd@N 在小型程序环境从 N=1 的 1.00 降至 N=2048 的 0.13；预注册扩展实验在 N=4096 从 0.94 降至 0.32。现实锚定把约 0.27 的 hacking gap 压到接近 0，on-policy settlement 比随机标注约高 10 倍标签效率。真实 MBPP/HumanEval 中弱 Judge 的 Snd@N 显著下降；结算模型将定价误差降低 59%。真实 GRPO 下冻结 RM 的执行奖励下降 90%，用 10% 结算流重拟合后执行奖励约为冻结组 6 倍。

## 证据质量与局限

优点是预注册、主动报告反证、同时有合成与真实模型实验。局限也很实质：主实验仍是短程序与小模型代理；Gaussian 闭式外推被扩展实验否定并修正；强 verifier 未在所有区域崩溃；drift alarm 首次测试失败；现实锚定尚未覆盖真正长时程 Agent 与端到端学习型对手。

## 最接近的相关工作

RLVR、reward overoptimization/Goodhart、过程奖励模型、可执行 verifier、RecurSE、Cheap Verifiers Large Blind Spots、Harness-of-Harness 与 S3Gym 最接近。区别是把“优化压力曲线”和现实结算流组合成统一训练与评测框架。

## 如何复用或推进 LLM-as-a-Verifier

训练轻量 verifier 输出序数/概率 claim 与校准区间；在 student on-policy 高分、高不确定或高影响轨迹上调用环境真值结算，周期性重拟合。必须分别记录 proxy score、settled reward 与 Snd@N 曲线，而非只看 judge agreement。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：硬结算决定梯度符号，蒸馏 verifier 分布只定幅度。
- **A/B/T 与序数分布**：同状态候选若结算差异落在区间内标 tie，并用 proper scoring 蒸馏完整概率。
- **真值门控**：优先结算 student 当前最能放大 proxy 的尾部，而非随机抽样。
- **critique states**：critique 应拆成可执行或未来可结算的 typed claims。
- **高熵探索**：探索不因 proxy 高分而过早剪枝；用结算后的覆盖率和 Snd@N 控制压力。
- **sealed eval**：冻结独立 gold 执行器、延迟揭示测试集和 evaluator 快照；漂移报警只能作诊断，不能替代 sealed gold。
