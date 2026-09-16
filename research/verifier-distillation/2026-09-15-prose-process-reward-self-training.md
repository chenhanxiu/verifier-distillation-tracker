# Rewarding Reasoning, Not Answers: Fixing and Bounding Test-Time Reinforcement Learning on Medical QA

## 基本信息
- **方法名**：PROSE（Process Reward Guided Self-Training）
- **作者**：Kailong Fan；Anqi Pu；Yichen Wu；Wanhua Li；Yicong Li；Hanspeter Pfister；Huafeng Liu；Xiang Li；Quanzheng Li；Ning Guo
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.16660
- **代码**：未发现公开代码链接

## 一句话结论
【论文原文】小答案空间会让错误 rollout 在同一伪标签上碰撞并自我强化；PROSE 改用逐步 process reward，并以全轨迹最低步骤分作为奖励，避免均值聚合被局部高分利用。

## 真正新增的内容
【论文原文】论文通过只改变答案空间的控制实验，把 test-time RL 在医疗 QA 的坍缩归因于答案碰撞，而非领域难度。PROSE 用医疗过程奖励模型给每步评分，以 min 聚合形成轨迹 reward，并加入答案格式约束；信号被内化进策略后推理期无需 reward model。

【分析推断】“最低步骤分”是长轨迹硬门槛的直接原型：一个关键错误不能被大量无关正确步骤平均掉。

## 核心方法
1. 在无标签测试集上生成多个 rollout。
2. 不再用多数答案一致作为伪 reward。
3. process reward model 对每个推理步骤评分。
4. 以最小步骤分而非均值作为轨迹奖励。
5. 配合格式约束进行 test-time self-training。

## 关键实验结果
【论文原文】标准做法在医疗多选 QA 上准确率停滞且输出多样性迅速下降；PROSE 无标签适应后显著提升通用 Llama，超过专用医疗模型并接近更大系统，且能迁移到未见数据。均值聚合会出现 proxy reward 饱和而准确率下降，min 聚合是关键。

【证据边界】医疗 QA 的推理步骤是模型生成文本，不等同于可执行 Agent 行动；摘要未给出跨领域或环境反事实验证。

## 证据质量与局限
- 控制答案空间的因果诊断较有说服力，并直接展示 reward hacking。
- min 聚合对单个误判极敏感，可能让长轨迹随长度增加而系统性降分。
- process reward model 的自身校准、训练来源和同源偏差仍是主要风险。

## 最接近的相关工作
Process Reward Models、Hints/Critics/Teachers、Key-Step Supervision、MedSNIP、SIGNBALANCE 和硬门槛 rubric。PROSE 的特色是答案空间碰撞诊断与 min-aggregated process reward。

## 如何复用或推进 LLM-as-a-Verifier
【分析推断】将 min 改为“硬门槛维度取最坏值、软维度取风险敏感分位数”的序数聚合；安全、根据可行性、目标推进出现低分即可 fail，其余维度保留分布而非简单平均。

## 对 Agent verifier × OPD 实验路线的具体影响
【分析推断】
- score-level OPD：关键步骤低分决定梯度方向，非关键步骤仅调幅。
- A/B/T：比较分支的最差关键维度；都满足硬门槛且差异不显著时 Tie。
- 环境真值：工具执行、前置条件和终态检查校准关键步骤标签。
- critique states：只奖励能修复当前最差步骤的 critique。
- 探索：避免所有轨迹因单个不确定低分被清空，可对 verifier 置信区间做保守门控。
- sealed eval：单独监控 min reward、真实成功率、轨迹长度偏差和 reward saturation。