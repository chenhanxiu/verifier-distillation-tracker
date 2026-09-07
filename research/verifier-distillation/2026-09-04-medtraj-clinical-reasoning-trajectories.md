# Constructing and Evaluating Clinical Reasoning Trajectories for Medical Agent（MedTraj）

- **作者**：Yunqi Zhu、Wensheng Zhang、Xuebing Yang
- **首次公开日期**：2026-09-04
- **当前版本日期**：2026-09-04（v1）
- **原始论文**：[arXiv:2609.05090](https://arxiv.org/abs/2609.05090)
- **DOI**：[10.48550/arXiv.2609.05090](https://doi.org/10.48550/arXiv.2609.05090)
- **代码/数据**：截至本次记录未发现公开仓库链接

## 一句话结论

MedTraj 把临床推理拆成可评分步骤，用受控错误注入和边际贡献筛选关键步骤，直接启发长轨迹 critique-state 与“下一步动作贡献度”监督，但当前证据高度依赖同源 LLM Judge。

## 真正新增的内容

**论文原文结论**：将轨迹解析为观察、证据、编号步骤和结论，按连贯性、证据支持、幻觉、完整性、可追溯性评分；通过定向错误注入建立故障—质量下降关系，再以步骤边际贡献筛选训练上下文。

**分析推断**：该框架最适合作为 generative verifier 的结构化输出模板和 critique 数据生成器，而非最终真值源；其“边际贡献”应在 Agent 场景用环境反事实重放重新锚定。

## 核心方法

- Qwen3-32B 生成结构化多步临床轨迹，Qwen3-8B 充当多维 Judge；
- 七类受控错误注入生成强/弱轨迹；
- 计算每一步对轨迹价值的边际贡献并过滤；
- quality-weighted context 同时提供高低质量示例及其分数；
- 比较零样本、QA/轨迹上下文、SFT、自洽和 best-of-N。

## 关键实验结果

**论文报告**：

- 生成 87k 条有效轨迹、349k 个步骤实例。
- Trajectory Context 相对零样本在 CareQA/PubMedQA/CECMed 的 coherence 分别提升 0.029/0.041/0.039，evidence 提升 0.020/0.051/0.075。
- CECMed 中 correctness 从 0.390 提升到 0.642；摘要报告 quality-weighted context 的 correctness 近乎翻倍、hallucination ratio 降低 87%。
- 聚类中 12.4% 为“连贯但错误”，其幻觉比率 0.425，而高质量组为 0.029；少数步骤承载大部分质量信号，超过四步收益递减。

## 证据质量与局限

**证据质量：中。** 数据规模大，有受控干预、步骤分析和三数据集结果；但主要指标来自 LLM evaluator。

**论文局限**：生成与评估均依赖 Qwen 系列，内部一致的错误可能漏检；缺少临床专家审查；真实错误比合成注入复杂；质量信号尚未用于 RL。

**安全含义（分析）**：医疗场景不能以“更连贯”替代正确性。12.4% 的连贯错误组恰好说明生成式 verifier 必须受外部证据或专家 sealed eval 约束。

## 最接近的相关工作

最接近 PRM/process reward、Key-Step Supervision、DRACO、Legibility is Not Interpretability，以及基于反事实 rollout 的 Agent 步骤信用分配。MedTraj 的优势是结构化多维轨迹与定向错误注入，弱点是缺少环境真值。

## 如何复用或推进 LLM-as-a-Verifier

- 让 generative verifier 同时输出证据引用、步骤贡献、遗漏义务和不确定性，再蒸馏为序数分布。
- 对每个 student-generated critique state 做删除/替换重放；只有真实 outcome 改善才标为正贡献。
- A/B/T 可来自同一 prefix 的正确步骤、注入错误步骤与信息不足步骤，保留 tie/abstain。
- 程序或环境能验证的字段必须拥有否决权；LLM coherence 分数只控制软权重。

## 对 Agent verifier × OPD 实验路线的具体影响

1. 把多维 generative critique 蒸馏为 step-level ordinal heads：进展、证据、风险、可恢复性、置信度。
2. 比较 LLM 边际贡献与环境反事实 advantage，量化“可读性假象”。
3. 高熵分叉优先做受控故障注入与重放，不因轨迹冗长或低表面连贯度直接淘汰。
4. sealed eval 使用专家/程序标注、不同 Judge 家族和自然故障；训练 Judge 不得参与最终裁决。
5. 专门报告“连贯但错误”检出率，作为 verifier × OPD 是否安全推进的门槛。