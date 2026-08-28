# J-Zero：Challenger–Solver–Judge 零数据共演化

## 基本信息

- **论文标题**：J-Zero: Unified Challenger--Solver--Judge Co-Evolution from Zero Data
- **作者**：Gyouk Chu、Myeongho Jeon、Eunho Yang
- **首次公开日期**：2026-08-27
- **版本日期**：2026-08-27（v1）
- **原始论文**：[arXiv:2608.26582](https://arxiv.org/abs/2608.26582)
- **DOI**：[10.48550/arXiv.2608.26582](https://doi.org/10.48550/arXiv.2608.26582)
- **代码链接**：[GyoukChu/J-Zero](https://github.com/GyoukChu/J-Zero)（当前公开仓库仅含 README/License，代码可用性有限）

## 一句话结论

J-Zero 不让 Judge 用自己的分数给自己造标签，而是利用“生成过程已知排序”的偏好对共同训练 Challenger、Solver 和 Judge，使不可验证任务的自演化能持续十轮；这是降低 evaluator 自我确认偏差的有力原型。

## 真正新增的内容

**论文原文结论：**

- Challenger 生成更难任务，Solver 学习回答；Judge 同时使用生成机制自带排序的 preference pair 共适应。
- 两类排序来源：Solver answer 优于 Challenger answer；分解后重组的 answer 优于 one-shot answer。
- 标签顺序由生成路径预先规定，而非来自 Judge 自己的当前分数，避免直接自举。
- 方法同时覆盖可验证与不可验证域，十轮内持续提升，基线约两轮后退化。

**分析推断：**

“先构造有结构依据的 A/B，再训练 Judge”比让 Judge 给自身轨迹打分更接近 sealed teacher signal。对 Agent verifier 可用同状态下的恢复分支、环境真值分支和可逆修复分支构造 A/B/T，但生成机制的默认排序仍需抽样审计，不能天然当作真值。

## 核心方法

1. Challenger 与 Solver 进行对抗式任务—回答共演化。
2. 从角色不对称生成 A/B：Solver 回答默认优于 Challenger 的困难样例式回答。
3. 从子任务放大生成 A/B：分解并重组的回答默认优于 one-shot。
4. Judge 是 classifier-based discriminative reward model，以 Bradley–Terry loss 学这些 preference pairs。
5. 更新后的 Judge 为不可验证任务提供新训练信号，从而抬高 Solver 的可学习上限。

## 关键实验结果

**论文原文结果：**

- 相比基线，平均在可验证域提高 4.2 点、不可验证域提高 8.0 点。
- Qwen3-4B 的可验证 Overall：J-Zero 54.38，R-Zero 49.64，G-Zero 47.41。
- Qwen3-8B 的可验证 Overall：J-Zero 58.55，R-Zero 54.99，G-Zero 53.07。
- 论文报告至少十轮持续改善，而对照方法在约两轮后开始退化。
- 评测覆盖数学、通用推理、指令遵循，以及 AlpacaEval、Arena-Hard、Creative Writing 等不可验证任务。

## 证据质量与局限

**证据质量：中高。** 跨 4B/8B、可验证/不可验证多基准，并与两类 zero-data self-evolution 基线比较。主要限制：训练最多 8B，未测 post-trained reasoning model 与长 CoT；Judge 是现成初始化的判别式 RM，不是生成式 Judge；“Solver 优于 Challenger”“分解优于 one-shot”是结构性假设，可能有错序。部分不可验证评测仍依赖模型 Judge，存在 evaluator 相关性。公开仓库目前几乎没有实现代码。

## 最接近的相关工作

- RecurSE：Judge–Checker 共演化与有效停止窗口。
- R-Zero / G-Zero：Challenger–Solver 零数据自演化。
- Bradley–Terry reward modeling：从 pairwise preference 训练判别 Judge。
- SafeBranch / COTA / ParallelWorld：从同状态构造反事实分支对。
- Rubric Dropout：共演化 evaluator 导致 reward hacking 的风险。

## 如何复用或推进 LLM-as-a-Verifier

- 以生成机制产生可审计的 pair：成功恢复 > 未恢复、满足硬真值 > 违反真值、较少副作用 > 较多副作用。
- 将默认排序分为“硬排序”和“弱排序”：环境可验证 pair 用硬标签；仅基于分解/角色假设的 pair 保留概率标签或 Tie。
- Judge 训练后必须在人工与环境独立对上校准，而不能只看其对自生成 pair 的训练准确率。
- 将生成式 critique 作为未来扩展：Judge 不仅输出 A/B/T，还说明决定排序的环境证据与关键步骤。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### Score-level on-policy verifier distillation

可先用结构化 pair 更新 verifier，再将更新后的 score distribution 蒸馏到 student；避免 student 与 verifier 同时依靠 verifier 自评分闭环。

### Pairwise A/B/T 与序数评分分布

高度相关。A/B 标签来自生成过程，但对证据不足或两条路径都成功的情况应显式建 Tie，并保留标签置信度形成序数/概率监督。

### 程序化/环境真值门控

应把 J-Zero 的结构排序升级为环境真值排序：同 state 的分支重放、终态 diff、工具副作用与安全规则决定硬方向。

### Student-generated critique states

原文只用判别 RM。可让 student 为每个 pair 生成“为何 A 胜 B”的 critique，再由环境证据检查，验证通过后用于 generative verifier 蒸馏。

### 高熵分叉下保留探索

Challenger 持续提高难度有助于覆盖决策边界；但不要只保留赢家，应保存同状态的多分支与 Tie，防止 Judge 过早把新策略压成单一偏好。

### 独立 sealed eval

论文自身会根据评测下降选择停止点，因此迁移时必须把开发停止集与 sealed eval 分离。sealed set 应冻结任务、环境、Judge 家族和版本，禁止进入 Challenger、Solver、Judge 任一更新环。