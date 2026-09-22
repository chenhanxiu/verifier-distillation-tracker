# IWD：按 Teacher 的跨环境不变性加权蒸馏

- 论文标题：Do Student LLMs Inherit OOD Robustness? Invariance-Weighted Distillation for Reliable Knowledge Transfer
- 作者：Dileesha Kannangara；Sanghamitra Dutta
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.22566
- DOI：https://doi.org/10.48550/arXiv.2609.22566
- 代码：截至 v1 未见公开代码仓库

## 一句话结论

IWD 通过保持语义、扰动伪相关线索的多个合成环境，检验 teacher 输出是否稳定，并只强化跨环境不变的 teacher 信号，为 verifier 蒸馏增加了“先审计 teacher 是否依赖捷径”的样本级门控。

## 真正新增的内容

- 【论文原文】指出标准 KD 的 OOD 退化来自两层叠加：蒸馏数据含伪相关，且 teacher 在不同样本上依赖因果或捷径特征的程度不同。
- 【论文原文】提出用多合成环境下 teacher 预测的不变性估计 causal reliance，并据此连续加权每个蒸馏样本。
- 【论文原文】理论上证明该权重降低 student 梯度的 Spurious-to-Causal 比率，而不是仅做事后数据过滤。

## 核心方法

1. 针对每个样本生成多个保持核心语义、改变表面或伪相关线索的环境变体。
2. 比较 teacher 在原样本和变体上的输出距离；越稳定表示越可能依赖因果特征。
3. 将不变性映射为样本权重，使用加权 KD 更新 student；不同任务采用匹配输出结构的距离度量。
4. 同时让 student 接触全部环境变体，以学习跨环境一致表征。

## 关键实验结果

- 【论文原文】在 MNLI、SQuAD-v2、CoNLL-2003、SST-2 及两个模型家族上，IWD 在 16 个 OOD 设置中的 15 个达到最佳。
- 【论文原文】相对标准 KD，NLI 平均 OOD 提升 4.34 个百分点，QA 提升 14.94 个百分点。
- 【论文原文】MNLI 合成环境数从 3 增到 5 时，HANS 提升 2.14 点；全部变体训练比单变体在 HANS 最多高 4.2 点。
- 【论文原文】有效样本量始终不低于 95%，说明方法主要是平滑重加权而非激进删样本。

## 证据质量与局限

- 证据中等偏强：有理论梯度分析、四任务、两模型家族、多 OOD 集和多随机种子。
- 论文承认合成环境生成成本较高，并仅用输出级距离；token-level 不变性、instruction tuning、Agent 轨迹和 verifier 蒸馏尚未验证。
- 【分析推断】teacher 在扰动下稳定仍可能稳定地错，因此不变性只能作为软置信度，不能替代环境真值。

## 最接近的相关工作

最接近 shortcut learning、反事实数据增强、选择性 KD；与仓库中的 Unified Per-Token OPD Gating、RoboRMBench、TV-Regulated OPD 和 MAWILE 可组合为 teacher 信号审计与加权链路。

## 如何复用或推进 LLM-as-a-Verifier

- 对同一 Agent 状态生成实体重命名、无关信息、格式、工具返回顺序等语义保持变体，计算 Judge 的 score-distribution 距离。
- 将跨变体稳定性作为序数 verifier 的 reliability head，控制 OPD loss 幅度；硬环境结果仍负责决定正负方向。
- 对 critique state 做成对干预：保持事实证据不变时 critique 应稳定，改变关键环境事实时 critique 必须响应。

## 对现有 Agent verifier × OPD 路线的具体影响

- 【分析推断】可把 IWD 权重加入 score-level on-policy verifier distillation：权重由 teacher 跨环境不变性、Judge 共识有效规模与环境真值共同决定。
- 【分析推断】高熵分叉处不应简单丢弃不稳定 teacher 信号；可保留多个分支继续探索，只降低蒸馏力度，等待真实 rollout 结算。
- 【分析推断】sealed eval 应使用未参与生成合成环境的扰动族和模型家族，验证 student 是否真的获得 OOD 稳健性，而非适应固定扰动模板。
