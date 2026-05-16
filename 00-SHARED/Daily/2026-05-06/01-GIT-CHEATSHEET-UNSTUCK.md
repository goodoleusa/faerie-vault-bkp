# Git Cheatsheet — Common One-Liners to Get Unstuck

## Status & Inspection

1. **See what changed (all branches)**
   ```bash
   git status
   ```

2. **See diff of unstaged changes**
   ```bash
   git diff
   ```

3. **See diff of staged changes**
   ```bash
   git diff --cached
   ```

4. **See last N commits**
   ```bash
   git log --oneline -10
   ```

5. **See commits only on current branch (not on main)**
   ```bash
   git log --oneline main..HEAD
   ```

## Undo & Recover

6. **Discard all unstaged changes (DESTRUCTIVE)**
   ```bash
   git restore .
   ```

7. **Unstage a file**
   ```bash
   git restore --staged <file>
   ```

8. **Undo last commit but keep changes staged**
   ```bash
   git reset --soft HEAD~1
   ```

9. **Undo last commit and discard changes (DESTRUCTIVE)**
   ```bash
   git reset --hard HEAD~1
   ```

10. **Recover a deleted branch (if you still have its hash)**
    ```bash
    git checkout -b <branch-name> <commit-hash>
    ```

## Branches & Remotes

11. **List all branches (local + remote)**
    ```bash
    git branch -a
    ```

12. **Switch to a branch**
    ```bash
    git checkout <branch-name>
    ```

13. **Create and switch to new branch**
    ```bash
    git checkout -b <new-branch>
    ```

14. **Delete a local branch**
    ```bash
    git branch -D <branch-name>
    ```

15. **Rename current branch**
    ```bash
    git branch -m <new-name>
    ```

16. **See which remote each branch tracks**
    ```bash
    git branch -vv
    ```

17. **Change upstream (tracking) branch**
    ```bash
    git branch -u origin/<branch>
    ```

18. **Fetch latest from remote without pulling**
    ```bash
    git fetch origin
    ```

19. **Push to remote (create if not exists)**
    ```bash
    git push -u origin <branch>
    ```

20. **Delete remote branch**
    ```bash
    git push origin --delete <branch>
    ```

## Merge & Rebase

21. **Merge another branch into current**
    ```bash
    git merge <other-branch>
    ```

22. **Abort a merge (if conflicts exist)**
    ```bash
    git merge --abort
    ```

23. **Rebase current branch onto main (REWRITING)**
    ```bash
    git rebase main
    ```

24. **Abort a rebase**
    ```bash
    git rebase --abort
    ```

## Stash (Temporary Storage)

25. **Save work without committing**
    ```bash
    git stash
    ```

26. **List all stashes**
    ```bash
    git stash list
    ```

27. **Restore latest stash**
    ```bash
    git stash pop
    ```

28. **Restore specific stash**
    ```bash
    git stash apply stash@{N}
    ```

## Cherry-Pick & Reset

29. **Copy a commit from another branch**
    ```bash
    git cherry-pick <commit-hash>
    ```

30. **Move back to previous stable state (HARD - DESTRUCTIVE)**
    ```bash
    git reset --hard <commit-hash>
    ```

## Remotes

31. **List all remotes**
    ```bash
    git remote -v
    ```

32. **Rename a remote**
    ```bash
    git remote rename <old-name> <new-name>
    ```

33. **Remove a remote**
    ```bash
    git remote remove <name>
    ```

34. **Add a new remote**
    ```bash
    git remote add <name> <url>
    ```

## Search & Find

35. **Find which branch contains a commit**
    ```bash
    git branch --contains <commit-hash>
    ```

36. **Search commit messages for a keyword**
    ```bash
    git log --grep="keyword" --oneline
    ```

37. **Search file content in commits**
    ```bash
    git log -S "text to find" --oneline
    ```

38. **See who changed a line (blame)**
    ```bash
    git blame <file>
    ```

## Lock File Issues

39. **Remove stuck git lock (if git crashed)**
    ```bash
    rm .git/index.lock
    ```

40. **Force garbage collection (free space)**
    ```bash
    git gc --aggressive
    ```

## Pre-Commit Hooks (When Stuck)

41. **Run pre-commit checks manually**
    ```bash
    git pre-commit run --all-files
    ```

42. **Bypass pre-commit hook (NOT RECOMMENDED - use only for emergencies)**
    ```bash
    git commit --no-verify
    ```

---

## Common Scenarios

### "I committed to the wrong branch"
```bash
git reset --soft HEAD~1         # Undo last commit, keep changes staged
git checkout <correct-branch>   # Switch to right branch
git commit -m "message"         # Recommit
```

### "I need to go back to main state"
```bash
git fetch origin main
git reset --hard origin/main
```

### "I see '(no branch)' / detached HEAD"
```bash
git checkout main   # or your intended branch
```

### "My branch is behind main, need to catch up"
```bash
git fetch origin
git rebase origin/main    # or: git merge origin/main
git push -u origin HEAD   # push to remote
```

### "Lots of untracked files, want them gone"
```bash
git clean -fd   # -f = force, -d = directories
```

---

**Last updated:** 2026-05-06 | **Version:** 1.0
