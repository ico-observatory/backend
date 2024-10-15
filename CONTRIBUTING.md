# Contributing

- All contributions should be made branching from `development`

## On a new feature implementation

1. /Create your feature branch: `git checkout -b features/implementationName`
2. Commit your changes: `git commit -m 'Add some feature'`
3. Push to remote: `git push origin features/implementationName`
4. Create a pull request on [GitHub](https://github.com/ComputerNetworks-UFRGS/ico-backend/pulls) with your branch name, using the base branch `main`.
  - If you are not finished with your implementation, prepend [WIP] to your PR name.
  - Assign reviewers to your PR and assign it to self.
  - Describe your implementation for the reviewer.
5. Wait for reviews. If no changes are needed, including file conflicts, you can safely merge your pull request to the base branch.

**After your pull request is merged**, you can safely delete your branch.

## Pull Request Labels

When submitting a Pull Request, please assign a label according to the type of change the PR makes.
The available options are:
- **PR-bugfix**: Pull Request contains a bug fix.
- **PR-build**: Pull Request contains changes related to the build process or CI/CD pipeline.
- **PR-documentation**: Pull Request contains changes to documentation and/or README.
- **PR-feature**: Pull Request contains a new feature.
- **PR-refactoring**: Pull Request contains refactoring.
- **PR-upgrade**: Pull Request contains dependency upgrades.
- **PR-hotfix**: Pull Requests is a hotfix, directly to production.

Changelogs are updated via the use of [pr-log](https://github.com/lo1tuma/pr-log), using the command `pr-log *version*`.

The --sloppy command is required if not running on the master branch.

[GH_TOKEN environment variable](https://github.com/settings/tokens) needs to be defined, due to pr-log needing to access GitHub private repositores.

## Coding guidelines
For any doubts regarding the styleguide enforced the Pylint, please check the [pyguide.md](PYGUIDE.md).


_More TBD_
