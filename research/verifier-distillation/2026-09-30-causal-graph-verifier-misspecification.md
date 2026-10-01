# Who Verifies the Graph? Misspecification Attacks on Causal Action Verification for Language Agents

- **作者**：Fabio Rovai
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40027
- **代码**：未发现公开代码链接

## 一句话结论

即便 causal verifier 的证书内部完全有效，一条错误因果边也可把 false execution 从 0 推到 15.3% 或 48.9%；安全证书不能替代模型规范审计。

## 真正新增的内容

【论文原文】只篡改 committed action-state graph，不改 verifier 算法：漏掉一条双向边时 91% 已执行动作有害；反转一个箭头时 false execution 为 48.9% 且无正确执行。有限随机实验 attestation 可恢复零 false execution，但恢复被错拒的价值还需额外审计。

【分析推断】程序化/因果 hard gate 也存在 specification gap；只审计执行动作防 wrongful action，却无法发现 wrongful inaction。

## 核心方法

对 causal action verifier 做结构错设攻击；用 bounded randomized sample 对 observational certificate 做实验性 attestation，并分别核算执行与拒绝的审计成本。

## 关键实验结果

【论文原文】漏边攻击在公开混杂强度下 false execution 15.3%，utility 从 +2.27 降到 +0.35；反向箭头产生 48.9% false execution。真实图上 555 次执行仅 2 次误报；恢复安全需每 1,050 动作做 127 次实验，恢复全部价值再需 614 次。

## 证据质量与局限

因果干预清晰、数值完整，但为单一 verifier/benchmark 红队案例；攻击者假设能影响图规范，外推到其他环境仍需验证。

## 最接近的相关工作

Executable-Contract Audit、MAGS、GCAC、Reality Is the Final Verifier、Proof-Carrying Cognition。

## 如何复用或推进 LLM-as-a-Verifier

给每个硬门控证书增加“规范来源、可证伪试验、拒绝审计”三项；独立 verifier 同时采样已放行和已拒绝动作。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：证书只决定候选可信度，错设风险应降低而非放大权重。
- **A/B/T 与序数分布**：规范未经 attestation 时输出 T/INVALID。
- **硬真值门控**：必须验证生成真值的图与契约，而不只验证推理过程。
- **student-generated critique states**：critique 引用因果图时需记录具体边和反证。
- **高熵分叉**：同时抽查放行与拒绝，避免安全策略因错拒而探索坍缩。
- **sealed eval**：sealed audit 包含隐藏图错设、执行与不执行两类代价。
