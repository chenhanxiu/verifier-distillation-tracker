# CROP：通过反事实任务相关性选择性进行 On-Policy Distillation

## 基本信息

- **论文标题**：CROP: Task Relevance via Counterfactuals for Selective On-Policy Distillation
- **作者**：Enhan Li、Junhao He、Hongyang Du
- **首次公开日期**：2026-08-13
- **版本日期**：2026-08-13（arXiv v1）
- **arXiv ID**：2608.13387
- **DOI**：10.48550/arXiv.2608.13387
- **原始论文**：https://arxiv.org/abs/2608.13387
- **代码**：论文正文记录了实现版本，但公开页未给出可确认的官方代码仓库链接

## 一句话结论

CROP 用“语义条件变化引起的分布位移，减去等义改写引起的分布位移”选择 OPD token，在固定 10% 监督预算下优于已有选择器，说明 task relevance 是 uncertainty/disagreement 之外独立且有用的蒸馏信号。

## 真正新增的内容

**论文原文结论**：既有 selective OPD 多回答“哪里需要优化”，CROP 首次把“该 token 的监督是否真正依赖当前任务语义”显式操作化为 paraphrase-calibrated counterfactual sensitivity margin。

它不是新的 teacher loss，而是保持 student rollout、teacher target 与 sampled-token OPD 目标不变，只改变哪些位置进入损失。因此新增点主要是可插拔的 token 选择准则及严格的 matched contrast 构造。

## 核心方法

1. 为每个原始问题离线生成并验证三元组：原题、等义改写、只改变一个实质条件的反事实题。
2. student 仅在原题上生成一次 on-policy rollout；在三种 prompt 下对同一响应及同一 prefix 重打分，避免把不同采样轨迹误当作语义敏感性。
3. 对每个位置计算 top-64-with-residual Jensen–Shannon divergence：
   - 反事实敏感度：原题分布与反事实题分布的 JSD；
   - 表面敏感度：原题分布与等义改写分布的 JSD；
   - CROP 分数为前者减后者。
4. 在 batch-global 固定预算下选择最高分 token，形成硬 mask，再执行原有 sampled-token OPD。可选 CROP-ent 把 student entropy 与相关性混合。

## 关键实验结果

**论文报告**：

- 训练使用 16,594 个数学 prompt，评估覆盖 AIME24、AIME25、MATH-500、GPQA-Diamond、HumanEval、IFEval。
- Qwen3-4B teacher → Qwen3-1.7B student：CROP 六项平均 47.98，比 Pure OPD 高 3.11 点，比最强非 CROP 选择器 TIP 高 1.92 点。
- Qwen3-8B（GRPO）teacher → Qwen3-4B student：CROP-ent 平均 57.48，CROP 为 57.13；CROP 相对最强非 CROP 选择器提高 2.96 点。
- highest-relevance 选择优于匹配预算的随机选择，lowest-relevance 明显更差；消融支持反事实敏感度是主信号，等义校准带来额外收益。

## 证据质量与局限

- **证据质量：中等。** 有两个 teacher–student 配置、固定预算的强基线、组件消融、污染审计与复现实验细节。
- **论文原文局限**：仅覆盖 Qwen 系列和数学训练 prompt；反事实三元组由模型自动构造，虽经独立 critic 验证，仍未控制所有混杂因素（如难度）；尚未直接验证代码、开放域或长时程 Agent。
- CROP 分数是 model-internal、contrast-specific 排序启发式，不是正确性、真实因果效应或 ground-truth relevance 的证明；额外三次 student rescoring 的时延/能耗未评估。
- 结果主要是 aggregate accuracy，不能证明在 sealed evaluator 下不存在 selector–benchmark 共适应。

## 最接近的相关工作

最接近的是 TIP（entropy + teacher–student divergence）、TA-OPD（局部可教性）、TrOPD（teacher reliability trust region）、CREDIT（用无关问题构造输入敏感信用）和 DOPD（按 privileged-policy advantage 路由）。CROP 的区别是用同一题的等义/单条件反事实配对，尽量把任务语义变化与表面变化分开。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：

- 把 verifier 的 score distribution 或 A/B/T 判断分布替代 next-token distribution，计算“反事实条件改变是否使评分分布移动、等义改写是否保持稳定”，可形成 verifier-level relevance mask。
- 对序数评分 (1\ldots K) 不应只比较均值；可在完整 ordinal distribution 上用 JSD、Wasserstein 距离或累计概率差，使“同均值、不同不确定性”的监督仍可区分。
- 三元组验证最好由程序化约束或环境真值门控；LLM critic 只负责语义检查，避免 teacher 与 selector 共享同一偏差。
- 反事实/等义对可加入 sealed eval，专门检测 verifier 是否学习到格式、长度或措辞捷径。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level on-policy verifier distillation**：在 student-generated trajectory/critique states 上，不必蒸馏全部状态；优先蒸馏对任务条件敏感且对等义变化稳定的状态。
- **pairwise A/B/T 与序数分布**：为同一轨迹构造等义环境描述与单条件反事实，比较 A/B/T 或 ordinal 分布的变化；相关性分数可与 entropy/disagreement 作为二维 selector，而非压成单一置信度。
- **真值门控 teacher 信号**：只有反事实确实改变程序执行结果、环境状态或约束满足性时才接受 triplet，防止伪反事实污染。
- **高熵分叉保留探索**：不要把高熵直接视为应蒸馏。可仅在“高熵且高 task relevance”时加强 verifier 监督；高熵但低相关位置保持探索。
- **student-generated critique states**：固定 student critique prefix 后做 matched rescoring，避免独立生成三条 critique 导致轨迹差异混入 relevance。
- **sealed eval**：训练 selector 与最终 evaluator 应隔离，并加入未见过的 paraphrase/counterfactual family，检验相关性是否迁移，而非只适配三元组生成器。
