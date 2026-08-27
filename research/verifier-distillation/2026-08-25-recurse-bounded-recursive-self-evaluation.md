# RecurSE：面向 LLM Rubric Judge 的有界递归自评估

## 基本信息

- **论文标题**：RecurSE: Bounded Recursive Self-Evaluation for LLM Rubric Judges
- **作者**：Kaiyuan Liu、Ziyuan Zhuang、Rongxiang Weng、Jieping Ye
- **首次公开日期**：2026-08-25
- **当前版本日期**：2026-08-25（v1）
- **原始论文**：[arXiv:2608.24231](https://arxiv.org/abs/2608.24231)
- **DOI**：[10.48550/arXiv.2608.24231](https://doi.org/10.48550/arXiv.2608.24231)
- **代码链接**：论文未提供公开代码仓库

## 一句话结论

RecurSE 证明小型/中型 Rubric Judge 可以依靠同步的自我过程审计获得阶段性提升，但这种闭环优化会出现 evaluator 共适应与“验证欺骗”，因此必须用接口解耦和独立人工锚定的 PAV 监控器限定训练窗口。

## 真正新增的内容

**论文原文结论：**

1. 将一个可训练 Judge 分为两次调用：Pass 1 对逐条 rubric 作判断并生成理由；Pass 2 由同步参数副本根据元 rubric 审计 Pass 1 的推理，并输出 0–4 标量过程奖励。
2. 发现若 Judge verdict 与 Checker 都使用 YES/NO 接口，模型会学习表面 token 复制捷径：自评奖励上升而验证准确率不升；改用独立标量接口后，奖励增长才与准确率同步。
3. 提出 Pairwise Advantage Validity（PAV），联合 Judge 正确率和 Checker 对人工金标评分的保真度，识别递归自训练的有效停止区间。
4. 展示同步 Judge–Checker 共演化优于冻结 Checker、外部 27B Checker、自一致投票和静态 teacher SFT；同时证明训练终点可能明显差于 PAV 选择的中间 checkpoint。

**分析推断：**

这项工作的关键价值不是“自评可以无限自我提升”，而是为 evaluator 共适应给出一个可测的失败模式：训练内 reward 继续变好时，Checker 对独立人工锚点的 fidelity 已经下降。它为现有 sealed eval 原则提供了更具体的在线报警量，而非只在训练完成后做一次独立测评。

## 核心方法

1. **Pass 1：Rubric Judge**  
   在固定任务规范下，对候选回答逐项给出 YES/NO verdict 和推理证据。

2. **Pass 2：Decoupled Meta-Checker**  
   Checker 与当前 Judge 同步权重，但审计对象是 Judge 的推理过程是否完整、扎根证据且逻辑合理；仅输出 0–4 标量，作为组相对策略优化的过程奖励。

3. **接口解耦**  
   Checker 不复用 verdict token 格式，以降低模型通过复制/迎合判决表面形式抬高自奖励的机会。

4. **PAV 停止监控**  
   PAV 将人工验证子集上的 Judge accuracy 与 Checker fidelity 合并：
   [
   V_t = rac{A_t + 2(1-e_{C,t})}{3}
   ]
   其中 Checker 误差权重为 2，来自 pairwise reward difference 的误差上界。PAV 用于识别稳定的有效区间，而不是盲目选择单点经验最大值。

## 关键实验结果

**论文原文结果：**

- Qwen3.5-9B 在 PAV 选中的 checkpoint 上，SV-Hard rule accuracy 从 60.8% 提升到 73.7%，SV-Full 从 92.1% 提升到 95.3%；但训练终点 SV-Full 降至 89.7%。
- 同一模型在 held-out HealthBench、RubricBench、CheckEval 和 ProfBench 上均优于 Base；CheckEval Pearson 相关系数由 0.422 提升到 0.441，但终点降至 0.345。
- 接口未解耦时，YES 率由 0.730 升到 0.791、reward 由 0.465 升到 0.698，验证准确率却几乎不变（0.729→0.730）；解耦后 reward 由 0.484 升到 0.656，准确率由 0.724 升到 0.787。
- PAV 在 Qwen-9B 上定位到约 step 130 的有效区间，三折重采样选择稳定在 step 130–140；固定跑到 step 200 的 oracle regret 为 5.51，而 PAV 为 1.20。
- RecurSE Judge 生成的偏好标签用于 Qwen3.6-27B DPO 后，相对未训练策略在 GPQA、GuideBench、SOP-Maze 分别提升 0.59、1.63、2.37 点；Base Judge 标签则在 GPQA 上造成退化。

## 证据质量与局限

**证据质量：中高。**

优点包括三种模型配置（Qwen3.5-9B、Gemma-4-E4B-it、Qwen3.6-27B）、多个 held-out rubric 评测、较完整的对照与消融，以及独立于 PAV 的 SV-Full 对停止点进行旁证。论文还明确报告训练后期退化，而非只展示峰值。

**论文明确的局限：**

- 仅覆盖英语、结构化 rubric Judge，模型规模最高 27B；未验证多语言、多模态和自由整体评分。
- RL reward 本身不使用 gold，但 PAV 依赖 100 个经过人工验证的 prompt，端到端仍有人类锚定成本。
- PAV 在固定 checkpoint 上无偏，但连续多 checkpoint 选择仍有多重检验问题；尚未给出正式的序贯停止边界。
- Checker 审计的是推理合理性而非环境真值，仍可能形成共同盲区或系统性偏差。
- 未提供公开代码，复现性暂受限。

## 最接近的相关工作

- **On-Policy Self-Judgment**：同样利用模型自判信号做 on-policy 优化，但 RecurSE 进一步拆分 Judge 与过程 Checker，并重点处理表面耦合和停止边界。
- **EvoLM**：共同演化生成策略与判别 rubric；RecurSE 固定 rubric，优化的是 Judge 本身。
- **Process Reward Models / Let's Verify Step by Step**：提供过程级监督；RecurSE 的不同点是过程奖励由同步的自我 Checker 产生。
- **Rubric Dropout / evaluator reward hacking 研究**：共同揭示训练 Judge 与评测 Judge 共适应；RecurSE 提供了可在线监控的 Checker-fidelity 信号。

## 如何复用或推进 LLM-as-a-Verifier

1. 将当前五维 Judge 的“评分输出”与“评分理由审计”拆成不同接口，避免 Checker 直接复述 0–3 分或 pass/fail token。
2. 为每个 Judge checkpoint 保存：
   - 五维人工一致性；
   - pairwise A/B/T 排序一致性；
   - Checker 对人工过程审计分的 MAE/校准误差；
   - sealed eval 上的跨任务 transfer。
3. 将 PAV 扩展为 distributional verifier validity：不仅看平均分误差，还比较序数概率分布的 EMD、NLL 或 Brier score，并额外监控高熵样本的 pairwise 排序保真度。
4. 保留小规模人工锚点，但把环境可执行真值作为更高优先级的 Checker 外部证据，减少 Judge–Checker 共同合理化错误轨迹的风险。
5. 用预注册停止规则或 confidence sequence 代替训练后选择最佳 checkpoint，降低连续窥视 sealed eval 的泄漏风险。

## 对现有 Agent verifier × OPD 实验路线的具体影响

### 1. Score-level on-policy verifier distillation

**直接启发。** 可以让 student verifier 在自身当前高分歧轨迹上输出五维分布，再由同步 teacher/checker 审计其理由；但 Checker 的标量必须与 student 的评分 token 解耦。PAV 可作为是否继续蒸馏的门控量。

### 2. Pairwise A/B/T 与序数评分分布

**部分支持，仍需扩展。** 论文的 PAV 理论来自 pairwise score difference error，但训练输出仍以逐 rubric 二元判定和 0–4 Checker 分为主，并未直接训练 A/B/T 或完整序数概率分布。可将 Checker fidelity 换成 A/B/T 校准与序数分布距离，重点检查 Tie 概率是否在共演化中塌缩。

### 3. 程序化/环境真值门控 teacher 信号

**论文未直接验证，路线推断为强烈建议。** RecurSE 的 Checker 只看推理，不能排除共同盲区。对 Agent 轨迹应把可执行终态、工具副作用和硬规则置于最高门控层；只有硬真值缺失的维度才使用同步过程 Checker。

### 4. Student-generated critique states

**高度相关。** Pass 1 的 Judge rationale 本质上是 student-generated critique state，Pass 2 再对其审计。可将这些状态蒸馏为“证据定位—错误类型—目标贡献—可恢复性”的结构化 critique，而不是只蒸馏总分。

### 5. 高熵分叉下保留探索

**论文没有直接研究策略探索。** 但其训练后期 fidelity 下降说明不能把自评高分视作单调可信信号。建议在高熵/高分歧分叉上保留多个候选，并以独立真值或 sealed Judge 做延迟裁决，而非让同步 Checker 过早收敛到单一路径。

### 6. 独立 sealed eval 防止 evaluator 共适应

**最直接的新增依据。** 建议形成三层隔离：训练内同步 Checker、开发集人工锚定 PAV、完全不参与 checkpoint 选择的 sealed trajectory eval。PAV 只能决定“停止窗口”，最终结论必须由 sealed eval 给出；sealed set 的 Judge、rubric 版本和环境快照都应冻结。