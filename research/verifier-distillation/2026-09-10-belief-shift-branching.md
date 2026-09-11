# Fork Where the Model Changes Its Mind: Belief-Shift Branching for Tree-Structured Reinforcement Learning

- **作者**：Bin Lei、Yu Li、Prafulla Kumar Choubey、Jiaxin Zhang、Becky Xiangyu Peng、Qinyuan Ye、Kartik Narayan、Caiwen Ding、Silvio Savarese、Chien-Sheng Wu
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.11061
- **DOI**：https://doi.org/10.48550/arXiv.2609.11061
- **代码**：截至记录时未发现公开代码

## 一句话结论

Belief-Shift Branching 用“模型答案信念发生转折的位置”选择分叉点，以约 1%–5% 额外代价逼近昂贵 value-curve 分叉，为高熵分支采样提供了比 token entropy 更语义化的触发器。

## 真正新增的内容

**论文原文结论**：通过黑盒 probe、logit lens 或 learned activation direction 估计答案信念变化，在推理链的 belief pivot 处分叉；其分叉点与 Monte Carlo value curve 更一致，并改善 tree-structured RL。  
**分析推断**：belief shift 可作为 verifier 主动标注预算的触发器，但它衡量“模型改变主意”，不是动作真实贡献，必须用环境 rollout 校验方向。

## 核心方法

沿推理轨迹估计答案信念曲线并检测突变，只在关键 pivot 生成替代后缀。三种读出覆盖纯黑盒到内部激活可用的场景；训练时在这些分叉上构造树状相对优势与可验证奖励。

## 关键实验结果

分叉选择成本约为数学任务 1%、代码任务低于 5%。相对 Monte Carlo value curves，在 8 个 model×benchmark panel 中排名第一，优于 entropy、结构启发式和 LLM Judge。跨三个模型族、两个领域训练：OLMo-3-7B 数学 aggregate 提升 2.6 点、AIME26 提升 2.9 点；代码的 LiveCodeBench-medium 提升 6.5 点。并非处处领先，例如 Nemotron 某设置 midpoint 为 64.5，对方法的 64.0。

## 证据质量与局限

跨模型/领域、含成本与多种定位基线，证据较完整；但 pivot 与因果贡献不是同一概念，内部读出依赖模型访问，黑盒 probe 也会增加调用。个别设置被简单 midpoint 超过，说明触发器具有模型依赖性；尚未覆盖工具副作用和超长环境轨迹。

## 最接近的相关工作

Tree-structured RL、step-level branching、entropy-based sampling、process reward/value models、COTA/ParallelWorld 的同前缀分支比较、EDGE/PGPO 的反事实信用分配。

## 如何复用或推进 LLM-as-a-Verifier

只在 belief shift 高的状态调用强 verifier 与环境回放，生成同前缀 A/B/T；把 shift 大小、rollout reward 分布和 critique 一起蒸馏给小 verifier，使其学习“何时值得验证”。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：belief shift 决定采样位置，执行 advantage 决定符号，序数 verifier 决定梯度幅度。
- **A/B/T**：同 pivot 生成多个后缀；环境结果相同或区间重叠时保留 T。
- **critique states**：要求 student 在 pivot 生成“为何改变计划”的 critique，再用反事实结果筛选。
- **高熵探索**：避免对所有高 token 熵位置分叉；优先保留语义信念突变且 verifier 不确定的分支。
- **sealed eval**：用未参与 pivot 训练的任务和独立 rollout harness 检验定位质量，防止 verifier 学会触发器表面特征。