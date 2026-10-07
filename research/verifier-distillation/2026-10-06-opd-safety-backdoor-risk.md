# Does On-Policy Distillation for Safety Pose Backdoor Risks?

- 作者：Jian Luo、Kehan Qi、Qingqiao Hu、Meilong Xu、Jiacheng Qiu、Weimin Lyu、Jiawei Zhou、Chao Chen
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.07654
- Canonical URL：https://arxiv.org/abs/2610.07654
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】安全 OPD 会把安全外观 teacher 的隐藏后门传给干净 student：仅 3% 污染率可使攻击成功率最高达 70%，而 top-k KL 与更多训练轮次会加速传播。

## 真正新增的内容

【论文原文】论文把 teacher 可信假设改造成可测威胁模型，识别出训练轮次和 top-k KL 两个风险放大器，并提出裁剪 KL reward 的 Lazy Defense 延缓低污染率下的后门学习。

## 核心方法

【论文原文】以安全对齐但带触发器后门的 teacher 蒸馏干净 student，控制污染率、训练轮次和 KL 形式；比较 top-k KL 与 sampled-token KL，并通过 reward clipping 限制激进更新。

## 关键实验结果

【论文原文】3% 污染率下 student ASR 最高 70%；仅 10 个污染样本，训练 16 个 epoch 后 ASR 达 67%；top-k KL 在多数设置中比 sampled-token KL 更早诱发触发条件下的有害行为。Lazy Defense 在低污染率下延缓传播，但未被证明彻底消除后门。

## 证据质量与局限

【论文原文】有明确威胁模型与因子消融。【分析推断】结果依赖特定触发器、teacher 和安全任务；“延缓”不是稳健防御，也未覆盖长轨迹中组合触发或环境状态触发。

## 最接近的相关工作

【分析推断】与 IWD 的不变性加权、DiffGate 的 verifier 门控、ImpossibleRubrics 的奖励攻击和一般模型后门研究最接近。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】verifier teacher 在进入 OPD 前应做语义保持扰动、触发器扫描和环境反事实审计；高 KL/高置信样本不能自动获得更大权重，需用真值证书与独立安全 monitor 交叉确认。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：加入污染率×epoch×KL 形式矩阵，并报告 ASR/正常效用。
- 【分析推断】A/B/T：异常高置信偏好先转 T，不直接作为 A/B。
- 【分析推断】真值门控：安全关键方向只能由程序规则或环境证书批准。
- 【分析推断】critique states：扫描 critique 中的触发器依赖和条件化有害建议。
- 【分析推断】高熵分叉：保留 sampled-token/弱更新对照，避免 top-k 快速锁入后门。
- 【分析推断】sealed eval：使用未公开触发器、独立模型族与多轮工具状态进行盲测。