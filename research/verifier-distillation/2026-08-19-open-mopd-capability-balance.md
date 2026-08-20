# Open-MOPD：多 Teacher OPD 的能力失衡诊断与修复

## 基本信息

- **论文标题**：Open-MOPD: Diagnosing and Fixing Capability Imbalance in Multi-Teacher On-Policy Distillation
- **作者**：Huan-ang Gao、Haohan Chi、Yong Yan、Shiyuan Feng、Hanlin Wu、Zheng Jiang、Bingxiang He、Wei-Ying Ma、Ya-Qin Zhang、Hao Zhou
- **首次公开日期**：2026-08-19
- **版本日期**：2026-08-19（v1）
- **arXiv ID**：2608.19098
- **DOI**：10.48550/arXiv.2608.19098
- **论文**：https://arxiv.org/abs/2608.19098
- **代码、数据与评测**：https://github.com/BytedTsinghua-SIA/Open-MOPD

## 一句话结论

多 teacher OPD 的主要瓶颈并非 teacher 梯度冲突，而是不同领域的响应长度、teacher–student gap 和重复 PPO 更新造成的有效优化预算失衡；Open-MOPD 用 token-share balancing、gap-following allocation 与 reward refresh 将能力 headroom 恢复率从 35.6% 提升到 83.4%。

## 真正新增的内容

### 论文原文结论

在 oracle domain routing 下，naive M-OPD 仍无法把数学、代码与指令遵循 teacher 的能力合入同一 student。短响应的 instruction-following 约占 20% prompts，却仅占约 1% gradient tokens。不同领域的 teacher–student gap 收敛速度不同，而多次 inner update 还使缓存的 student-dependent reward 过时。Open-MOPD 分别修复这三类预算问题。

### 分析推断

对 Agent verifier × OPD，这说明“多维 verifier / 多 teacher 各自给分”后不能只平均 loss；长轨迹维度会吞掉 token 预算，易让短但关键的安全、约束、终止判断失声。

## 核心方法

1. 用已知 domain label 将 student rollout 路由给对应 frozen teacher。
2. **Token-share balancing**：按每领域实际 response-token share 反向加权，使领域 token 预算接近均衡。
3. **Gap-following allocation**：依据每领域平均绝对 token reward（剩余 teacher–student gap）动态分配预算，并裁剪权重范围。
4. **Reward refresh**：缓存 teacher log-prob，但在每次 PPO inner update 前重算当前 student log-prob，避免 stale dense reward。
5. 全流程包含 mixed-domain SFT、三个领域 RL teacher、M-OPD 及六项评测，公开训练代码与数据。

## 关键实验结果

### 论文原文

- 基座为 SmolLM3-3B，领域为数学、代码、instruction following。
- Naive M-OPD 总分 28.05；Open-MOPD 为 31.24，增益 +3.19。
- 相对 RouteRL 的 headroom recovery 从 35.6% 提升到 83.4%；与 RouteOPD 的 integration gap 从 3.50 缩至 0.31 点。
- 消融中 token-share balancing、gap allocation、refresh 均提供增益；IF 是 naive 方法受损最明显的领域。
- 用 teacher consensus 替换高 disagreement token 反而降低总分，支持“teacher 冲突不是主瓶颈”。

## 证据质量与局限

- **质量**：oracle routing 隔离了路由误差；完整 ablation；六个公开 benchmark；代码、teacher/student checkpoints、训练与评测数据公开。
- **局限**：仅一个 3B student、三类相对清晰的领域；oracle domain label 不符合开放 Agent 的模糊状态；不同 benchmark 的 mean@K 不一致；没有 verifier distillation 或长时程 Agent 环境实验；v1 预印本。
- 训练和主要评测使用同一类公开 verifier，仍需独立 sealed evaluator 检查共适应。

## 最接近的相关工作

多 teacher OPD、DoReMi/MoDoMoDo 数据混合、domain RL expert merging、TIES/DARE，以及 reward refresh / PPO staleness 研究。

## 如何推进 LLM-as-a-Verifier

- 将每个 rubric、phase 或错误类型视为一个“领域”，统计其实际 token/turn 覆盖、reward magnitude 与收敛 gap。
- 对序数 reward distribution，不只均衡样本数，还应均衡每一档评分贡献的有效 gradient mass。
- 将 teacher/verifier score 缓存与 student 当前分布解耦：teacher 可缓存，student-dependent residual 应刷新。

## 对 Agent verifier × OPD 路线的具体影响

以下为**分析推断**：

- **Score-level OPD**：按 rubric/阶段统计有效更新预算，防止长答案质量维度压制短工具参数或安全维度。
- **A/B/T**：T 不应视为零信息；应单独监控其 token share 与 gap，避免平局样本被长轨迹稀释。
- **真值门控**：程序化 verifier 维度可做硬方向，LLM Judge 维度只调幅；两者必须分别报告预算。
- **Critique states**：critique 通常更长，若直接拼接会占据多数 token loss；应按 action/turn 而非原始 token 平衡。
- **高熵探索**：gap 大不等于错误，应限制动态权重，避免某一高熵 teacher 获得失控预算。
- **Sealed eval**：训练调度以训练域 gap 为依据，sealed evaluator 不参与动态预算；每个维度分别报告校准和 capability regression。