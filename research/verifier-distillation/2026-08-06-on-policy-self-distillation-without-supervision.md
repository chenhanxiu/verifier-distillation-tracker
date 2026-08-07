# On-Policy Self-Distillation without Any Supervision

## 基本信息

- **作者**：Yijiang Li、Bingyang Wang、Yijun Liang、Yunjie Tian、Di Fu、Nuno Vasconcelos
- **首次公开日期**：2026-08-06
- **当前版本日期**：2026-08-06（arXiv v1）
- **arXiv ID**：2608.06296
- **原始论文**：https://arxiv.org/abs/2608.06296
- **代码**：截至记录时未发现公开代码仓库
- **记录类型**：新论文（2026-08-07 检出）

## 一句话结论

论文表明，模型可仅靠自身多次采样形成高置信伪答案，再把“短且答对共识”的轨迹作为 privileged teacher，对自身失败轨迹做 on-policy 分布蒸馏；在非思考模式数学任务上明显有效，但其 teacher 信号仍受错误共识与精确答案投票的限制。

## 真正新增的内容

**论文原文结论：**作者提出 u-OPSD，不使用人工答案、外部 teacher 或可执行 verifier，只给定未标注问题。它利用当前模型 rollouts 的答案共识自动确定伪标签，从同一批 on-policy 样本中构造成功 teacher 与失败 student prefix，因此把监督式 OPSD 推进到无监督设置。

相较于常见“只模仿成功样本”的自训练，该方法不只训练成功序列的采样 token，而是把成功轨迹产生的完整 token 分布蒸馏到失败轨迹状态；重点落在模型当前能力边界附近、既有成功也有失败的题目。

**分析推断：**其价值不在于“多数票等同环境真值”，而在于给出一个可替换的 teacher-signal 管线：在 Agent 场景中可将答案共识替换为程序化测试、环境回报或 sealed judge，把论文的失败状态条件化蒸馏原样保留。

## 核心方法

1. 对每个无标注问题从当前策略采样多条回答，并抽取最终答案。
2. 当 plurality/majority 共识超过置信阈值时，将共识答案作为伪标签；不够确定的问题跳过。
3. 在与伪标签一致的轨迹中选择较短的一条，作为包含 privileged solution context 的 teacher reference。
4. 从不一致轨迹中选取较长或代表性的失败 completion，并在其 prefix 状态上查询 teacher 分布。
5. 以 forward KL/全词表分布为主，将 teacher 的 token-level 分布蒸馏回同一模型；训练样本始终来自当前策略，因而保持 on-policy。

## 关键实验结果

**论文报告：**

- 在 Qwen3 4B/8B 的数学推理实验中，非思考模式相对 base 平均提升约 **8.5% / 10.7%**，并相对需要监督答案的 OPSD 平均高约 **3.2% / 2.3%**。
- 在思考模式中收益显著缩小：相对监督 OPSD 约为 **+0.9 个百分点 / 基本持平**，说明强推理模式下自举空间有限。
- 小规模伪标签审计中，约 **86.7%** 的共识伪答案与 gold 一致，仍有 **13.3%** 错误共识。
- 全词表或 top-k 分布蒸馏优于只学习采样 token；reverse KL 出现训练不稳定/发散，JSD 接近 base，说明方向与分布覆盖很关键。

不同表格可能采用平均准确率或相对提升口径；以上按论文报告口径摘录，不将跨设置数字直接合并比较。

## 证据质量与局限

- 优点：包含监督 OPSD、不同散度、分布截断方式和 thinking/non-thinking 设置的对照，能较清楚隔离“无监督伪标签 + 分布蒸馏”的贡献。
- 局限：主要集中于一个模型家族和数学题；答案可被规范化并精确投票，不能直接代表开放式 Agent 轨迹。
- 共识不是事实保证。论文自己的审计显示错误伪标签不为零，多数错误可能被自蒸馏放大。
- 没有直接测试长时程 credit assignment、环境交互、开放式 critique 或独立 evaluator 共适应。
- 公开结果不足以证明对随机种子、迭代轮次和跨域迁移都稳定；截至记录时也没有公开代码便于复现。

## 最接近的相关工作

- **On-Policy Self-Distillation（OPSD）**：使用当前策略状态和 privileged reference solution 做分布蒸馏；u-OPSD 的主要差异是去掉人工 reference answer。
- **Self-training / majority-vote pseudo-labeling**：同样从模型自身样本形成监督，但通常只优化硬标签或成功序列。
- **STaR、rejection sampling fine-tuning**：依赖筛选出的正确推理；u-OPSD 进一步利用失败轨迹的状态。
- **Verifier-guided RL / process reward models**：可提供比共识更可靠的正确性门控，但一般需要额外 verifier 或环境。

## 如何复用或推进 LLM-as-a-Verifier

最直接的复用方式，是把“回答共识是否足够高”改造成多源门控：

- 可执行任务优先使用单元测试、环境终态和约束检查；
- 不可执行任务再用独立 LLM judge 的 A/B/T 或序数评分分布；
- 仅当程序真值、环境结果与模型共识一致，或 posterior 置信度超过阈值时，才开放 teacher 蒸馏；
- 保留共识冲突样本作为 verifier calibration 与 hard-negative 数据，而非直接丢弃。

论文 teacher 目前提供的是解题分布，不是显式 critique。可让 generative verifier 先针对 student 失败 prefix 生成“下一步风险/修复建议”，再把该 critique 作为 teacher 的 privileged context，以测试 student-generated critique states 是否比完整参考解更贴近部署分布。

## 对 Agent verifier × OPD 实验路线的具体影响

1. **Score-level on-policy verifier distillation**：支持在 student 自己产生的失败状态上蒸馏，但应把硬共识替换为 teacher 的评分分布；优化 ordinal-bin KL 或 calibrated score distribution，而不只蒸馏答案 token。
2. **Pairwise A/B/T 与序数分布**：同一问题的成功/失败 rollout 天然构成 A/B；对结局等价或证据不足的样本保留 T（tie/uncertain），避免强行排序。共识比例可作为序数 posterior 的先验而非标签真值。
3. **程序化/环境真值门控**：这是从数学题迁移到 Agent 的关键。环境真值应高于 rollout majority；冲突时不更新或降权。
4. **Student-generated critique states**：论文已经以失败 prefix 为 student state；下一步应比较“reference solution 条件 teacher”与“student critique + 环境证据条件 teacher”。
5. **高熵分叉与探索**：只蒸馏能力边界题很合适，但不要把所有少数派视为失败。若多个分支均通过环境检查，应保留其概率质量，并只压低可证伪分支。
6. **Sealed eval**：训练门控 verifier 与最终评估器必须隔离。独立保留任务、环境 seed、judge prompt/模型，防止模型学会迎合形成伪标签的 evaluator。

## 建议的最小验证实验

在长时程 Agent benchmark 上，每个初始状态采样 8–16 条轨迹；以环境终态产生 gold gate，同时构造 majority、LLM judge 与二者融合三种伪门控。仅在 student 失败分叉蒸馏 teacher 的 5 档序数回报分布，并对通过环境检查的多样分支设置 tie/保留项。最终用从未参与训练的 sealed evaluator 比较成功率、ECE、分叉熵和错误共识放大率。
