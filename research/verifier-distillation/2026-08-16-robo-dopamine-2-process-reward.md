# Robo-Dopamine 2.0：历史条件与 OOD 感知的机器人过程奖励模型

## 基本信息
- **论文标题**：Robo-Dopamine 2.0: History-Conditioned and OOD-Aware Process Reward Modeling for Robotic Manipulation
- **作者**：Yijie Xu, Haopeng Jin, Run Zhou, Shengbang Liu, Sixiang Chen, Hongyang Cheng, Sicheng Hu, Peterson Co, Jinwen Luo, Huajie Tan, Shanghang Zhang
- **首次公开日期**：2026-08-16
- **版本日期**：2026-08-16（v1）
- **原始论文**：https://arxiv.org/abs/2608.15680
- **DOI**：10.48550/arXiv.2608.15680
- **代码**：未在 arXiv 页面发现公开链接

## 一句话结论
Robo-Dopamine 2.0 用历史条件化的 pairwise reward 和带正负号的 progress space 区分有效进展、鲁棒变体、失败与恢复，直接对应长时程 Agent 的 A/B/T、序数轨迹评分和“暂时回撤不等于无价值”。

## 真正新增的内容
**论文原文**：静态 before/after 奖励在 OOD 执行中有时间歧义。新模型根据 query 类型使用同 episode 专家历史、在线 rollout 历史或 source-aligned 成功参考面板，并保持被比较端点不变；Signed-Hop curriculum 先学粗顺序，再校准细粒度进度。

**分析推断**：文本 Agent 可把视频帧换成状态/工具调用片段，用 source-aligned reference trajectory 为高熵分叉提供可比上下文；signed recovery 类别比单调 progress score 更适合可恢复性建模。

## 核心方法
GRM 接收任务、起终锚点、有序历史与一对状态，预测 signed relative progress。训练空间显式包含 progress、robustness-preserving variation、failure、recovery；transition-aware replay 复习跨阶段跳跃。

## 关键实验结果
参考面板使 mean VOC 从 0.967 升至 0.986，OOD-robust VOC 从 0.906 升至 0.958。同为 400K pairwise reward 预算，25% replay 的 Signed-Hop 达 0.9872 mean VOC，匹配池 shuffled control 为 0.9858。下游 RL 达到 86.8% RoboTwin 平均成功率，真实插入任务 71/80 成功。

## 证据质量与局限
优点是含 OOD 数据、五类 benchmark、静态/历史对照、固定预算 curriculum 控制和仿真/真实机器人 downstream RL。局限是视觉机器人域、VOC 是内部排序指标、部分提升绝对值较小；历史/参考面板可能泄露阶段信息；未展示跨任务 sealed judge 或文本 Agent 泛化。

## 最接近的相关工作
visual reward model、pairwise preference learning、process reward model、PRM-as-a-Judge 1.5、VICtoR、failure/recovery modeling、distributional value。

## 如何复用或推进 LLM-as-a-Verifier
把轨迹对按同任务、同起点和相似历史对齐，预测 A 更进展/B 更进展/Tie，并扩展为 progress/robust/failure/recovery 序数分布。程序化环境真值用于锚定 endpoint 与 recovery。

## 对 Agent verifier × OPD 路线的影响
1. **score-level**：蒸馏 signed progress distribution，不只终局分数。
2. **A/B/T**：同源参考面板降低比较歧义；Tie 对应等进度或鲁棒等价。
3. **真值门控**：固定端点并校验环境状态，防止上下文改变结果。
4. **critique states**：在回撤与恢复节点生成 critique/恢复建议。
5. **探索**：把 recovery 单独建模，高熵回撤分支不立即剪枝。
6. **sealed eval**：隐藏任务、参考轨迹和环境种子，单独评估 OOD recovery。

## 结论边界
论文强支持历史和 signed progress 改善机器人过程奖励，但迁移到语言 Agent 仍需新数据与独立校准。
