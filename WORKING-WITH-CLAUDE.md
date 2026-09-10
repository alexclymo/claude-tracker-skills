# Working with Claude Code on academic work

**Author:** Alex Clymo

These are notes from using Claude Code on my own research over the last several months, mostly
quantitative macro and heterogeneous-agent work. They are here to set honest expectations about what
the tracker system in this repo is for, and what it is not for.

The short version: the agent is a confusingly brilliant research assistant. It is better than you at
a lot of maths and at almost all coding. It is worse than you at economics. It is very overconfident
at times, and blazingly fast at getting things done. Nearly everything below follows from that one
asymmetry.

What this system is emphatically *not* for is one-shotting or vibe-coding academic work. Agents are
not good enough at frontier economics for you to get away with that. The point of the tracker is to
let the agent work more autonomously while you stay firmly in the steering seat — not to let you
leave the seat.

## Where the asymmetry bites

**Writing.** The agent is now genuinely good at writing up a result, once the result is clear, and
it is very good at dealing with TeX. What it is bad at is deciding what an interesting result *is*.
It will happily try to present navel-gazing or internal progress as a finding: "we tried this and it
failed" is useful for us and does not belong in the paper. Judging what goes in is your job, and it
does not seem to be getting easier to delegate. (The usual complaints about AI writing style apply
too.)

This document is a case in point. As you can probably tell, it was written entirely by Claude — but
after an interview session with me, where it asked good questions and I gave it all the content. It
organised that content better than my scrambled thoughts had, and I have to say the writing feels
pretty good to me.

**Coding versus economics.** Ask the agent to code a standard model and it is no problem. Ask it to
port your code from one project to a similar project, even with complex differences, and that is no
problem either. Ask it to work on a non-standard or new model and you need to be very careful. It is
bad at calibration and does not understand the art of it, because calibration is not a clear,
rules-based science. It does not have a feel for the subtle art of solving messy heterogeneous-agent
problems. It codes them beautifully and has bad economic intuitions about them, which leads to
strange decisions.

One very good use case I have found looks like this: we have code that works but is slow, so try a
bunch of things to make this model converge faster, use trial runs to learn, and make informed
decisions from what you find. That is a list of options you could have worked through in the
pre-agentic world. The difference is that the agent holds the reins, reasons about each result, and
gets through the list far faster than you would have.

That is the middle of the range. At the smaller end, we all know that agents are great for quickly
making a bunch of fiddly edits that would have been tedious to do yourself. At the largest end, I
have found that agents help me step out of my comfort zone into new areas of research or new
statistical methods, since they know the basics of most topics well and you can discuss and learn
with them as you go.

**Bad decisions the agent does not notice.** This is the one to internalise. In a two-step GMM I was
working on, the first stage was difficult and needed multiple initial guesses to find the global
minimum. The agent ran the full two-step estimation for each initial guess, rather than running the
first step for each guess, taking the best first-step solution, and only then moving on to the second
step. When I asked why, it knew instantly that it was wrong. But it had been happily using the wrong
specification until I checked.

Two lessons. The agent will often spot its own error, but it will not check unless you ask. And you
have to read the code yourself, because a mistake like this looks like perfectly clean output once
it is put into a pretty plot or table in a research document — and Claude is very good at making
those look pretty, regardless of the quality of the underlying work.

## Staying in charge

Read the agent's code. If you will not do that, then at the very least ask it to explain clearly what
it did and show the relevant snippets in the chat. Do not fall into the trap of never checking.

Question the agent, and follow your nose when something seems off. If it writes an answer that is
too complex, ask it to explain more simply. Claude Code often explains what it just did too briefly,
or too densely, to actually follow. You need to stay on top of things, so just ask — ask for a
summary, ask for plainer language, ask again.

Run code reviews using subagents. I do not do this often enough and it always helps.

Ask for code a human can run. Left alone, agents tend to write code that is awkward to run yourself,
which makes it hard to play with the model or verify anything by hand. Ask for either the main code
or the test files to be written so that a human can press play on a script with the options clearly
laid out at the top. That can be a playground script alongside the messier batch code the agent runs
end to end.

## Practical habits

**Use git.** It is highly recommended, and not only as a safety net for you. The agent uses it
naturally — checking past changes, reading diffs, working out what happened when.

**End sessions early.** Watch your context and do not let a session run much past the usual
recommendations of roughly 100k–200k tokens.

**Keep using plan mode and brainstorming.** This system does not replace them, and there is nothing
about having a tracker that means you should stop planning things properly.

**Name the mess.** Tell the agent — in `CLAUDE.md`, so it sticks — that any temporary files it makes
while working on a task should be labelled with a lab naming scheme tied to that task, so an
exploratory script becomes something like `lab_t21_robustness.py`. Agents make a lot of files, and
this is how you keep track of them. Then keep a clear line between lab files and the actual
production pipeline, which should follow an obvious convention of its own — `main1_cali.py`,
`main2_plots.py`. A `PIPELINE.md` or `ARCHITECTURE.md` on top of that helps you and the agent both
stay on top of the codebase.

**Be explicit about unsupervised work.** If you want the agent to go on a long hunt for something,
overnight say, tell it so and give it a clear goal and a time budget. Save this for work you are
genuinely happy to leave alone — long model runs where it is tweaking parameters or settings while
learning about a calibration or a solution method.

## Where the tracker helps, and where it can hurt

There are two big points, and they pull in opposite directions.

On the one hand, this system lets the agent work really autonomously, because it stores and edits
the information it needs to work. It genuinely helps you work better with the agent, and it seems to
do so at very little cost. Not having to tell the agent the same things every session is a real
gain.

On the other hand, that same property is how you get led off course. If the tracker documents go
stale, the agent loads bad information instead of good, and it does so silently. The system removes
the friction of re-briefing, and some of that friction was doing useful work.

So steer what gets written. Be specific about what you want recorded as priorities for the next
session, and what you want recorded as results, solutions, and problems in the task detail
documents. Do not be afraid to say "make sure that's all noted with all the context we need to pick
this up again next session." The agent will suggest good things to record, but choosing and steering
is your job. It also often seems happy to move on, where I frequently want another round of making
the code faster or more robust.

One candid note. Earlier versions kept a separate `DECISIONS.md` ledger. In fast-moving projects it
went stale, and the agent filed things there that were not important, or not general enough to still
be true a few sessions later, so v3 retired it. A decision now lives where it was made — a dated
note in the task's detail file — and the rare rule that binds the whole project is a line in
`CLAUDE.md` that you sign off on. Less to maintain, and nothing stale gets loaded every session.
