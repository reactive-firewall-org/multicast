# Multicast Project AI Usage Policy

## 1. Purpose and Scope

### 1.1 Rationale :bookmark:

> [!IMPORTANT]
> This policy governs the use of AI tools, particularly CodeRabbitAI, GH Copilot, and
> Codecov-ai-reviewer, within the Multicast project's development workflow. It establishes
> guidelines for responsible AI integration while maintaining the project's security, quality, and
> integrity.

### 1.2 Definitions :book:

* 1.2.A The following acronyms and abbreviations are used throughout this document:
  * **AI** - Artificial Intelligence
  * **CEP** - Convention Enhancement Proposal
  * **CI** - Continuous Integration
  * **CWE** - Common Weakness Enumeration (security vulnerability classification system)
  * **e.g.** - exempli gratia (for example)
  * **GH** - GitHub (as used in "GH Copilot")
  * **GHI** - GitHub Issues
  * **LLM** - Large Language Model
  * **PR** - Pull Request

## 2. AI Role Definitions

### 2.1 Permitted AI Roles :information_desk_person:

* 2.1.A Assistive Code Review:
  * AI may provide feedback on code quality, style compliance, and potential issues.
* 2.1.B Assistive Project-Management Delegation:
  * AI may provide feedback when requested on GitHub issues (GHIs), as well as open new, or comment
    on existing, GHI, to track suggested improvements to the project content.
* 2.1.C Documentation Improvement:
  * AI may suggest improvements to documentation clarity and completeness.
* 2.1.D Test Coverage Analysis:
  * AI may identify areas lacking test coverage.
* 2.1.E Code Generation Assistance:
  * AI may suggest code implementations when requested.

> [!CAUTION]
> However, AI may **NOT** apply changes, nor code suggestions, by themselves, to any protected
> branch (That is reserved for qualified human contributors).

### 2.2 Prohibited AI Roles :no_entry_sign:

* 2.2.A Sole Developer:
  * AI (especially LLM-based AI) is not well suited for innovation; No vibe-coding - the direction
    and development of the project CANNOT meaningfully come from AI.
* 2.2.B Sole Approver:
  * AI approval alone is insufficient for merging any PR.

> [!WARNING]
> Only project admin may sufficiently act as a Sole Approver, and _even_ that is discouraged.

* 2.2.C Security Gatekeeper:
  * AI cannot be the only mechanism for security validation
* 2.2.D Merge Commit Author:
  * AI cannot trigger auto-merge without human verification

## 3. PR Review Process

### 3.1 Required Human Review

* 3.1.A Human Review
  * All PRs MUST receive at least one human review from an authorized maintainer
* 3.1.B Verify or Resolve
  * Human reviews must verify (or conversely reject) the AI's suggestions.
  * Discussions are encouraged in both cases, as humans and AI alike may later consider relevant
    project content in future reviews.
* 3.1.C Very Large PRs
  * For PRs exceeding 99 changed files, at least two human reviews are recommended.

> [!NOTE]
> Currently there is only one core maintainer. Hoping to change this.

* 3.1.D Review Conventions and Instructions
  * The project's code review conventions are currently enumerated in the living document:
    [CEP-4](https://gist.github.com/reactive-firewall/cc041f10aad1d43a5ef15f50a6bbd5a5)
    (convention enhancement proposal no.4)

## 3.2 AI Review Requirements

### 3.2 AI Assisted Code Review

* 3.2.A AI Review Purpose
  * AI reviews are supplementary and do not replace human review
* 3.2.B AI Troubleshooting
  * When AI review is triggered but fails (e.g., due to throttling), the PR must be marked as
    requiring additional attention
  * AI approval comments should not be used to bypass branch protection rules

### 3.3 Large PR Handling

* 3.3.A Less is More
  * PRs with more than 99 changed files should be split into smaller PRs when possible.
  * When splitting is not feasible, PR authors must provide a summary highlighting the most
    critical changes for human reviewers.

## 4. Security Considerations

### 4.1 Verification and Validation

* 4.1.A Review Line-by-Line
  * Absolutely, NO "Vibe-coding" is acceptable for this project. ALL AI-suggestions MUST be
    understood by at least one core maintainer (same as all other reviewed code needs to be).

> [!TIP]
> > Good code is its own best documentation. As you're about to add a comment, ask yourself,
> > "How can I improve the code so that this comment isn't needed?" Improve the code and then
> > document it to make it even clearer.
> ~ Steve McConnell

  * All AI-suggested code changes must be verified by a human maintainer (see § 3.1.B).
* 4.1.B Signed Commits
  * Code signing with different keys for human vs. AI contributions is required.
* 4.1.C Security Assessments
  * AI-suggested security fixes must undergo additional human security review.

### 4.2 Branch Protection

* 4.2.A Stable and master branches must maintain protection rules requiring:
  * Minimum of one human approval
  * Signed commits
  * Passing CI checks
  * Force-pushing to protected branches is prohibited

### 4.3 CWE-655 Mitigation

* 4.3.A dual-approval system
  * The project implements a dual-approval system to help prevent single points of failure.
  * AI approvals are tracked separately from human approvals in the review process. Humans
    must be responsible for the actual merge of pull-requests.
  * Every user (e.g., AI or human) must have a distinct code-signing identity (see § 4.1.B).
  * Only human controlled identities may merge branches, or commit to the default branch directly.

> [!NOTE]
> Historically @dependabot (a simple bot, not a LLM-based AI) had been allowed to merge to the
> default branch; this policy considers such actions in the past to now be violations of § 4.3.A
> because the code-signing identity was not controlled by a human. Fortunately, these changes had
> been limited to improving supply-chain security and required approval from the project admin.

## 5. Implementation and Compliance

### 5.1 Configuration Management

* 5.1.A CoderabbitAI Configuration
  * The `.coderabbit.yaml` file is the source of truth for CodeRabbitAI configuration.
* 5.1.B Dependabot Configuration
  * The `.github/dependabot.yml` file is the source of truth for @dependabot configuration.
* 5.1.C Configuration Updates
  * Changes to these configurations require PR approval from at least one core maintainer.
* 5.1.D Configuration Audits
  * Regular audits of AI configuration will be conducted to ensure alignment with this policy.

### 5.2 Monitoring and Reporting

* 5.2.A Monitoring
  * Periodic audits of PR approvals will verify compliance with this policy.
* 5.2.B Reporting
  * Security incidents related to AI usage must be reported via project security channels.

### 5.3 Developer Training

* 5.3.A Contributors should understand the limitations of AI tools in the review process.
* 5.3.B Clear communication about when and how to utilize AI assistance will be provided.
* 5.3.C New contributors will be directed to this policy as part of onboarding.

## 6. Exceptions

## 6.1 Exceptions to this policy require

* 6.1.A Documented justification.
* 6.1.B Approval from at least two core maintainers.
* 6.1.C Time-limited scope with defined expiration.
* 6.1.D Post-implementation security review.

## 7. Policy Review

### 7.1 This policy will be reviewed

* 7.1.A After any security incident involving AI tools.
* 7.1.B When significant changes to project AI integration are proposed.
