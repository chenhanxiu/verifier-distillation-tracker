# Beyond Accuracy：程序轨迹如何移动 Overseer 判定阈值

## 元数据

- **论文标题**：Beyond Accuracy: How Procedural Traces Shift the Decision Criterion of LLM Overseers
- **作者**：Zihan Chen、Di Zhu、Lei Zheng、Weiling Li
- **首次公开日期**：2026-09-16
- **版本日期**：2026-09-16（v1）
- **原始论文**：https://arxiv.org/abs/2609.18204
- **代码链接**：未发现公开代码链接
- **状态**：HICSS 录用

## 一句话结论

更详细的程序轨迹不一定让 Judge 更容易被骗，却会让部分 Overseer 更倾向拒绝；长轨迹 verifier 必须同时校准命中率、误报率和判定 criterion。

## 真正新增的内容

**论文原文结论**：在反证始终可见时，五个 LLM overseer 的错误检测接近上限；详细轨迹的主要作用是把判定 criterion 向拒绝方向移动，增加部分模型的 false alarm，而非简单造成“轨迹越详细越轻信”。

**分析推断**：student-generated critique states 和完整轨迹不应默认等价于更多有效证据。训练序数 verifier 时，应将“证据充分性”和“程序复杂度诱发的拒绝倾向”拆成两个头或两个校准变量。

## 核心方法

- 采用信号检测理论分离 discriminability 与 decision criterion。
- 对 19 个合规任务、5 个 LLM overseer，只改变轨迹细节与证据标签。
- 保持反证可见，降低内容变化的混淆。
- 对误报理由进行人工验证编码，分析标签能否消除证据绑定问题。

## 关键实验结果

**论文报告**：共分析 4,551 个判断。无选项标签时，约 60% 的 false alarm 理由是无法把证据绑定到选项；加标签后该理由消失，但易感 overseer 对正确工作的残余拒绝仍随轨迹细节增加。作者因此主张除准确率外报告 criterion 与 false alarm。

## 证据质量与局限

- 优点：受控操纵、信号检测框架、人工验证的理由编码；直接研究 LLM 审 LLM 的程序轨迹。
- 局限：19 个合规任务未覆盖开放式工具环境；没有训练新的 verifier；“反证始终可见”的设置可能高估真实长轨迹中的可观察性。

## 最接近的相关工作

Draft-Verify-Revise 指示语漂移关注 critique 级联中的语义漂移，LLM Judge 遗漏盲区关注义务枚举，MedSNIP 关注过细原子化。本文独特地测量轨迹细节对判定 criterion 的系统位移。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输出从单一分数扩展为：证据支持度、错误检出概率、false-alarm 风险和 criterion。训练时对同一事实构造不同详细度但语义等价的轨迹，要求质量排序不变，并把证据指针显式绑定到 action/observation。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：不要把详细 critique 造成的低分直接当能力退化；先校准 criterion shift。
- **A/B/T**：A/B 共享事实、只改变轨迹冗长度；若排序翻转则标为 evaluator instability/T。
- **真值门控**：可执行真值决定对错，Judge 负责不可程序化维度。
- **critique states**：要求每条 critique 带可解析证据指针，避免“细节更多=风险更高”。
- **高熵探索**：防止保守 Judge 对长分支系统性误杀。
- **sealed eval**：按轨迹长度、证据密度分层报告 false alarm 与 criterion，而非只给总准确率。