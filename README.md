# CNCF People Overview

This repo stores the data that will populate the various people listings on cncf.io and control access to repositories in the CNCF GitHub org.

People can update their listing by submitting a PR for approval. After a PR is merged, the CNCF site will reflect the update within 10 min. The listings are:

- [Ambassadors](https://www.cncf.io/people/ambassadors/)
- [Governing Board](https://www.cncf.io/people/governing-board/)
- [Kubestronaut](https://www.cncf.io/training/kubestronaut/)
- [Staff](https://www.cncf.io/people/staff/)
- [Technical Oversight Committee](https://www.cncf.io/people/technical-oversight-committee/)

CNCF community members can request access to any repo by submitting a PR to change the config.yaml file in this repo.

## CLOWarden Permissions Documentation

For comprehensive guidance on managing repository permissions using CLOWarden:

- **[CLOWarden Permissions Guide](CLOWARDEN_PERMISSIONS.md)** - Complete documentation on permission levels, configuration, and best practices
- **[Contributing Permissions](CONTRIBUTING_PERMISSIONS.md)** - Step-by-step guide for requesting and managing permissions
- **[Quick Reference](docs/PERMISSIONS_QUICK_REFERENCE.md)** - Syntax reference and common patterns
- **[Workflow Guide](docs/CLOWARDEN_WORKFLOW.md)** - Detailed workflow from request to implementation
- **[Permissions Checklist](docs/PERMISSIONS_CHECKLIST.md)** - Validation and quality assurance checklists
- **[Documentation Index](docs/INDEX.md)** - Complete documentation navigation

These documents address [Issue #230](https://github.com/cncf/people/issues/230) and provide the missing documentation for CLOWarden's permission management system.

## Listing Formats

### config.yaml configures CNCF org repository access

Use config.yaml here to control repo-level access to your CNCF org repository.

config.yaml documents the people, and teams of people, who are granted access to GitHub repositories in the CNCF org.

DO NOT USE settings.yml at the repo-level to control permission; if you do, [Sheriff](#notes) will overwite permissions described in the repo-level settings.yml with the settings described here in config.yaml.

A person's GitHub profile is used to grant access to a repository or define membership of a team.

Adding an entry to repositories allow you to describe who has access to your repoistory.

```yaml
repositories:
  - name: repo_name
    external_collaborators:
      github_profile_1: read | triage | write | maintain | admin
              |
      github_profile_n: read | triage | write | maintain | admin
    teams:
      team_name_1: read | triage | write | maintain | admin
              |
      team_name_n: read | triage | write | maintain | admin
    # Optional repository settings
    settings:
      has_wiki: true|false # Default is false
    visibility: public | private # Default is public
```

Note: the ```name: repo name``` does not necessarily appear as the first field in a repositories entry which can be confusing.

 Named teams referenced in a ```repository``` entry are also defined in config.yaml under ```teams```. (much further down the file, beyond line 10,000)

```yaml
teams:
  - name: team_name
    maintainers:
      - github_profile_1
               |
      - github_profile_n
    members:
      has_wiki: true|false
    displayName: Team name that can have spaces used to create a Slack Channel
    slack: {true|false|Slack channel name}  # Create a Slack channel for this team
    secret: {true|false} # Hidden GitHub Team
```

#### Notes

[cncf/sheriff](https://github.com/cncf/sheriff) periodically reads config.yaml on the main branch to apply the permissions to CNCF orgs, so once your PR is approved, the [Sheriff Apply GitHub action](https://github.com/cncf/people/actions/workflows/apply.yml ) will run to apply your changes.

[cncf/sheriff](https://github.com/cncf/sheriff) is a fork of [electron/sheriff](https://github.com/electron/sheriff). The cncf fork has code to cover CNCF-specific procedures. Thank you Electron Sheriff contributors.

### people.json

The [people.json file](https://github.com/cncf/people/blob/main/people.json) lists all people in alphabetical order by name.  Add new entries in the right place in the list.  Not all fields are used by each listing.  This is the format:

```json
    {
        "name":"Full name of person",
        "bio":"Full bio of person. Use html markup when needed.",
        "company":"Company and/or title",
        "pronouns":"Personal pronouns",
        "location":"A Google Maps readable name of city, state, country",
        "linkedin":"LinkedIn url",
        "twitter":"Twitter url",
        "github":"GitHub url",
        "bluesky":"Bluesky url",
        "wechat":"Wechat url",
        "website":"Personal website",
        "youtube":"YouTube url",
        "priority":Value to diffentiate between other entries in an ordered list; omit this entry in most cases,
        "languages":[Array of languages spoken],
        "projects":[Array of CNCF projects of expertise],
        "category":[Array of categories the person belongs to],
        "email": "person!example.com",
        "slack_id": "U123ABC456",
        "image":"Image filename from the /images/ directory"
    }
```

Project names must exactly match [the landscape listing](https://landscape.cncf.io/card-mode?project=hosted).  Category names must exactly match the list above.

And here is an example entry:

```json
    {
        "name":"Johnny Appleseed",
        "bio":"John Chapman (September 26, 1774 – March 18, 1845), better known as Johnny Appleseed, was an American pioneer nurseryman who introduced apple trees to large parts of <a href='https://en.wikipedia.org/wiki/Pennsylvania'>Pennsylvania</a>, Ohio, Indiana, Illinois and Ontario, as well as the northern counties of present-day West Virginia.",
        "company":"Apples R Us",
        "pronouns":"he/him",
        "location":"Portland, Maine, United States",
        "linkedin":"https://www.linkedin.com/in/johnny-appleseed/",
        "twitter":"https://twitter.com/jappleseed",
        "github":"https://github.com/jappleseed",
        "bluesky":"https://bsky.app/profile/jappleseed",
        "wechat":"https://web.wechat.com/jappleseed",
        "website":"https://jappleseed.com",
        "youtube":"https://www.youtube.com/c/jappleseed",
        "priority":10,
        "languages":["Spanish","English"],
        "projects":["prometheus","kubernetes","envoy"],
        "category":["Ambassadors"],
        "email": "johnny!example.com",
        "slack_id": "U123ABC456",
        "image":"jappleseed.jpg"
    }
```

## Images

Upload your headshot image to the `/images/` directory with a filename made up of your name.  Images should be at least 500x500px with file size less than 100kB.

## Team Management

Also within this repo is a YAML file used by our [automation tooling](https://github.com/electron/sheriff) to help us manage access to resources for teams. This tooling takes advantage of data in [people.json](people.json) such as the `email` and `slack_id` fields. This will allow us to add maintainers to different properties only using their GitHub handle.

- To find your Slack ID for the CNCF slack, please follow this [handy guide](https://moshfeu.medium.com/how-to-find-my-member-id-in-slack-workspace-d4bba942e38c)

- When adding your email, please follow the same format used within [devstats](https://github.com/cncf/devstats):

  ```shell
  email!address.xyz
  ```
