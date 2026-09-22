# MAWILE：同时审计 Judge、Rubric、输入与输出的多轴工作台

- 论文标题：MAWILE: Multi-Axis Workbench for Inspecting LLM Evaluators
- 作者：Jackson Hassell；Farima Fatahi Bayat；Pouya Pezeshkpour；Estevam Hruschka
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.22599
- DOI：https://doi.org/10.48550/arXiv.2609.22599
- 代码：https://github.com/megagonlabs/mawile-judge

## 一句话结论

MAWILE 用经过独立验证的“不应变/应变”扰动同时压力测试 Judge prompt、rubric、Agent 输入和输出，可直接作为序数与 pairwise verifier 上线前的元评测层。

## 真正新增的内容

- 【论文原文】把 Judge 配置视为完整测量仪器，统一审计 prompt、rubric、target input 和 target output 四个表面。
- 【论文原文】每个扰动显式声明预期关系：语义保持时 verdict 应不变，真实质量下降时 verdict 应按方向变化。
- 【论文原文】支持 binary、ordinal、scalar、pairwise 和 structured verdict；即使没有 gold label，也能测 repeat noise 与 invariant flip risk。

## 核心方法

1. 用户冻结 Judge 模型、提示、rubric、解码参数和输出 schema。
2. 生成规则型或 LLM 型扰动，包括位置交换、rubric 重排、输入释义、输出格式/长度/语气变化，以及遗漏义务、事实矛盾、过度拒绝等定向退化。
3. 独立 validator 检查语义保持或退化是否成立；未通过的变体不得进入 Judge 执行。
4. 重复执行并报告准确率、重复翻转率、不变量翻转率、退化检出率以及高风险样本。

## 关键实验结果

- 【论文原文】MT-Bench 演示中，rubric 重排造成 15.9% 的不变量翻转，而未修改样本的基线翻转仅 4.0%。
- 【论文原文】MT-Bench 上 Gemma 3 4B 的 invariant flip 为 2.4%–2.8%，GPT-5.6 Luna 为 5.7%–6.0%，DeepSeek-V4-Flash 为 11.7%–12.2%；但在 Search Arena/GSM8K 上排序发生变化。
- 【论文原文】Search Arena 中 Gemma 的重复翻转仅 0.3%–0.4%，语义保持扰动后却达到 13.8%–16.0%，说明可复现并不等于稳健。
- 【论文原文】更换扰动生成模型对 invariant flip 的平均影响仅 0.5 个百分点，但对退化检出率影响达 7.5 个百分点。

## 证据质量与局限

- 证据中等偏强：代码公开，覆盖多种 verdict 协议、多个数据集和 Judge，并对扰动进行独立准入验证。
- 论文明确指出 MAWILE 测的是敏感性而非正确性；一个稳定 Judge 仍可能稳定执行错误 rubric。无 gold 的审计不能认证 validity。
- LLM 生成与验证扰动仍可能同源共错；论文规模主要是标准 QA/对话数据，而非完整长时程工具轨迹。

## 最接近的相关工作

最接近 Judge Reliability Harness、EvalSense、ReWordBench、Beyond Aggregate Scores 和 ImpossibleRubrics；MAWILE 的贡献是把四个评价表面与“应保持/应下降”关系纳入同一可执行工具。

## 如何复用或推进 LLM-as-a-Verifier

- 将现有五维 0–3 Judge 配置直接接入 ordinal 模式，分别测试 rubric 顺序、释义、任务卡片压缩、输出长度和置信措辞变化。
- 对 A/B/T 增加候选位置交换和稳定 candidate ID，防止展示位置改变 preference；对“遗漏目标、错误工具结果、过度拒绝”建立定向退化探针。
- 将 validator 与 Judge 分属不同模型家族，并用程序/环境断言验证可自动检查的扰动。

## 对现有 Agent verifier × OPD 路线的具体影响

- 【分析推断】只有通过 invariant robustness 与 directional sensitivity 双门槛的 teacher 信号才进入 OPD；翻转样本应降权或标成 T/不确定，而非硬 A/B。
- 【分析推断】可把扰动前后的完整评分分布用于训练 distributional verifier，使 student 学到哪些变化不应移动分数、哪些变化必须降分。
- 【分析推断】MAWILE 适合训练期持续回归；最终 sealed eval 仍需冻结扰动集、validator 和模型快照，并加入环境真值，避免审计器与 Judge 一起适应。
