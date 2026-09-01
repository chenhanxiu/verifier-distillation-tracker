# S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?

## 基本信息

- **作者**：Jiajun Shi, Siyuan Tao, Yuhao Wu, Zexuan Wang, Jingyuan Zhang, Jiaheng Liu, Xinping Lei, Xinrong Zhang, Siyuan Fang, Zhewen Tan, Tianle Cai, Junhao Fang, Jiameng Huang, Yueyang Wang, Jinkai Liu, Yuxuan Zhang, Jian Yang, Zhoujun Li, Shen Yan, Wenhao Huang, Ge Zhang
- **首次公开日期**：2026-08-31
- **版本日期**：2026-08-31（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2608.31100
- **DOI**：https://doi.org/10.48550/arXiv.2608.31100
- **项目页**：https://self-developing-agents.github.io/
- **代码**：论文页面当前未给出独立代码仓库

## 一句话结论

S3Gym 把 permissive exploration、模型自评分与更严格的可执行 held-out eval 明确拆开，直接提供了审计“student-generated experience/critique 是否真的带来可迁移改进”的 sealed-eval 原型。

## 真正新增的内容

**论文原文结论**：该 benchmark 不把 Agent 当作固定策略，而是联合测量 Self-Testing、Self-Judging、Self-Improvement。七个文本游戏提供可执行环境 verifier；探索阶段不向 Agent 暴露 verifier outcome，评测阶段使用更严格或更困难的配置。论文比较 History ICL、score-conditioned Summary Memory 和参数训练三条经验吸收路线。

**分析推断**：它最重要的价值不是新训练算法，而是把“模型认为经验有价值”和“环境证明经验可迁移”变成两个可独立测量的变量。这正适合检验 critique-state verifier 蒸馏与 evaluator 共适应。

## 核心方法

- Agent 在宽松环境中主动探索并为交互经验生成自评分。
- 环境保存独立的可执行真值，但探索期不把该 outcome 直接交给 Agent。
- 三种经验使用路径：
  - History ICL：保留原始轨迹细节；
  - Summary Memory：把得分、规则、错误和改进方向压缩为记忆；
  - Parameter Training：将筛选经验写入参数。
- 严格评测使用不相交且通常更难的配置，例如 Minesweeper 从额外生命变为触雷即终止、Snake 从碰撞 no-op 变为碰撞终止。
- 同时记录 self-judgment 与环境 outcome，用于区分“判断错”还是“判断对但无法转成策略”。

## 关键实验结果

**论文报告**：

- 评测七个文本游戏，并在上下文路线比较 GPT-4o、GPT-4.1、o3-mini、Gemini-2.5-Flash/Pro、GPT-5.5、Gemini-3.5-Flash 等模型。
- Summary Memory 在可压缩为通用策略的任务上有效；依赖精确状态信息时常弱于原始 History ICL。
- Qwen3-8B 参数训练在 Trust Evolution 明显提升，但 Minesweeper、Nullify、Tetris 仍为零改进。
- Plants-vs-Zombies 初始分为 **23**，更新后各 checkpoint 均为 **6**，出现严重负迁移。
- 每个探索周期最多 30 个 episode，每 3 个 episode 在严格模式上评估一次；每个 checkpoint 使用 3 个严格模式 episode。

## 证据质量与局限

- **证据质量：中**。协议设计与可执行真值很强，覆盖多模型和三类经验路径；但每个 checkpoint 的严格评测仅 3 个 episode，方差可能较大。
- 游戏环境与真实工具 Agent 的任务结构、状态噪声和长轨迹成本不同。
- self-judgment 不是一个专门训练/蒸馏的 verifier，论文也未直接比较 distributional/ordinal reward model。
- 探索与评测配置不同是优点，但不等于完全隐藏的长期 sealed benchmark；重复迭代仍可能间接适应协议。
- 参数训练失败原因多为诊断性推测，尚缺逐轨迹因果归因。

## 最接近的相关工作

- SEA-Eval、SEAGym、PAST-Bench、ContinualSkillBench、FinEvo-Bench：持续适应、记忆或技能累积 benchmark。
- RecurSE：审计 Judge–Checker 共演化和独立锚定停止窗口。
- LongWoF-Bench、LongRCA Bench：验证经验可复用性与长轨迹失败定位。
- MemGuard、MuseCritic：将 verifier/critique 信号写入持久经验或 student-generated critique state。

S3Gym 的区别在于把 self-testing、self-judging 和后续改进放入同一可执行、严格 held-out 协议中。

## 如何复用或推进 LLM-as-a-Verifier

- 为每条探索轨迹同时保存 student 自评分分布、critique、环境 outcome 和严格重放结果。
- 将 self-judging 作为 verifier student 的输入状态，而不是默认可靠标签；用环境 truth 校准其置信度。
- 分别测量判断正确率与“经该判断筛选的经验对未来策略的 uplift”，避免只优化 judge agreement。
- 对 score-conditioned memory 做原始轨迹对照，判断压缩是否抹掉关键状态信息。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：训练集应来自 permissive student exploration，但评测必须落在更严格、未参与更新的环境配置。
- **A/B/T 与序数分布**：同一状态分支可同时用 self-judgment 与 executable outcome 标注；二者不一致时形成高价值 A/B/T 校准样本。
- **程序化真值门控**：environment verifier 应作为经验准入的最终门槛，自评分只能提供筛选优先级。
- **student critique states**：直接比较 raw history、score-conditioned summary、critique memory 三种状态表示对 held-out uplift 的影响。
- **高熵分叉**：宽松探索阶段保留多样路径；不要仅按自评分截断，否则可能把判断偏差固化为经验污染。
- **sealed eval**：采用“宽松训练环境 + 更严格配置 + 隐藏真值”的三层协议，并增加独立任务族与长期冻结集，监测 verifier 与 policy 共适应。
