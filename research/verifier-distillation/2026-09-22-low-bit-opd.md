# Train Where the Quantized Model Goes: On-Policy Distillation for Low-Bit Reasoning

- **作者**：Yuanteng Chen, Zhilei Liu, Peisong Wang, Yuantian Shao, Chuangyi Li, Weining Wang, Shuang Qiu, Gang Li, Jing Liu, Jian Cheng
- **首次公开日期**：2026-09-22
- **版本日期**：2026-09-22（v1）
- **原始论文**：https://arxiv.org/abs/2609.26708
- **Canonical URL**：https://arxiv.org/abs/2609.26708
- **DOI**：10.48550/arXiv.2609.26708（arXiv DataCite，待注册）
- **代码**：https://github.com/MingZwhy/QAOPD
- **arXiv ID**：2609.26708

## 一句话结论

【论文原文】极低比特模型的长推理失败主要来自量化偏差在自身前缀上累积；在部署用 quantized forward path 上采样，再结合 frozen BF16 teacher 的 reverse-KL 与数学/代码执行 verifier reward，可将 MATH-500 的 BF16 性能保留率从约 35% 提升到 70%。

## 真正新增的内容

【论文原文】论文把 OPD 明确用于量化后模型，并要求 rollout 真正经过部署时的低比特 forward path，使 teacher 监督覆盖量化诱发的错误前缀，而不是继续在固定语料前缀上做 QAD。训练目标把逐 token reverse-KL 与 group-relative verified outcome advantage 相加，分别负责局部轨迹纠偏和终局正确性。

【分析推断】这是“student 真正会到达的状态 + 程序真值门控 teacher”的干净基线，也证明 OPD 的价值不只是知识迁移，而是恢复被部署扰动破坏的 trajectory control。

## 核心方法

1. 先用 quantization-aware distillation 恢复短任务能力，得到可采样的低比特初始 policy。
2. student 通过实际 quantized forward path 生成多条 completion；frozen BF16 teacher 在这些 student prefix 上评分。
3. 使用 student-sampled reverse KL，惩罚 student 高概率但 teacher 低概率的 continuation。
4. 数学以最终答案正确性、代码以测试执行结果作为 verifier reward，形成同 prompt 组内 advantage。
5. 总损失为 verified policy-gradient 项加 β=1 的 token-level reverse-KL；β 在全部实验中不按设置调参。

## 关键实验结果

- 四个模型、2.79/1.88 effective bits 上，MATH-500 的平均 BF16 retention 从 35% 升至 70%，HumanEval 从 66% 升至 91%，短答案能力保持。
- Qwen3-0.6B W2.79 的 MATH-500 loop rate 从 70% 降到 17%，budget exhaustion 从 95% 降到 53%，准确率从 10.4% 升到 24.2%（BF16 为 27.2%）。
- GSM8K loop rate 从 30% 降到 2%，budget exhaustion 从 32% 降到 5%，与 BF16 行为相当。
- Qwen3-4B W1.88 的 OPD 阶段 260 steps、57 GPU-hours，对比 QAD 6,400 steps、820 GPU-hours；在仍能提升的设置中，每千步收益最高可达继续 QAD 的 42 倍。
- 即使将 matched-budget QAD 延长到 3×，四个数学设置仍比 OPD 低 8.9–18.1 个点。

## 证据质量与局限

【论文原文】实验跨四个模型、两种极低比特宽度、数学与代码任务，并有 matched/延长 QAD 对照和行为指标，证据较完整。局限是 teacher 始终为对应 BF16 模型，任务主要是可验证的单轮推理，不是带外部环境副作用的多轮 Agent；β 固定但未充分探索 teacher 错误或 reward 冲突；checkpoint 仍按当前阶段 validation metric 选择。

【分析推断】成功不能直接外推到 verifier 自身蒸馏或开放式长轨迹；teacher 与执行 reward 同时共适应时仍可能把错误方向固化，需独立 sealed eval。

## 最接近的相关工作

最接近标准 OPD/SDPO、QAD、Unified Per-Token OPD Gating、γOPD 与 RA-OPD。区别在于 student rollout 必须经过部署低比特计算路径，并把 reverse-KL 与程序化终局 verifier reward联合，而非只在离线前缀上匹配 logits。

## 如何复用或推进 LLM-as-a-Verifier

- 将 quantization noise 类比为 Agent 环境/工具扰动：verifier student 必须在自身实际观测与 critique state 上训练。
- 用 hard oracle 决定 advantage 方向，teacher score distribution 决定局部形状和幅度。
- 对 A/B/T 分支，执行测试相同但 teacher 分歧大时保留 T；不要用 reverse-KL 强迫单一路径。
- 训练一个低比特 verifier student 时同时监控 loop、budget exhaustion、置信熵和执行正确率，避免只看静态 Judge accuracy。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】建议新增“部署路径一致性”实验：student verifier/Agent 用实际量化、工具解析器和上下文截断生成状态，teacher 只在这些状态上给 score/critique；程序/环境 truth 提供 group-relative gate。与 teacher-forced verifier distillation 做等预算对照，并按轨迹长度分层。高熵分叉保留多 completion，只有执行真值显现后再蒸馏；最终在冻结未见任务、独立 harness 与未参与 checkpoint 选择的 sealed set 上验收。