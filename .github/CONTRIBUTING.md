# Contributing

You are here to help the Python Multicast Project? Awesome, feel welcome and read the following sections in order to know what and how to work on something. If you get stuck at any point you can create a ticket on GitHub.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.


When reporting an issue, please list the version of Python Multicast Library you are using and any relevant information about your software environment (python version, OS type and version, etc). Also avoid vague language like "it doesn't work." Please describe as specifically as you can what behavior you are actually seeing (e.g., an error message? a nil return value?).


For all contributions, please respect the following guidelines:

Each pull request should implement ONE feature or bugfix. If you want to add or fix more than one thing, submit more than one pull request.
- Do not commit changes to files that are irrelevant to your feature or bugfix (e.g., .gitignore).
  <details><summary>Always use git stash instead</summary>

```bash
# remember your starting branch
VCS_BRANCH_NAME=$(${GIT:-git} name-rev --name-only HEAD | cut -d~ -f1-1) ;
git add -p $(git ls-files -m)  # add modified files interactivly
# select ONLY the changes you are working on
git stash push  # stash the intended changes
git add $(git ls-files -m)  # add remaining modified files automaticly
git branch my-idea-untracked  # create a new branch where you are
git switch my-idea-untracked  # switch to the new branch
git commit # commit the unrelated changes on the new branch
git switch ${VCS_BRANCH_NAME}  # change back to the starting branch
git stash pop # unstash the intended changes
```

</details>

- Do not add new external dependencies unless ABSOLUTELY necessary (these could cause Load Errors on certain systems).
- Add new tests for new code if able (otherwise add descriptive pseudo-tests as issues).
- Be willing to accept criticism and work on improving your code; care must be taken not to introduce bugs or vulnerabilities.

## Known Issues and Possible Improvements

