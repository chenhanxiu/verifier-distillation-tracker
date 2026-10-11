# DreamTrue: Action-Faithful Robot World Model with Counterfactual Post-Training

- **作者**：Junyan Li；Ruizhi Li；Yu Liu；Xiangshuo Liu；Mingchao Sun；Hongyu Pan；Mu Xu；Lue Fan；Zhaoxiang Zhang
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12468
- **Canonical URL**：https://arxiv.org/abs/2610.12468
- **项目页**：https://brave-eai.github.io/DreamTrue
- **代码**：https://github.com/brave-eai/DreamTrue

## 一句话结论

DreamTrue 用反事实动作扩展失败交互覆盖，并以人类标注缺陷训练 embodied video reward model 来优化世界模型，使交互缺陷率从 48.12% 降至 6.25%；它为长时程 Agent 提供了“先预测可观察后果、再由专门 verifier 评分”的闭环原型。

## 真正新增的内容

【论文原文】现有机器人数据既有标定误差导致动作条件不准，又严重偏向成功轨迹。DreamTrue 将跨 embodiment 的动作轨迹渲染到图像空间并做离线几何校准；随后修改历史动作与接触条件生成反事实未来，再用人类标注的机器人、物体和交互缺陷数据训练 embodied video reward model，以该分数做 RL post-training。

【分析推断】这把“世界模型”和“verifier”明确分层：世界模型生成候选后果，reward model 评价物理可信度。它与现有 Agent verifier 路线的关键契合点是，语言 Judge 不再凭文字猜测后果，而是评价可视化/可执行的预测结果。

## 核心方法

1. 将不同机器人 embodiment 的动作轨迹投影为统一的图像空间条件。
2. 用离线几何校准修正动作条件与目标视频之间的错位。
3. 对记录动作、接触方式和未来轨迹做反事实修改，扩大失败和边界交互覆盖。
4. 构建带人类缺陷标注的视频数据集，训练 embodied video reward model。
5. 以 reward model 分数对世界模型进行强化学习后训练，提高动作忠实度与物理合理性。

## 关键实验结果

【论文原文】DreamTrue 在 AgiBot 上达到当时最优的 action following 表现；人类评估的 interaction defect rate 从 48.12% 降至 6.25%，并在 AgiBot World Challenge 2026 的 world model 赛道排名第一。

## 证据质量与局限

【论文原文】包含跨 embodiment 建模、人类缺陷标注、反事实后训练和赛事结果，且缺陷率改善幅度较大。  
【局限】reward model 主要评价可见物理缺陷，不等价于真实任务成功、安全或长期因果正确；它也由人类标签训练，可能继承观察盲区。由生成视频而非真实执行得到的反事实结果仍有 model bias，不能直接作为环境真值。

## 最接近的相关工作

最接近 HaWMPO、FARM、CriticHack、RoboRef、FailBench、OPD-Aha 和 Code Owns the Simulation, Jev Owns the Evaluation。区别在于 DreamTrue 联合使用反事实未来生成和专门的视频 reward model 来修正世界模型本身。

## 如何复用或推进 LLM-as-a-Verifier

对工具型 Agent 可迁移成“后果模型＋结果 verifier”两层：先根据候选动作生成结构化状态 diff、页面变化或工具返回，再由分布式 verifier 评价目标推进、违规、可恢复性与预测可信度。真实环境执行到达后，用预测—现实残差持续校准 verifier；绝不能让生成的未来自证正确。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：将后果可信度、目标达成度和安全风险拆成独立 score head，避免物理逼真分数吞并任务正确性。
- **A/B/T 与序数分布**：对多个反事实未来比较 A/B；世界模型不确定或多模态未来分歧时保留 T 与完整序数分布。
- **程序化/环境真值门控**：真实执行结果决定监督方向，视频 reward 只在不可执行或执行昂贵时提供软幅度。
- **student-generated critique states**：critique 必须指向具体预测后果与缺陷帧；真实执行不支持时拒绝写入。
- **高熵分叉**：利用反事实动作生成覆盖失败和边界接触，而不是只学习成功轨迹；按 verifier 不确定性分配真实执行预算。
- **sealed eval**：冻结独立 reward model，并以未参与训练的真实机器人执行和人工缺陷审计验收，防止世界模型与 evaluator 共同迎合视觉伪特征。

总体判断：【分析推断】DreamTrue 不是 LLM OPD 论文，但它提供了可直接迁移的 verifier 架构：生成式世界模型负责展开后果，独立 reward model负责评分，真实环境负责最终结算。