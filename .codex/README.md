# Blog Codex Automation

These prompt files are for the `k4nul.github.io` blog repository only. They are separate from `/home/k4nul/git/automation-projects` and its 20-minute automation rotation.

## Prompt Files

- `daily-prompt.txt`: daily lane
- `weekly-prompt.txt`: weekly lane
- `monthly-prompt.txt`: monthly lane

## Schedule

Cron uses the host timezone. The current host timezone is KST.

```cron
0 9 * * * /home/k4nul/codex/run-k4nul-blog-prompt.sh daily
0 11 * * 0 /home/k4nul/codex/run-k4nul-blog-prompt.sh weekly
0 1 1 * * /home/k4nul/codex/run-k4nul-blog-prompt.sh monthly
```

## Activation

The daily, weekly, and monthly lanes are active. Each prompt must keep the hard boundary that work is limited to `/home/k4nul/git/k4nul.github.io`.

The runner also records sibling repository status before and after each run. If another repository under `/home/k4nul/git` changes during a blog lane run, the runner treats the lane as failed so the change can be inspected.

After a successful lane run, the runner commits repository changes immediately when the blog repository was clean at the start of the run. It does not push. If the repository already had local changes before the lane started, auto-commit is skipped so unrelated user work is not mixed into an automation commit.

## Local Rules

Each lane must follow repository rules in `AGENTS.md`. Post edits must also follow `_posts/AGENTS.md`, `docs/blog-style.md`, and `templates/post-template.md`. Channel derivative posts must follow `doc/channel-posting/`.
