# Rethinking Cross-Tokenizer On-Policy Distillation: From Alignment Coverage to Supervision Reliability

- 作者：Bingxi Hou、Guochao Jiang、Guofeng Quan、Weiqing Li、Wenfeng Feng、Guohua Liu、Yuewei Zhang
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.08448
- Canonical URL：https://arxiv.org/abs/2610.08448
- 代码：https://anonymous.4open.science/r/Cross-Tokenizer-OPD

## 一句话结论

【论文原文】跨 tokenizer OPD 不应盲目追求监督覆盖率：只在可靠的严格 1:1 对齐位置，对共享词表的 student top-16 做 reverse-KL，已能匹配完整共享词表 OPD，并优于论文比较的跨 tokenizer 基线。

## 真正新增的内容

【论文原文】论文把“对齐覆盖”与“监督可靠性”拆开检验：严格位置已覆盖大多数 student token 且保留近乎全部概率质量；补入 mismatch span 的 MSE 虽实现全覆盖，却降低准确率。梯度诊断显示 span 梯度与严格对齐梯度方向弱一致甚至相反。

## 核心方法

【论文原文】在三个异构 teacher–student 对上测量严格对齐覆盖与共享词表概率质量；在严格位置只保留 student 选出的共享词表 top-16，优化 reverse-KL；再以 span log-prob MSE 扩展到不匹配片段，并比较梯度方向与相对幅度。

## 关键实验结果

【论文原文】数学推理和代码生成上，top-16 严格位置方案与完整共享词表 OPD 准确率相当，并超过所测跨 tokenizer 基线；加入 span MSE 后准确率下降，且训练后期 span 梯度相对严格梯度变大而方向相容性差。摘要未给出统一绝对分数，结论依赖三组模型配对。

## 证据质量与局限

【论文原文】优点是同时报告覆盖、概率质量、性能和梯度诊断，而非只看最终分数。【分析推断】证据仍限于三组模型及数学/代码任务；top-16、严格对齐比例和梯度冲突是否能迁移到长时程工具轨迹、score-level verifier 尚未验证。匿名代码链接也应在正式发布后复核。

## 最接近的相关工作

【分析推断】最接近 Cross-Tokenizer OPD、GVPO++、RouteOPD 与 CompassOPD；区别在于本文的核心不是扩大 token 映射，而是拒绝低可靠覆盖。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】异构 verifier teacher 输出序数分布时，可只蒸馏可证明语义对齐的评分槽位，并用 student top-k 压缩类别支持；对 critique 文本的错位 span 先标为缺失监督，而不是强行 MSE 对齐。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：增加“严格对齐 top-k”基线，并单独记录覆盖率与梯度余弦。
- 【分析推断】A/B/T 与序数分布：只在标签语义和顺序严格匹配时传递完整分布；错位时保留 T。
- 【分析推断】真值门控：环境真值决定方向，跨 tokenizer soft score 只调幅度。
- 【分析推断】critique states：未可靠对齐的 critique span 不进入 student 状态。
- 【分析推断】高熵分叉：不要因追求全覆盖而压平未对齐分支。
- 【分析推断】sealed eval：冻结 tokenizer、映射器与 top-k 规则，独立评估对齐错误和最终任务表现。