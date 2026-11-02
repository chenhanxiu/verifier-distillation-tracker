# CRoS：基于打乱推理步骤的因果奖励

- **论文标题**：CRoS: Causality Reward on Scrambled CoTs Improves Accuracy and Reasoning Faithfulness
- **作者**：Xiao Yu, Justin Chih-Yao Chen, Zaid Khan, Hyunji Lee, Mohit Bansal
- **首次公开日期**：2026-10-30
- **版本日期**：2026-10-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.42054
- **DOI**：https://doi.org/10.48550/arXiv.2610.42054
- **代码**：https://github.com/xxiaoyuuuu/CRoS
- **项目页**：https://xxiaoyuuuu.github.io/CRoS-Page/

## 一句话结论

CRoS 在不删除或改写步骤内容的前提下打乱 CoT 顺序，用原答案概率下降构造因果奖励，较 outcome-only 和既有因果奖励同时改善 OOD 准确率、CoT 质量与 faithfulness。

## 真正新增的内容

**论文原文结论**：删除步骤或注入错误会改变信息内容，使“因果性”与“对信息变化的敏感性”混淆；CRoS 只改变步骤顺序，并用冻结 base policy 比较原答案在原序列与打乱序列下的 log-probability。

**分析推断**：这为 student-generated critique states 提供了内容保持的反事实审计：若 critique 的步骤顺序被破坏却不影响 action/verdict，其过程分数不应被当作强 teacher 信号。

## 核心方法

将 CoT 按非空行切分为步骤，采样 Kendall (	au) 低于阈值的随机排列。冻结 RL 前策略，计算原答案在原 CoT 和多个打乱 CoT 下的平均 token log-probability差：
[
F(r)=ell(s)-rac{1}{M}sum_j ell(	ilde{s}^{(j)}).
]
该分数作为 outcome reward 的辅助项进入 RLVR。

## 关键实验结果

**论文原文报告**：

- Gemma-3-4B 在五个未见逻辑/游戏数据集上达到 46.8% 准确率，强基线为 43.8%，outcome reward 为 41.8%。
- CoT-Pass@K（K=1…128）平均 43.4%，基线 41.4%。
- hint acknowledgment 为 34.0%，强基线 20.2%。
- 中高难度同域设置也有小幅优势；64 samples 时准确率 88.3%，高于 outcome reward 的 85.4%。

## 证据质量与局限

论文公开代码、checkpoint 与逐题响应，并对多种行为指标做交叉评估，复现条件较好。但只在 Gemma-3-4B 和 Reasoning Gym 的逻辑/游戏任务上验证；按换行切步不等于真实因果单元，顺序打乱也可能产生明显 OOD 文本。答案概率来自同源冻结模型，仍可能继承模型偏差，不能替代环境真值。

## 最接近的相关工作

包括 Early Answering、Adding Mistakes、CIR、SR、ReMUL、CoT faithfulness 与 RLVR。相较仅评估 outcome 或删除/注错的过程奖励，CRoS 的关键区别是内容保持的顺序干预。

## 如何复用或推进 LLM-as-a-Verifier

- 对 Agent critique/计划按依赖单元重排，测量最终 verdict 或动作分布变化，形成 causal-process score。
- 将 CRoS 分数作为序数 verifier 的一个维度，而不是单独决定总奖励；与环境执行结果、约束检查并列。
- 对 A/B/T：只有当原顺序相对打乱版本产生稳定、显著的真值增益时判 A/B，否则输出 T/INCONCLUSIVE。
- 在高熵分叉处避免惩罚自我修正；论文恰表明有缺陷的因果奖励会压缩探索。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析推断**：可新增“顺序因果门控 OPD”：teacher 给出 score-level 目标前，先在冻结 policy 上计算原 critique 与打乱 critique 的答案/动作 log-prob gap；仅在环境真值一致且 gap 通过阈值时提高蒸馏权重。训练集使用 student-generated critiques，sealed eval 则固定扰动生成器、隐藏任务与外部 executor，以避免 student 学会 CRoS 的表面格式。核心消融应比较 outcome-only、删除步骤、注错、随机重排与依赖保持重排。