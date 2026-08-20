# SPADE：自适应合成可执行环境中的 Self-Play

## 基本信息

- **论文标题**：SPADE: Self-Play in Adaptive Synthetic Executable Environments
- **作者**：Bo Liu、Simon Yu、Yiding Jiang、Ao Qu、Andrew Zhao、Zichen Liu、Junsu Kim、Zijian Zhou、Seungone Kim、Tongzheng Ren、Mickel Liu、Hanfei Yu、Zhaorun Chen、Weiyan Shi、Paul Pu Liang、Luke Zettlemoyer、Yejin Choi、Natasha Jaques
- **首次公开日期**：2026-08-19
- **版本日期**：2026-08-19（v1）
- **arXiv ID**：2608.19197
- **DOI**：10.48550/arXiv.2608.19197
- **论文**：https://arxiv.org/abs/2608.19197
- **代码**：https://github.com/spade-rl/spade

## 一句话结论

SPADE 让同一个 LLM 同时充当可执行环境设计者与解题 Agent，用“有/无 privileged hint 的环境回报差”训练设计者持续生成位于 Agent 能力边界的长时程任务，为程序化真值门控和难度自适应 verifier 数据生成提供了完整闭环。

## 真正新增的内容

### 论文原文结论

Environment Designer 生成完整 Python Gym 风格 reset()/step() 环境、reward function 与 privileged hint；Reasoning Agent 分别在有提示和无提示条件下执行。两者回报差构成 hint-based regret，使设计者偏好“提示可解、无提示尚难”的环境。语法与执行检查通过后环境才进入训练池。

### 分析推断

SPADE 不是 verifier distillation，但它可自动生成 verifier-grounded on-policy states。最有价值的是 teacher 信号同时拥有程序化环境真值和 privileged hint 对照，可用于训练 score-level Agent verifier；风险是 designer、agent 与 reward code 共同演化形成封闭生态。

## 核心方法

1. 单模型使用不同 system prompt 扮演 Environment Designer 与 Reasoning Agent。
2. Designer 基于预训练语料与环境 memory 生成 stateful executable MDP、验证逻辑和 hint。
3. Agent 对同一环境分别无 hint / 有 hint rollout；任务回报训练 Agent，截断为非负的 hint regret 训练 Designer。
4. 两个角色用 GRPO 联合更新；生成环境须通过语法、运行时和成功条件可达性检查。
5. 同一接口覆盖单轮推理、游戏与多轮 tool calling。

## 关键实验结果

### 论文原文

- 在 Qwen3 4B、8B、30B-A3B 上测试游戏与工具环境。
- 30B-A3B 游戏设置八项平均 58.3，相对 base +8.1、相对最强 fixed-environment baseline +5.3。
- 工具设置 30B-A3B：BFCL-v4 multi-turn +5.7、τ²-bench +3.6、ACEBench-Agent +13.9。
- 增益随规模上升：4B +5.2、8B +5.7、30B-A3B +8.1；matched fixed-env GRPO 约 +1.2。
- 代码、训练脚本、环境、checkpoints 与评测配置公开。

## 证据质量与局限

- **质量**：多尺度、多领域、固定环境和 frozen frontier designer 对照；可执行验证；开源完整度较高。
- **局限（论文原文）**：环境复杂度受 designer 模型与 context 限制；优化器仍为人工设计 GRPO；hint regret 无最优课程保证；评估仍是固定任务，而非开放式增长。
- **额外局限**：designer 与 agent 共享参数，reward code 也由模型生成，存在共适应和 reward loophole；部分外部 synthetic-system 对比的预算与协议不同；work in progress。

## 最接近的相关工作

PAIRED、自适应 curriculum、RLVR、Agent World/EnvScaler、WebGrader、可执行 task synthesis，以及 privileged-information/self-distillation。

## 如何推进 LLM-as-a-Verifier

- 保存同环境有/无 hint 的 sibling rollouts，用程序 reward 差训练“当前状态下 hint 的边际价值” verifier。
- 将环境 reward 拆成多项 executable checks，形成序数进度分布而非仅终局 0/1。
- 用独立 LLM Judge 审计 reward code 的覆盖与可钻漏洞，但不让该 Judge参与 policy 更新。

## 对 Agent verifier × OPD 路线的具体影响

以下为**分析推断**：

- **Score-level OPD**：以 `return_with_hint-return_without_hint` 作为 privileged teacher 的轨迹级残差，再分配到 student action states。
- **A/B/T**：同一环境的有/无 hint、不同恢复路径天然形成配对；二者回报相同则保留 T。
- **真值门控**：先通过 executable state checks；LLM teacher 仅补充分解、critique 和密集指导。
- **Critique states**：hint 可替换为 student critique；比较 critique 前后回报，筛选真正有用的 critique。
- **高熵探索**：环境设计应奖励可学习区间而非固定最优轨迹，保留多种可执行成功路径。
- **Sealed eval**：Designer、memory、reward code 和训练 Agent 必须与 sealed 环境生成器及 evaluator 分离；报告跨生成器迁移，避免一套模型同时出题、判题和答题。