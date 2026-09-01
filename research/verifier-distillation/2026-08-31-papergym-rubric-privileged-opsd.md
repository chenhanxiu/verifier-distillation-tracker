# PaperGym: Rubric-Centered Evolution for Research-Plan Generation

## 基本信息

- **作者**：Yuhan Wang, Zhengxi Lu, Yuchen Yan, Kaitao Song, Wenqi Zhang, Weiming Lu, Jun Xiao, Yueting Zhuang, Yongliang Shen
- **首次公开日期**：2026-08-31
- **版本日期**：2026-08-31（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2608.31119
- **DOI**：https://doi.org/10.48550/arXiv.2608.31119
- **代码**：https://github.com/ZJU-REAL/PaperGym
- **项目页**：https://zju-real.github.io/PaperGym

## 一句话结论

PaperGym 把原子 rubric 先作为 privileged context 做 on-policy self-distillation，再作为 GRPO 的整体验证奖励，是“生成式 verifier → 密集 OPD teacher → 稀疏 rubric reward”两阶段闭环的直接实例。

## 真正新增的内容

**论文原文结论**：论文从研究目标/背景生成问题，从方法/实验部分独立提取评分准则，以降低 task–criterion 泄漏；每个实例含十个方法创新与实验设计的原子二值准则。训练先让带 rubric 的同模型 self-teacher 对不带 rubric 的 student rollout 提供 OPSD，再用相同 rubric 作为 GRPO reward。

**分析推断**：这给现有 Agent verifier × OPD 路线一个比“直接蒸馏总分”更完整的模板：rubric 是 privileged verifier state；OPSD 把准则转成 token 级密集信号；随后独立的 outcome/rubric reward 再纠正整条输出。真正应迁移的是信号拓扑，而非研究计划这一具体任务。

## 核心方法

- 从论文的 research goal/background 构造开放问题，从 method/experiments 构造十项原子二值 rubric。
- 通过内容分离减少答案与评分准则的表面复述泄漏。
- 阶段一：同一模型在 teacher 侧可见完整 rubric，student 侧不可见；在 student 生成样本上做 OPSD。
- 阶段二：用 rubric 对完整研究计划评分，并以 GRPO 继续优化。
- 发布 PaperGym-20k，以及分别关注方法创新和实验设计的 held-out benchmark。

## 关键实验结果

**论文报告**：

- criterion leakage 为 **3.7%**，已有数据管线为 **11.90%–34.10%**。
- 在 Qwen3-1.7B/4B/8B 上，两阶段顺序相对基线的五基准平均分分别提升 **+5.6、+5.0、+4.8**。
- 同一训练配方下，PaperGym-20k 模型在三方比较中总体胜率 **58.1%**，RubricHub Science 为 **28.2%**，未训练 base 为 **13.7%**。
- Qwen3-8B 在 ResearchQA 达到 **73.48**，论文对比的 Kimi K2.6 为 **73.19**。
- 两阶段顺序优于 SFT、任一单独阶段及反向顺序。

## 证据质量与局限

- **证据质量：中高**。有 20k 数据、三种模型规模、多基准、阶段顺序和数据来源对照，并发布代码/数据/模型。
- 研究计划无硬终局真值，rubric 由论文自动构造；准则正确性、覆盖度和领域偏差仍可能进入 teacher 与 reward 两端。
- 部分比较依赖 LLM Judge，可能与训练 rubric 共享盲区。
- 论文证明的是开放式研究计划生成，不是多轮工具 Agent 轨迹。
- 同一 rubric 既进入 privileged teacher 又作为 GRPO reward，存在 evaluator 共适应风险；held-out task 不等同于独立 sealed evaluator。

## 最接近的相关工作

- Rubrics as Privileged Information / OPSD：用 privileged rubric 构造 self-teacher。
- STAR-OPD：在 student 生成集合上使用结构化 reward 蒸馏。
- AutoSciRub：先自动诱导可执行 rubric，再进行 criterion-level verification 和迭代修订。
- OPDVR、RA-OPD、GC-OPD：用 outcome/verifier 信号约束或校准密集 OPD。
- RubricHub Science：同类科学任务 rubric 数据，PaperGym 重点降低 criterion leakage 并验证两阶段顺序。

## 如何复用或推进 LLM-as-a-Verifier

- 把 Agent 的五维 rubric 拆成原子、可证据定位的准则，不直接蒸馏一个总分。
- teacher verifier 读取完整轨迹、环境状态和 rubric；student verifier 只读取部署时可得的局部状态，在 student 分布上蒸馏各准则的 score/logit 分布。
- 第二阶段用程序检查、终态结果和独立 Judge 对整条轨迹再校准，避免 privileged teacher 的密集信号变成唯一目标。
- 保留准则级 explanation/critique，使 student-generated critique state 可被逐项验证。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：优先蒸馏每项 rubric 的 logits/序数分布，再聚合，而非只回归总分。
- **pairwise A/B/T 与序数分布**：同一状态下用十项原子准则生成 A/B/T 标签，并保留各准则的不确定度，避免 scalar reward 压缩。
- **程序化真值门控**：安全、工具执行、终态状态等可验证项应覆盖自动 rubric；主观项再由 generative verifier 补充。
- **student critique states**：将“未满足准则 + 证据位置”作为 critique state，验证 critique 是否改善后续动作。
- **高熵探索**：OPSD 先建立宽先验、GRPO 后收敛的顺序值得直接做消融；同时要监控 rubric 是否过早压掉罕见可行方案。
- **sealed eval**：必须另建不暴露 rubric 文本、不同 Judge 家族和真实环境终态组成的 sealed suite，检测 criterion leakage 与 evaluator 共适应。
