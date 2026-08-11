# CoDA：从共识与分歧进行无监督 On-Policy Self-Distillation

## 基本信息

- **论文标题**：Learning from Consensus and Disagreement: Unsupervised On-Policy Self-Distillation with Minority-Trajectory Contrast
- **方法名**：CoDA
- **作者**：Jiaxin Guo, Yanwei Yue, Xuanbo Fan, Chunyu Yang, Yan Zhang
- **首次公开日期**：2026-08-09
- **当前版本日期**：2026-08-09（v1）
- **arXiv ID**：2608.08764
- **原始论文**：https://arxiv.org/abs/2608.08764
- **代码**：截至记录时未发现公开代码仓库

## 一句话结论

CoDA 不依赖外部标签，利用同一问题上 student rollouts 的多数答案形成正向共识监督、以少数轨迹形成温和负向校准，使 1.7B/4B 数学模型获得有效 OPSD 增益，但“少数即不可靠”会威胁高熵探索。

## 真正新增的内容

**论文原文结论：** CoDA 将自生成轨迹中的共识与分歧同时转为训练信号：冻结的 self-teacher 以共识信息提供稠密分布监督，少数轨迹则通过 reference-anchored、KTO 风格目标受到温和抑制。作者明确承认共识可能错误，负向分支用于减轻错误共识的放大。

**分析推断：** 它展示了无需 ground-truth 的“分支内相对监督”，但共识/少数并不等价于正确/错误。对长时程 Agent，更安全的解释应是“共识作为先验、分歧作为待验证状态”，而不是直接剪枝少数路径。

## 核心方法

1. 每个问题从当前 student 采样 10 条轨迹，归一化最终答案并选出众数。
2. 至少两条有效轨迹共享众数时形成共识；1.7B 设置选择最短众数轨迹，4B 设置采用随机众数轨迹。
3. 冻结、adapter-disabled 的初始策略充当 self-teacher，并在共识条件下对新的 student rollout 提供 forward-KL 分布监督；KL divergence clipping 为 0.05。
4. 少数答案轨迹进入 reference-anchored KTO 风格负向校准；论文设置 β=0.1，每个问题最多使用一条少数轨迹。
5. 正负两分支共同训练，无需人工标签或外部 verifier。

## 关键实验结果

**论文报告：**

- 使用 Qwen3-1.7B 和 Qwen3-4B，在 AIME24、AIME25、AIME26、AMO、HMMT25 上评估。
- 1.7B 五任务平均：Base 29.74，SFT 32.13，监督 OPSD 35.81，GRPO 32.69，SFT-Self oracle 31.73，TTRL 31.42，CoDA 共识分支 34.37，完整 CoDA 36.12。
- 完整 CoDA 1.7B 的分任务结果为 56.67/41.67/47.29/4.75/30.21。
- 4B 上，TTRL、CoDA 共识分支、完整 CoDA 的平均分分别为 52.73、53.70、54.57。
- 1.7B 中选择最短共识轨迹效果最好：平均 36.12；随机和最长轨迹分别为 35.26、35.28。
- 采样设置为 temperature 1.3、top-p 0.95；这些结果支持在该数学推理设置中，少数轨迹对比可在共识蒸馏之上继续带来增益。

## 证据质量与局限

**证据较强处：** 同时覆盖 1.7B/4B、多项数学 benchmark 和多类无监督/监督基线，并包含共识轨迹选择与正负分支对比。

**局限及分析：**

- 实验只覆盖可归一化最终答案的数学任务，没有工具调用或长时程 Agent 轨迹。
- 共识可能系统性错误，少数轨迹也可能是唯一正确或更具探索价值的路径；同源模型采样还会产生相关错误。
- 负向信号是未配对的二元偏好式反馈，不是严格的 pairwise A/B/T，也不是校准过的序数概率分布。
- 没有程序化环境真值时，少数分支的惩罚可能压制“罕见但正确”的高熵探索。
- 截至记录时未发现公开代码；论文未提供足以覆盖上述迁移风险的 Agent 实验。

## 最接近的相关工作

- OPSD / self-distillation：在 student 自身访问到的分布上蒸馏冻结或更强 teacher。
- TTRL 与无监督 self-training：从模型自己的聚合答案产生训练信号。
- KTO：从非配对 desirable/undesirable 反馈学习。
- Self-consistency：通过多样本答案共识提高推理可靠性。
- Distributional/ordinal reward modeling：显式表示评分不确定性，而 CoDA 仍主要使用共识二元结构。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 将共识比例、少数分支质量和 teacher 分数一起建模为序数评分分布，不把众数硬编码成真值。
- 对 student-generated critique states 做聚类，使用“共识 critique + 分歧 critique”训练生成式 verifier，但最终标签要由环境回执或程序测试校准。
- 把少数轨迹视为主动验证队列：在额外 rollout、工具检查或反事实继续后，再决定 A/B/T。
- 蒸馏 teacher 的置信区间或完整 score histogram，使 student verifier 能区分“多数但低置信”和“少数但可验证”。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断：**

- **Score-level OPD**：把 CoDA 的硬共识目标替换为 teacher 的序数概率分布；KL 蒸馏应保留不确定性。
- **Pairwise A/B/T**：仅在环境真值区分两分支时判 A/B；两个分支都成功、都失败或证据不足时明确记 tie。
- **真值门控**：程序化测试、工具执行结果和环境终态应高于答案共识；共识只作弱先验。
- **Critique states**：对同一状态采样多条 student critique，分歧本身可作为 verifier 查询或额外探索触发器。
- **高熵探索**：禁止把 minority 自动当负例；对少数路径保留熵预算，并优先验证可恢复性。
- **Sealed eval**：训练时的 consensus teacher、负向校准器与最终 evaluator 必须隔离，避免共同偏差被自蒸馏放大。

CoDA 值得作为“无标签分叉监督”基线，但 Agent 版实验应加入环境真值门控、tie/ordinal 表示和少数路径保护。