For Details on current issues:
- see [Issues](https://github.com/reactive-firewall-org/multicast/issues)

### Triaging tickets
Here is a brief explanation on how I triage incoming tickets to get a better sense of what needs to be done on what end.

> [!NOTE]
> You will need Triage permission on the project in order to do this. You can ask one of the
> core maintainers to give you access.

### Initial triage
When sitting down to do some triaging work, start with the list of untriaged tickets. Consider
all tickets that do not have a label as untriaged. The first step is to categorize the ticket into
one of the following categories and either close the ticket or assign an appropriate label.

#### If the reported issue . . .

##### is not valid

If you think the ticket is invalid comment why you think it is invalid, then close the ticket.
Tickets might be invalid if they were already fixed in the past or it was decided that the proposed
feature will not be implemented because it does not conform with the overall goal of Multicast
Project. Also if you happen to know that the problem was already reported, label the ticket with
Status: duplicate, reference the other ticket that is already addressing the problem and close
the duplicate.

**Examples**:

[This is an issue. (A good starting point for first person to discover)](https://github.com/reactive-firewall-org/multicast/issues/412)


##### does not provide enough information

Add the label question if the reported issue does not contain enough information to decide if
it is valid or not and ask (e.g., by commenting on the ticket) for the required information to move
forward. We will re-triage all tickets that have the label question assigned. If the original
reporter left new information we can try to re-categorize the ticket. If the reporter did not come
back to provide more required information after a long enough time, we will close the ticket
(this should be roughly about two weeks, but can be left open for longer).

**Examples**:

> My builds stopped working. Please help!

 * Ask for a link to the build log and for which version is affected.


##### is a valid enhancement proposal

If the ticket contains an enhancement proposal (e.g., a new feature, an idea to improve an existing
feature, etc.) that aligns with the goals of Multicast, then add the label `Enhancement`. If the
proposal seems valid but requires further discussion between core contributors because there
might be different possibilities on how to implement the enhancement, then also add the
label question.

**Examples**:

>Improve documentation Examples in contribute docs.

> Provide better integration with security feature XYZ

> Refactor module X for better readability (see #387)

> Achieve world domination
_(also needs the label question)_

##### is a valid problem within the code base

If it’s a valid bug, then add the label Bug. Try to reference related issues if you come across any.

**Examples**:

Multicast Library fails to transmit the leter 'x' or 'y' (logs attached)


##### is a question and needs answering

If the ticket contains a question about Multicast messages or the code, then move the question to
the FAQ documentation and add a task to answer the question to the issue (or close if already
answered).

**Examples**:

> My message was seen by two hosts. Why?

> Why are my builds failing?


### Helpful links for triaging

Here is a list of links for contributors that are looking to help triage:

 * [Untriaged issues](https://github.com/reactive-firewall-org/multicast/issues?q=is%3Aissue%20sort%3Acomments-asc%20state%3Aopen%20no%3Alabel): Go and triage them!
 * [Good first issues](https://github.com/reactive-firewall-org/multicast/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22%20sort%3Acomments-asc)
 * [All Open Issues](https://github.com/reactive-firewall-org/multicast/issues)

---
# Reviewing Checklist:

> [!NOTE]
> This is the checklist that I try to go through for every single release.
> If you're wondering why it takes so long for me to complete stable releases, this is why.

---
## General

> [!TIP]
> Ask yourself "Is this change useful to me, or something that I think will benefit others greatly?" before opening the PR.

- [ ] Check for overlap with other PRs.
  > Those PRs are . . . _include a list_.
  * for example
    > ## Included and Superseded PR/MRs
    >
    > * Supersedes . . . _link to pull-request_
    > * Includes and Supersedes _link to pull-request_

  **OR**

  > This will introduce . . . _description of what is changed only by this PR's set of changes_.

- [ ] Check for relevant GHI.
  * For example:
    > - [x] Closes _link to issue_
    > - [ ] Contributes to _link to issue_

 - [ ] Think carefully about the long-term implications of the change.
   - [ ] How will it affect existing projects that are dependent on this?
     * For example:
       > Breaking changes include . . . _include a list of impacts to dependents_

     **OR**
       > This _PR type, ie version|update|patch_ . . . _previous version this can safely upgrade from_.
   - [ ] How will it affect my projects? If this is complicated, do I really want to maintain it forever?
     * For example:
       > - [ ] Opens _link to new issue_
   - [ ] Is there any way it could be implemented as a separate package, for better modularity and flexibility?
       - [ ] yes
         > . . . _plan for how goes here_

         * include the following advisory at the bottom of your plan.
           > 🚧 CAUTION: 🏗️ This is still experimental. ⛔ DO NOT MERGE AS IS. :no_good:

       **OR**
       - [ ] No

---
## Check the Code

- [ ] If it does too much, ask for it to be broken up into smaller PRs.
  * For example:
    > This is too monolithic; please consider breaking this PR into parts.
    >
    > These numerous changes are disjoint; please reorganize into separate, smaller PRs.

- [ ] Does it pass `make test-style` (flake8, etc.)?
  > These changes follow the current project style conventions as tested by `make test-style`.

  **See project `Makefile`.**

  **OR**

  - [ ] Comment on the PR describing style convention violations.
    * Include the following advisory until it is fixed:
      > 🚧 CAUTION: 🏗️ This is still experimental. 🔧 Fix in progress. ⛔ DO NOT MERGE AS IS.

- [ ] Is it consistent?
  > This change follows current project style conventions as tested by `make test-style`.

  **See project `Makefile`.**

  **OR**

  - [ ] Comment on the PR describing style convention violations.
    * Include the following advisory until it is fixed:
      > 🚧 CAUTION: 🏗️ This is still experimental. 🔧 Fix in progress. ⛔ DO NOT MERGE AS IS.

- [ ] Review the changes carefully, line by line. Make sure you understand every single part of every line. Learn whatever you do not know yet.

🗒️ **Take the time to get things right. PRs almost always require additional improvements to meet the bar for quality. Be very strict about quality. This usually takes several commits on top of the original PR.**

---
## Check the Tests

- [ ] Does it have tests for all the changes? If not:
  * Comment on the PR:
    > Can you please add tests for this code to `tests/test_blah.py`?

  **OR**

  - [ ] Write the tests yourself.

- [ ] Do the tests pass for all of the CI tests? If not:
  * Comment on the PR requesting a fix for the regression in CI.

  **OR**

  - [ ] Fix them yourself.

  **AND**

  - Include the following advisory until it is fixed:
    > 🚧 CAUTION: 🏗️ This is still experimental. 🔧 Fix in progress. ⛔ DO NOT MERGE AS IS.

---
## Check the Docs

- [ ] Does it have docs? If not:
  * Comment on the PR:
    > Can you please add docs for this feature to the documentation?

  **OR**

  - [ ] Write the docs yourself.

- [ ] If any new functions/classes are added, do they contain docstrings?

---
## Credit the Authors

- [ ] Add name and URL to documentation for security fixes.
- [ ] Thank them for their hard work.
- [ ] Close Issues.

---
# Release Checklist:

## Release (optional)

> **Decide whether the changes in master make sense as a major, minor, or patch release. Look at the clock. If you're tired, release later when you have time to deal with release problems.**

- [ ] Merge the PR branch. This will close the PR's issue.
- [ ] Close any duplicate or related issues that can now be closed. Write thoughtful comments explaining how the issues were resolved.

## Check the copyright year:

- [ ] Verify it reads:

  > Copyright (c) 2017-2025, _Author_

## Close Issues

- [ ] Merge the PR branch. This will close the PR's issue.
- [ ] Close any duplicate or related issues that can now be closed. Write thoughtful comments explaining how the issues were resolved.

## Release (optional)

- [ ] Decide whether the changes in master make sense as a major, minor, or patch release.
- [ ] Look at the clock. If you're tired, release later when you have time to deal with release problems.
- [ ] Then follow all the steps in [EXAMPLE Release Checklist](link to be created).

---
