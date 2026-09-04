# Interface-Induced Trajectory Censoring

## 基本信息

- **作者**：Wenbo Wang
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **arXiv**：2609.03966
- **原始论文**：https://arxiv.org/abs/2609.03966
- **代码/数据/预注册**：https://github.com/nebula-1999/Interface-Induced-Trajectory-Censoring
- **DOI**：https://doi.org/10.48550/arXiv.2609.03966

## 一句话结论

Agent 轨迹可在模型已生成合法工具调用后被 chat template × parser 接口静默截断，使观测工具调用率从接近 1 变为 0，并把错误的“无动作”状态送进训练与评测。

## 真正新增的内容

**论文原文结论**：通过只替换 serving adapter、保持权重、样本、解码和 seed 不变，将轨迹缺失精确定位为 template 与 parser 的交互效应，并给出 98 行 preflight checker。

**分析推断**：对 Agent verifier 蒸馏，轨迹可观测性本身必须先被验证。否则 teacher 会在被截断的伪状态上学习“模型未调用工具”，score/critique 蒸馏再精细也只是在复制测量链路故障。

## 核心方法

- 在 BFCL v4 上固定模型与实验条件，仅改变 serving adapter。
- 用 chat template × parser 的 2×2 析因实验定位交互。
- 在 tau-bench 115 个交互任务和 Qwen2.5-Coder 21× 参数规模跨度上复现。
- 进入 verl AgentLoop 检查生成、解析、执行、观察返回的完整漏斗。
- 以独立人工 adjudication 校准“模型实际发出合法调用”的估计。

## 关键实验结果

- BFCL v4：同一模型仅因 adapter 不同得分可为 **0.00** 或 **0.96/0.19**。
- 两个主效应均为 0，差异全部来自 template × parser 交互。
- tau-bench：server-parsed calls 从 **0→636**，至少执行一次工具的任务从 **0→103/115**。
- Qwen2.5-Coder 从小到 32B，server 均解析 0/100，但 32B 实际合法调用达 80/100，人工校准后约 72。
- verl AgentLoop 7B：115 个生成中 45 个含完整调用，接受/执行/返回 observation 均为 0。
- 修复 adapter 后 pass rate 53→62，但结果提升未显著，说明恢复机制不等于立即恢复任务效果。

## 证据质量与局限

- **质量：高。** 有预注册、控制实验、多个模型规模、两个公开基准和训练环路复现。
- 主要针对工具调用协议，不能直接外推到纯文本 verifier。
- 修复接口后的最终成功率增益未显著，论文证明的是测量与训练信号污染，不是完整性能修复。
- 不同生产栈需运行自己的契约测试，不能假定同类 parser 必然同样失效。

## 最接近的相关工作

与 ToolGate、Thinkingbox、Harness-of-Harness、CordisBench 和 LLM-as-a-Judge Is Not an Oracle 的确定性验收思路最接近；其独特贡献是把“轨迹在进入 verifier 前是否完整”作为可实验定位的测量问题。

## 如何复用或推进 LLM-as-a-Verifier

- 在 verifier 前增加 raw generation → parse → execute → observation 的逐层 receipt。
- 对每个步骤输出 observed / censored / invalid / executed 四态，而非把缺失统一标为失败。
- 训练 A/B/T 时只比较可观测性状态一致的分支；接口不一致应标为不可比。
- student critique 必须可引用原始消息字节和执行 receipt，避免对被截断日志编造原因。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：对 censored state 将 loss mask 掉，不能按 0 分或 teacher rejection 训练。
- **A/B/T 与序数分布**：增加 INCONCLUSIVE/CENSORED 类；A/B 解析链路不同则不生成偏好标签。
- **真值门控**：执行器 receipt 与环境终态优先于 server 统计字段。
- **critique states**：加入“接口契约不匹配”专门 critique 类型，与策略错误分离。
- **高熵探索**：解析失败不等于策略无探索；统计原始生成中的候选调用。
- **sealed eval**：冻结 template/parser 版本并运行 preflight；把接口栈哈希纳入评测快照。