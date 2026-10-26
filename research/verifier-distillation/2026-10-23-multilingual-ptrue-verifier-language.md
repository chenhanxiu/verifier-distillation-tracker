# 多语言 P(True)：Verifier 指令语言会移动校准

- **论文标题**：Disentangling Question, Response, and Verifier Languages in Multilingual P(True) Self-Evaluation
- **作者**：Jewon Yeom、Jaewon Sok、Seonghyeon Park、Jeongjae Park、Hwiyeong Lee、Taesup Kim
- **首次公开日期**：2026-10-23
- **版本日期**：2026-10-23（v1）
- **原始论文**：https://arxiv.org/abs/2610.32144
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.32144
- **代码**：未发现公开代码链接

## 一句话结论

即使答案固定，仅改变 verifier 指令语言也可把校准误差移动最多 0.04；distributional verifier 的 P(True) 不能跨语言直接比较，必须把问题、回答和 verifier 三种语言分别锁定并校准。

## 真正新增的内容

**论文原文结论**：以六语言全因子设计独立改变 question、response、verifier language，在十个 3B–14B 开源模型、LSQA/MMMLU/TriviaQA 上用首 token P(True) 测自评置信度。

**分析推断**：这是对“序数/概率分布天然可比”的直接反例；语言是 verifier 的测量条件，而不是无关表面变量。

## 核心方法

1. 固定答案，在三种语言角色间做因子化控制。
2. 从 True/False 首 token 概率构造 P(True)。
3. 分别评价 accuracy、discrimination 与 calibration。
4. 用外部 scorer 检查不同语言下结论是否被评价器偏差扭曲。

## 关键实验结果

**论文原文结论**：匹配 response 与 question/verifier language 可增强区分度但不必改善校准；仅 verifier language 就可改变校准误差最多 0.04而不改变准确率。一个未验证 Judge 会把 MMMLU 英语—印地语准确率差从 0.198 错缩到 0.038。

## 证据质量与局限

十模型、六语言、三 benchmark 的受控设计较强；但研究是单轮自评，不是外部长轨迹 verifier。P(True) 只取首 token，受 tokenizer、答案格式和语言词形影响；没有 on-policy 训练与执行真值闭环。

## 最接近的相关工作

接近 Rethinking Verbalized Confidence、The Mirage of Calibrated Confidence、Who Judges Matters、JEV-as-a-Judge 与 multilingual Judge calibration。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier language、rubric language、response language 与 tokenizer 作为校准元数据；对每个组合拟合独立温度或等距回归，并报告完整概率分布而非单一置信度。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：不同语言的 score 先校准再作为幅度，禁止直接混合。
- **A/B/T/序数**：只有同语言协议内可直接排序；跨语言后验重叠则标 T。
- **真值门控**：语言校准不能替代程序化结果。
- **critique states**：保存 critique 原语言与翻译来源，避免翻译后置信度漂移。
- **探索保留**：语言切换造成的高熵不应被当作能力不足。
- **sealed eval**：冻结多语言协议并使用独立人工/硬真值，审计模型排名是否随 verifier language 翻转。
