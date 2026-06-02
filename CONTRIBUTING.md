# Contributing to `networkdiagram`

First off, thank you for considering contributing to `networkdiagram`! It's people like you who make open source such a powerful community. 

We are incredibly excited to be a part of **GirlScript Summer of Code (GSSoC) 2026**! Because this is a live Python package on PyPI, we maintain a high bar for code quality, mathematical accuracy, and testing. To ensure your contributions are valuable and that your PRs are eligible for GSSoC points, please read and strictly follow these guidelines.

---

## 🛑 The Golden Rule: Ask Before You Code

With thousands of contributors looking for issues, we need to prevent duplicate work and ensure efforts align with the project roadmap.

**Do NOT submit a Pull Request without being assigned to an issue first.**

1. Browse the open issues.
2. If you find one you want to work on, comment on it: *"Hi, I am a GSSoC 2026 contributor and I would like to be assigned to this issue."*
3. **Wait** for a Project Admin to formally assign you.
4. Any unsolicited PRs or PRs linked to unassigned issues will be closed immediately without review.

---

## 💻 Local Setup & Installation

To contribute, you'll need to set up a local development environment. 

1. **Fork** the repository using the GitHub UI.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/kathan-majithia/networkdiagram.git
   cd networkdiagram
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install the Package in Editable Mode**:
   This allows you to test your changes without reinstalling the package every time.
   ```bash
   pip install -e .
   ```

---

## 🛠️ Development Workflow

We follow a structured branching model. **Never commit directly to the `main` branch.**

1. Ensure your local `main` branch is up to date with the upstream repository.
2. Create a new branch with a descriptive name indicating the type of work:
   - For new features: `git checkout -b feature/calculate-total-float`
   - For bug fixes: `git checkout -b fix/matplotlib-rendering`
   - For documentation: `git checkout -b docs/readme-update`
3. Write clean, readable Python code.

---

## 🧪 Testing Requirements (CRITICAL)

Because `networkdiagram` calculates critical paths, PERT estimations, and project crashes, **mathematical accuracy is our top priority.**

If your Pull Request adds or modifies any mathematical logic (e.g., PERT calculations, calculating floats, crashing algorithms, etc.), you **MUST** include corresponding unit tests using `pytest`. 

- Tests should verify your code's output against known, manually calculated project networks.
- PRs that introduce mathematical features without passing `pytest` coverage will not be merged.

---

## 📤 Pull Request Rules

When you are ready to submit your code:

1. Push your branch to your forked repository.
2. Open a Pull Request against our `main` branch.
3. **Link the Issue**: In your PR description, explicitly link the issue you were assigned using GitHub keywords (e.g., `Closes #3` or `Fixes #5`).
4. **Visual Changes**: If your PR modifies the `matplotlib` visualization code or the resulting network diagrams, you **must** include "Before" and "After" screenshots in the PR description.
5. Provide a clear summary of the changes you made and any testing steps you took.

---

## 🏆 GSSoC 2026 Points System

We are committed to fairly rewarding high-quality contributions. Please understand how the point system works for this repository:

- **Approval is Required**: A merged PR does *not* automatically give you points. Points are only awarded if a Project Admin reviews the code, merges it, and explicitly adds the `gssoc:approved` label.
- **Scaling Factors**: Your points are scaled based on the labels we assign to your PR:
  - Difficulty (`level:beginner`, `level:advanced`, etc.)
  - Type (`type:feature`, `type:bug`, `type:docs`, etc.)
  - Quality (`quality:clean`, `quality:exceptional`)
- **Zero Tolerance for Spam**: AI-generated code slop, low-effort typo fixes that break things, or spam PRs will be closed, labeled as `gssoc:invalid`, and will receive **zero points**. We value quality over quantity.

Thank you for helping us build a robust, open-source Operations Research tool! Happy coding! 🚀
