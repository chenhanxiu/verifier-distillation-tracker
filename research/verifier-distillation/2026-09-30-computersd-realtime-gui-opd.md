# ComputerSD: Online Self-Distillation from Real-Time Feedback for Computer-Use Agents

- **作者**：Yong Du, Tongbo Chen, Zhengxi Lu, Yizhou Liu, Bofan Chen, Tao Jiang, Wenhao Xu, Yongliang Shen
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40253
- **代码**：未发现公开代码链接

## 一句话结论

ComputerSD 将每次 GUI 执行后的真实状态变化转成 privileged guidance，并用 step value 调节 OPSD，在 OSWorld-Verified 上比 outcome-only GRPO 高 1.9–4.1 点。

## 真正新增的内容

【论文原文】直接在 CUA 上使用固定 guidance 会与当前 student 状态错位，且 teacher 概率位移可能和步骤正确性冲突。ComputerSD 用实时 GUI transition 生成 guidance 与 step-level value，再以 value 调节 OPSD 信号。

【分析推断】这是“环境观测定可信度、teacher 分布给稠密方向”的在线 Agent verifier 蒸馏实例。

## 核心方法

每次动作执行后，GUI analyzer 根据实际 transition 生成 privileged guidance 和步骤价值；异步联合优化 token-level OPSD 与 trajectory-level GRPO。

## 关键实验结果

【论文原文】OSWorld-Verified 上，相对 outcome-only GRPO，Qwen3-VL-8B-Thinking 提高 1.9 点，EvoCUA-8B 提高 4.1 点；OOD 评测也支持泛化性。

## 证据质量与局限

直接在可执行 GUI 环境验证且含 OOD 测试；但提升幅度中等，GUI analyzer 是额外学习组件，其误差、校准和与 policy 的共适应仍需审计。

## 最接近的相关工作

GC-OPD、OnPoKD、Ground-truth-as-code、SCA、Persistent Teacher Anchoring。

## 如何复用或推进 LLM-as-a-Verifier

将 GUI analyzer 改为分布式 verifier：分别预测动作正确性、状态推进、风险和可恢复性，并记录屏幕/DOM 状态证据。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：step value 可直接作为逐动作 OPD 强度。
- **A/B/T 与序数分布**：对同一 GUI state 的候选动作输出序数后验；观测不足时为 T。
- **硬真值门控**：真实 GUI transition 和任务断言优先覆盖 analyzer 判断。
- **student-generated critique states**：critique 必须引用执行后的状态差分。
- **高熵分叉**：对高熵动作保留多个可执行候选，以真实 transition 比较。
- **sealed eval**：冻结 GUI 任务、初始状态、analyzer 与 grader，避免在线闭环污染。
