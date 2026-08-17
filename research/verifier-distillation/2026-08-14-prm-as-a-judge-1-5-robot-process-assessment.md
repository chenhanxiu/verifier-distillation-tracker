# PRM-as-a-Judge 1.5：机器人过程评估工具包

## 基本信息

- **论文标题**：PRM-as-a-Judge 1.5: A Toolkit for Robot Process Assessment
- **作者**：Yuyang Liu, Yanqing Shen, Ruike Chen, Jifan Zhao, Yuxuan Tian, Yichi Zhang, Tianfeng Long, Zixuan Yin, Yipu Wang, Ziheng Qin, Wenxing Tan, Yang Shi, Mingyu Cao, Runze Xiao, Ziqi Wang, Zhixin Yin, Shiwei Chu, Yi-Fan Zhang, Yao Mu, Yuheng Ji, Yihao Wang, Jun Yan, Zhongyuan Wang, Pengwei Wang, Xiaolong Zheng
- **首次公开日期**：2026-08-14
- **版本日期**：2026-08-14（arXiv v1；项目技术文章于 2026-08-16 发布）
- **arXiv ID / DOI**：2608.14284 / 10.48550/arXiv.2608.14284
- **原始论文**：https://arxiv.org/abs/2608.14284
- **项目页**：https://prm-as-a-judge.github.io/
- **代码**：https://github.com/Yuheng2000/PRM-as-a-Judge

## 一句话结论

PRM-as-a-Judge 1.5 把机器人 rollout 视频转成稠密进度曲线，并用失败接近度、回撤恢复和成功质量等指标评估长轨迹；它不是 verifier 蒸馏算法，却提供了适合蒸馏的 distributional/process-verifier target 和独立审计基准 RoboPulse++。

## 真正新增的内容

**论文原文结论：**

- 在 1.0 的 Outcome–Process–Diagnosis（OPD，此处不是 on-policy distillation）指标体系上增加 Failure Near-Success（FNS）、Drawdown Recovery Ratio（DRR）和 Success Quality Score（SQS）。
- 发布 RoboPulse++，将 PRM 可靠性评估从简单 pairwise 比较推进到区间级进度判断，检查模型能否分辨执行过程中的上升与下降。
- 提供 benchmark、指标实现、可视化、命令行和 notebook，可从 rollout 视频生成进度曲线与交互报告。

**本文分析推断：**

对长时程文本/工具 Agent，稠密进度曲线可作为 ordinal probabilistic reward model 的蒸馏对象：student 不只预测最终成败，而是输出各步骤处于进度档位的概率分布，并派生停滞、回撤、恢复和近成功指标。

## 核心方法

输入任务描述与 rollout 视频，PRM 对时间片估计进度 `p_t`，再从整条曲线计算 outcome、process 和 diagnosis 指标。新增三项为：

- **FNS**：失败轨迹的近成功程度，组合最大进度与中后段 milestone completion；
- **DRR**：最大回撤后恢复量与该回撤大小之比，1 表示完全恢复；
- **SQS**：成功轨迹中路径效率、低回撤和低停滞的加权组合。

RoboPulse++ 用人工/基准区间级标签检验 progress judge 是否正确识别进度上升、下降及上下文依赖变化，而不只验证最终排序。

## 关键实验结果

**论文报告：**

- 在 RoboDojo-Sim 的 16 个 embodied model 上给出 11 个指标的完整排名；`π0.5` 总体平均排名第 1，Hy-Embodied-0.5-VLA 第 2，Spatial Forcing 第 3，展示单一 success rate 之外的排名差异。
- 任务类别分析中，Precision 整体最好；Long-Horizon 与 Generalization 可取得早期进度，但深度与近成功行为较弱。
- 论文指出模型规模并不保证过程质量，不同模型会在成功率、恢复能力、停滞和执行效率上呈现不同画像。
- RoboPulse++ 专门暴露 progress judge 在 falling-error 与 context-dependent 区间上的可靠性问题。
- 工具链可直接从 3 个 bundled cases 跑通视频 → judge → 曲线 → 指标 → 报告，并默认支持公开 Robo-Dopamine-GRM-2.0-8B-Preview checkpoint。

## 证据质量与局限

证据优势是评估对象多、指标定义透明、包含 judge-of-judge 基准、工具和可视化开源，并明确覆盖 Long-Horizon 类任务。

局限包括：

- 主要对象是机器人视频 rollout，向文本/网页/代码 Agent 的迁移未经验证；
- 整套指标依赖 progress judge 的曲线质量；RoboPulse++能审计但不能消除系统偏差；
- 复合指标含人为权重，例如 FNS 与 SQS 的 0.5/0.3/0.2，跨任务使用前需重新校准；
- 排名表展示的是特定 benchmark/model 集合，不应解释为一般模型能力；
- 论文没有提出 verifier distillation 训练目标，也未直接测试 A/B/T、ordinal calibration 或 teacher–student 共适应。

## 最接近的相关工作

- process reward models / process supervision
- RoboPulse 与 PRM-as-a-Judge 1.0
- robot success-rate、milestone 与 rule-based trajectory metrics
- distributional value / ordinal reward modeling
- Agent 轨迹中的 progress monitor、failure localization 与 credit assignment
- generative verifier / LLM-as-a-Judge 的 evaluator reliability benchmark

它与一般 PRM 的差异在于不把单步分数孤立使用，而是将整条 progress curve 变成可诊断的轨迹画像；RoboPulse++又进一步把 evaluator 本身纳入测试。

## 如何复用或推进 LLM-as-a-Verifier

- 训练 verifier 输出每步 `P(progress=k)` 而非单标量，曲线使用期望值，同时保留熵、分位点与校准误差。
- 从曲线自动生成 pairwise A/B/T：比较终局、最大进度、回撤恢复、停滞与成本；差异不足时保留 Tie。
- generative verifier 可先解释 milestone、回撤原因与恢复证据，再由序数头输出分布；解释与分数分别评估。
- 使用 RoboPulse++ 风格的局部上升/下降区间作为 sealed evaluator 数据，专门测试 verifier 是否真的理解动态变化。

## 对现有 Agent verifier × OPD 实验路线的具体影响

1. **score-level on-policy verifier distillation**：把 teacher target 从单个终局分数扩展为 step-wise progress distribution，再对 student 自生成 trajectory 做在线蒸馏。
2. **pairwise A/B/T 与序数评分分布**：A/B 可比较两条曲线的最终成功、FNS、DRR、SQS 和成本；Tie 由预注册阈值或置信区间定义，避免硬排序。
3. **程序化/环境真值门控**：成功、milestone、工具状态和约束违规应由环境真值校准曲线；PRM 仅填补中间过程的软标签。
4. **student-generated critique states**：在曲线回撤、停滞或高不确定区间触发 critique，让 teacher 标注“当前进度、失败原因、可恢复动作”。
5. **高熵分叉保留探索**：DRR 直接提醒“回撤不等于不可恢复”；高熵或暂时掉分的分支应保留一部分，观察后续恢复后再训练剪枝器。
6. **sealed eval**：RoboPulse++ 可作为设计蓝本：训练 verifier 与最终区间标注集隔离，隐藏任务、环境种子和 judge；同时报告 curve calibration、上升/下降识别与最终 outcome，而非只报相关系数。

## 结论边界

论文支持“稠密过程曲线能揭示 success rate 隐藏的长轨迹差异”，但没有证明这些曲线天然无偏，也没有证明指标可直接迁移到 LLM Agent。将其用于 verifier × OPD 应先验证环境门控后的校准、跨任务权重稳定性和 sealed judge 泛化。
