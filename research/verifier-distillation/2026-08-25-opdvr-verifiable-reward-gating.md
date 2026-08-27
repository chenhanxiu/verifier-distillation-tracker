# OPDVR：带可验证奖励的 On-Policy Distillation

## 基本信息

- **论文标题**：On-policy Distillation with Verifiable Reward
- **作者**：Wenze Lin、Jiale Zhao、Xitai Jiang、Songde Rao、Yining Li、Shenzhi Wang、Bingxiang He、Gao Huang
- **首次公开日期**：2026-08-25
- **当前版本日期**：2026-08-25（v1）
- **原始论文**：[arXiv:2608.24696](https://arxiv.org/abs/2608.24696)
- **DOI**：[10.48550/arXiv.2608.24696](https://doi.org/10.48550/arXiv.2608.24696)
- **代码链接**：[LeapLabTHU/OPDVR](https://github.com/LeapLabTHU/OPDVR)

## 一句话结论

OPDVR 用轨迹级可验证真值决定 teacher–student log-ratio 更新的符号，以一个无额外权重超参数的 ReLU 门控阻断“正确轨迹被 teacher 拉低、错误轨迹被 teacher 强化”的冲突梯度，是当前“程序化真值门控 score/token-level OPD”最直接的实现之一。

## 真正新增的内容

**论文原文结论：**

1. 将 sampled-token OPD 的梯度重写为隐式 token reward，指出其符号由 teacher/student 概率比决定，而不保证与轨迹正确性一致。
2. 提出 OPDVR：对 log-ratio 施加条件 ReLU。正确轨迹只保留非负强化，错误轨迹只保留非正惩罚，从而让 verifier 决定优化方向、teacher 分布决定更新幅度。
3. 将同一机制扩展到 group-relative advantage，形成 Group Relative Policy Distillation（GRPD），可嵌入 GRPO 等策略梯度算法。
4. 在同架构和跨架构数学推理蒸馏上均优于 sampled-token OPD 与 Top-64 OPD。

**分析推断：**

OPDVR 给现有 Agent verifier × OPD 路线提供了一个非常干净的基线：先不尝试用软 Judge 分数线性混合 distillation loss，而让可信的程序化/环境真值只控制更新方向。之后再逐步把二元终局真值扩展为带不确定性的序数 verifier advantage，可更清楚地区分“门控带来的收益”与“软分数校准带来的收益”。

## 核心方法

设 student 在自身轨迹上采样 token (o_t)，teacher 与 student 的条件概率分别为 (pi_T) 和 (pi_	heta)。

普通 sampled-token OPD 的隐式 reward 为：
[
R_{OPD}(o_t)=lograc{pi_T(o_tmid q,o_{<t})}{pi_	heta(o_tmid q,o_{<t})}
]

OPDVR 用轨迹正确性 (Rin{+1,-1}) 门控：

- 正确轨迹：
  [
  maxleft(0,lograc{pi_T}{pi_	heta}ight)
  ]
- 错误轨迹：
  [
  -maxleft(0,lograc{pi_	heta}{pi_T}ight)
  ]

因此：

- student 在正确 token 上比 teacher 更自信时，不再被 OPD 强行拉低；
- teacher 在错误轨迹 token 上比 student 更自信时，不再把错误模式推高；
- verifier 决定“强化还是抑制”，teacher–student 分布差决定幅度。

GRPD 将二元正确性替换为组内标准化 advantage，使正 advantage 样本只接受正向 teacher guidance，负 advantage 样本只接受负向抑制。

## 关键实验结果

**论文原文结果：**

- 同架构蒸馏（Qwen3-4B ← Qwen3-4B-RL，六个数学 benchmark，avg@16）：
  - Student：42.0
  - Teacher：50.4
  - Sampled-token OPD：47.8
  - Top-64 OPD：47.4
  - **OPDVR：49.1**
- 跨架构蒸馏（Qwen3-1.7B-Base ← Qwen3-4B-Base-RL）：
  - Student：17.3
  - Teacher：30.9
  - Sampled-token OPD：20.9
  - Top-64 OPD：21.7
  - **OPDVR：22.8**
- 在同架构设置中，OPDVR 相比 sampled-token OPD 平均提升 1.3 点；跨架构设置提升 1.9 点。
- 论文还报告 GRPD 可与 group-relative policy optimization 结合，并通过 gating 消融验证：反向门控显著弱于正确方向的 OPDVR。

## 证据质量与局限

**证据质量：中等。**

优点是方法极简、公式与实现关系清楚，包含同架构/跨架构设置、六个 benchmark、基础 OPD 和 Top-64 OPD 对照，以及门控方向消融；代码已公开。

**局限与谨慎解释：**

- 实验全部集中在可自动判答案的数学推理任务，尚未验证长时程工具 Agent、部分可观测环境或多轮恢复轨迹。
- verifier 是二元终局正确性；没有测试噪声 Judge、序数概率分布、A/B/T、局部步骤真值或 delayed side effects。
- 轨迹级标签被广播到所有 token；即使符号正确，也不能区分失败轨迹中的有益探索与真正致错步骤。
- 结果主要报告 avg@16，没有系统展示 pass@K、熵或能力边界是否收缩，因此不能据此断言该方法保留高熵探索。
- 论文没有 sealed evaluator 共适应问题，因为主要 verifier 是确定性答案检查；迁移到 learned Agent verifier 后该风险重新出现。
- “不增加超参数”只指门控机制无需额外 loss 权重，不能理解为训练完全无超参数。

## 最接近的相关工作

- **Reward-Gated OPD（RG-OPD）**：同样用 verifier 过滤不可靠 teacher 信号；OPDVR 的区别是从 sampled-token OPD 的隐式 reward 推导符号冲突，并用 ReLU 统一为 RLVR 形式。
- **CrEST**：同样强调 verifier 决定梯度方向、teacher/self-teacher 只调节幅度；CrEST 更关注多轮 Agent 的 turn/token 信用分配。
- **I-SDPO**：根据 rollout 组是否全失败决定蒸馏或保留 RL 样本；OPDVR 的门控粒度下沉到 sampled token 的 log-ratio。
- **AED / TA-OPD / SMOPD**：关注 teacher entropy、尾部概率质量与多轮 dirty history；OPDVR 本身不建模分布不确定性，可与这些方法正交组合。
- **OPD × Test-Time Scaling**：指出 OPD 可能改善 avg@K 却收缩大 K 能力边界；OPDVR 尚未回答这一问题。

## 如何复用或推进 LLM-as-a-Verifier

1. 把环境真值拆成三态 (zin{success, failure, unknown})：success/failure 使用 OPDVR 硬门控，unknown 不强制方向，改由校准后的 learned verifier 分布或保持零更新。
2. 对 Agent 五维评分分别构造门控；目标推进、根据可行性、安全由硬真值优先，效率和不确定性处理可使用 learned Judge 的序数分布。
3. 将二元符号扩展为 pairwise A/B/T advantage：
   - A 胜：强化 A 相对 B 的可区分 token/step；
   - B 胜：反向处理；
   - Tie：只做低幅度分布保持或校准，不把 Tie 强行拆成胜负。
4. 将 token-level log-ratio 聚合到“动作/工具调用/恢复段”层级，使门控能作用于可解释的 Agent step，而不是把终局错误广播到整条轨迹。
5. 对 learned verifier 输出做温度校准或 ordinal distribution matching；只有置信度超过预注册阈值时才让软信号控制方向。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### 1. Score-level on-policy verifier distillation

**直接改变首个基线。** 建议把 OPDVR 设为 score-level OPD 的硬真值基线：student verifier 在自身轨迹分布上学习，但方向先由环境 success/failure 决定，teacher score/log-ratio 只调幅。随后再比较“硬门控 + 序数 teacher 分布”是否优于单纯二元门控。

### 2. Pairwise A/B/T 与序数评分分布

**需要扩展。** 原文只处理二元 correctness，不支持 Tie 和多级评分。可把 verifier 的序数分布转成期望 advantage 与不确定性区间：仅当 A/B 的可信区间不重叠时做有符号更新；重叠时标为 Tie，保留多解路径。

### 3. 程序化/环境真值门控 teacher 信号

**强直接证据。** 这是论文与既有路线最吻合之处。推荐优先使用可执行终态、工具状态、副作用和安全规则作为方向门；LLM Judge 不得覆盖硬真值，只补充硬真值无法覆盖的过程质量。

### 4. Student-generated critique states

**原文未涉及。** 可在失败轨迹上让 student 生成 critique state，再由环境重放验证 critique 指出的修复是否真的改变终局；只有反事实验证通过的 critique 才进入 OPDVR 正向分支。

### 5. 高熵分叉下保留探索

**证据不足，需专门防护。** ReLU 会屏蔽与终局方向冲突的更新，但仍把整条失败轨迹视为负例。建议只在可定位的致错 step 上门控，并对失败轨迹中 verifier 不确定或具有正反事实贡献的分叉设 mask=0；评测必须同时报告 avg@K、pass@K、分支熵和新解覆盖率。

### 6. 独立 sealed eval 防止 evaluator 共适应

**在确定性数学 verifier 中不是主要问题，迁移后必须补上。** 若 Agent verifier 由 learned Judge 提供，训练内门控可能逐步适应 student 的表达风格。应冻结独立 Judge/环境快照和人工锚点，sealed eval 不参与门控、阈值调参或 checkpoint 选择，并跨模型家族复核 A/B/T 与序数校准。