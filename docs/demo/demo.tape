# skillskit README demo: the routing gate catching a collision you cannot see by reading.
# Regenerate from the repo root:  vhs docs/demo/demo.tape
#
# Runs against a throwaway copy in /tmp so the demo can break a skill description
# on purpose without ever touching the working tree.

Output docs/demo/demo.gif

Require make
Require python3

Set Shell "bash"
Set FontSize 17
Set Width 1200
Set Height 620
Set Padding 16
Set Theme "GitHub Dark"
Set TypingSpeed 32ms
Set Framerate 16
Set WindowBar Colorful
Set BorderRadius 8

# Setup: copy just enough of the repo for `make evals` into a scratch dir.
# Sleeps matter — Show before the shell has finished leaves the setup on screen.
Hide
Type "export PS1='$ ' REPO=$PWD"
Enter
Sleep 500ms
Type "rm -rf /tmp/skillskit-demo && mkdir -p /tmp/skillskit-demo"
Enter
Sleep 500ms
Type "cp -R $REPO/Makefile $REPO/scripts $REPO/skills /tmp/skillskit-demo/ && cd /tmp/skillskit-demo"
Enter
Sleep 2s
Type "clear"
Enter
Sleep 1s
Show

Type "# every skill's trigger prompts, scored against every description in the repo"
Enter
Sleep 800ms
Type "make evals"
Enter
Sleep 3s

# python3, not sed: BSD sed needs `-i ''` and GNU sed rejects it, so the tape
# would only work on one of them. Hide stops frame capture but leaves the text on
# screen, so clear before Show or the edit shows up in the next frame anyway.
Hide
Type `python3 -c "import pathlib; p=pathlib.Path('skills/create-skill-repo/SKILL.md'); l=p.read_text().split('\n'); l[2]='description: Authors or improves an Agent Skill in this repo via the eval-first workflow - scope one purpose, write trigger evals, draft the body, then validate.'; p.write_text('\n'.join(l))"`
Enter
Sleep 1s
Type "clear"
Enter
Sleep 500ms
Show

Type "# two skills have just been given near-identical descriptions"
Enter
Sleep 800ms
Type "make evals"
Enter
Sleep 4s

Hide
Type "cd / && rm -rf /tmp/skillskit-demo"
Enter
Show
