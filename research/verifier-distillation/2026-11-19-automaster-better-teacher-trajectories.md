# AutoMaster: Autonomous Post-Training by Making the Same Model a Better Teacher

- **作者**：Guoxin Chen, Shuang Sun, Fanzhe Meng, Xinyu Tang, Ruihua Song, Wayne Xin Zhao
- **首次公开日期**：2026-11-19
- **版本日期**：2026-11-19（v1）
- **原始论文**：[arXiv:2611.26510](https://arxiv.org/abs/2611.26510)
- **DOI**：[10.48550/arXiv.2611.26510](https://doi.org/10.48550/arXiv.2611.26510)
- **项目页**：[AutoMaster](https://aweai-team.github.io/AutoMaster/)
- **代码**：[RUCAIBox/AutoMaster](https://github.com/RUCAIBox/AutoMaster)
- **模型**：[Hugging Face](https://huggingface.co/)

## 一句话结论

【论文原文】成功轨迹也含不良行为，AutoMaster 通过轨迹分析自动设计自然语言 skill 干预，使同一固定模型生成更适合蒸馏的 teacher trajectories；【分析推断】Verifier 蒸馏不应只筛“成功/失败”，还应审计成功轨迹中的验证质量、冗余和无依据假设。

## 真正新增的内容

【论文原文】Skill-FT 用自然语言 skills 抑制不良习惯并激发欠覆盖的有效行为，再用受干预 teacher rollout 微调 target。AutoMaster 将轨迹分析、skill 设计、数据选择、rollout 反馈和 target-model 评估组成自主闭环。

【分析推断】该工作补上 verifier × OPD 的上游数据问题：即使环境最终成功，teacher trajectory 也不一定是安全、可泛化或高信息量的监督；应把 verifier 用于“成功轨迹内部的行为质量选择”。

## 核心方法

【论文原文】

1. 分析既有 Agent 轨迹中的支持不足、无效重复与表面验证等行为；
2. 生成自然语言 skill 作为 teacher rollout 的行为干预；
3. 选择受干预后更合适的轨迹；
4. 用这些轨迹做 Skill-Guided Fine-Tuning；
5. 根据新 rollout 与 target-model 评估反馈继续调整技能与数据；
6. teacher、任务池、训练集规模和 SFT 配方保持不变，用于隔离干预效果。

## 关键实验结果

【论文原文】

- 在 Terminal、Search 和软件工程任务上，4B/9B target 相对成功但未引导 teacher 轨迹的 Vanilla SFT，平均提升 1.42–8.99 个百分点。
- 六个设置中，SFT 时保留 skill instruction 均优于移除 instruction，尽管评估时不提供该 instruction，且监督输出相同。

## 证据质量与局限

【论文原文】跨三类 Agent 任务与两种模型规模，并通过固定 teacher、任务池、数据规模和训练配方减少混杂；保留/移除 skill instruction 的对照很有信息量。局限是主要比较 SFT 路线，未直接训练 reward model，也未在摘要中给出独立 evaluator、环境真值覆盖、成本和 reward-hacking 审计。

【分析推断】自主闭环可能逐步偏向 target evaluator 的口味；成功率提升不能单独证明 teacher 轨迹更真实或更安全。

## 最接近的相关工作

- DENSE：把 Agent 轨迹蒸馏为带恢复证据与未完成义务的结构。
- RSIAgent、SkillAA：验证记忆/skill 后再提交或回滚。
- FLARE：从环境结算的错误链训练生成式 reward model。
- data-free OPD 与自生成 curriculum：关注少量 prompt 产生高覆盖 on-policy 状态。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 AutoMaster 的 skill 设计模块接到 generative verifier：verifier 不只输出成功分，还标注“无依据假设、伪验证、重复、漏掉恢复条件”等行为标签。仅当环境结算和独立 verifier 同时改善时，才允许 skill 影响 teacher rollout；把 skill instruction 作为 privileged teacher context 蒸馏给 student。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：score 不只看终局成功，还加入证据质量与验证行为维度；teacher rollout 先经行为审计再蒸馏。
- **pairwise A/B/T 与序数评分分布**：比较同一 teacher 在有/无 skill 干预下的轨迹，终局相同但证据质量不同仍可形成 A/B；证据不足标 T。
- **程序化/环境真值门控**：skill 只能改变软监督和采样，不得覆盖失败测试或环境不一致。
- **student-generated critique states**：将自动生成 skill 视为候选 critique/memory，须经局部重放和全局成功率双门控。
- **高熵分叉保留探索**：skill 用于增加欠覆盖行为，而非只强化当前最优轨迹；以分支覆盖与验证收益分配预算。
- **独立 sealed eval**：冻结任务集、环境和 evaluator，比较“同成功率下的证据质量”及未见任务泛化，防止闭环追逐自有评分器。
