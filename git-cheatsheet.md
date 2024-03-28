### Clone:

```git
git clone [repo url] <folder-name>
```

### Push code:

```git
git add -A # tells git to keep track of all of your edits
git commit -m "[message]" # commit message, commits to local repo
git push origin [branch name] # pushes to github, "remote" repo
```

### Pull code:

(if you didn't make changes yet, pull this before you start coding. Important to avoid merge conflicts.):

```git
git pull
git pull origin [branch]
```

### Switch to an existing branch:

Work on someone else's code:

```git
git checkout [branch name]
```

### Take existing code, make a new branch, put code into it, and switch to that branch:

Do this when you're creating a new feature and/or working at the same time as someone else:

```git
git checkout -b [branch name]
```

If you have existing changes and you wanna pull code:

```git
git stash # saves changes in another place, removes from your code
git pull
git stash pop # restores changes
```

If there are merge conflicts, resolve them in VSCode, or abort the pull, make a new branch, and ask for help.

### If you want to merge to main, but main is ahead of your branch:

```git
git merge origin/main
```
