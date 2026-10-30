# MTA-OPSD：每个 Token 选择自己的教师

## 基本信息

- **论文标题**：Every Token Needs Its Own Teacher: Multi-teacher Adaptive On-policy Self-distillation
- **作者**：Yifu Luo, Chuang Ma, Zeyu Chen, Enkelejda Kasneci, Qi Chen, Gjergji Kasneci
- **首次公开日期**：2026-10-29
- **版本日期**：2026-10-29（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.40574
- **DOI**：https://doi.org/10.48550/arXiv.2610.40574
- **代码**：https://github.com/xingzhejun/MTA-OPSD

## 一句话结论

固定 teacher 或逐 response 选择 teacher 都太粗：MTA-OPSD 在同一学生 response 内按 token 从多教师池选择监督者，直接把“teacher reliability 是状态依赖的”落实成训练算法。

## 真正新增的内容

**论文原文结论**：

1. 通过 teacher-intervention pilot study 观察到，同一 response 内的教师偏好会逐 token 改变。
2. 提出首个 token-level adaptive OPSD：候选教师构成池，每个 token 通过多数投票或 KL 选择偏好的教师。
3. 在 Qwen3 数学推理上持续优于固定教师 OPSD，较 base model 的平均增益最高为 +5.9。

**分析推断**：

- 对 verifier 蒸馏，这相当于把“哪个 verifier 在当前状态可信”从 trajectory-level routing 下放到 step/token-level routing。
- 多数票并不等于真值；若教师同源，其相关错误会虚增共识，因此应该用环境 oracle 和跨家族误差相关性校准选择器。

## 核心方法

1. 用不同 privileged-reference 暴露方式构造候选 teacher pool。
2. 对学生当前 token，比较各教师分布；以多数偏好或 KL 规则选择局部 teacher。
3. 只把所选教师的分布用于该 token 的 OPSD 更新。
4. 公开实现包含 Qwen3-1.7B/4B/8B 训练脚本，并复用 RLCSD 的训练/评测数据。

## 关键实验结果

**论文报告**：在 Qwen3 系列数学推理任务上，MTA-OPSD 一致优于已有 OPSD 方法，较 base model 平均最高提升 5.9 个百分点。公开仓库给出主要训练配置、验证脚本和 MIT 许可证。

## 证据质量与局限

- **优点**：问题设定直接、算法粒度与发现一致；有公开代码和多尺寸模型。
- **局限**：实验集中在数学推理，尚未验证长轨迹工具状态、序数 reward distribution 或真实环境副作用。
- 多教师选择本身可能过拟合同一 benchmark；摘要未给出选择器额外计算成本和跨域校准。
- 多数投票在高度相关的 teacher panel 上会高估独立证据量。

## 最接近的相关工作

- **VG-OPD / Lightning Weave**：多专家路由与能力位移组合，但 MTA-OPSD 的选择粒度更细。
- **OnPoKD / Unified Per-Token OPD Gating**：按可靠性或不确定性混合目标。
- **Agreement Overstates Evidence / Judge Panel Distribution Recovery**：提醒多 Judge 共识需要按误差相关性折算。

## 如何复用或推进 LLM-as-a-Verifier

把教师池改为异构 verifier 池：环境测试、规则检查器、生成式 critic、过程 reward model 和安全 verifier。每个 Agent step 不输出单一分数，而输出来源条件化的序数分布；路由器优先选择能给出可重放证据的通道，相关 Judge 的票数按有效独立样本量折算。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：比较固定 verifier、trajectory-level router 与 step-level router 三个基线。
- **pairwise A/B/T 与序数分布**：教师池不直接压成均值；保留各通道的 A/B/T 与等级分布，再学习可靠性加权。
- **程序化/环境真值门控**：硬 oracle 可否决软 Judge；无硬真值时才让多教师路由决定蒸馏幅度。
- **student-generated critique states**：每个 critique state 记录所选教师、备选教师及分歧，便于离线审计。
- **高熵分叉与探索**：若教师间分歧高，降低 KL 强度并保留多分支，而非强选单一教师。
- **sealed eval**：用未参与路由器训练的 verifier 家族和任务快照评估，检查路由器是否只学会识别 benchmark 风格。