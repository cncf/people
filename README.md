# CNCF People Overview

This repo stores the data that

1. Populates various people listing pages on the cncf.io website
2. Grants access to repositories in the CNCF GitHub Org

## Update your listing(s) on the cncf.io website pages with people.json

You can update your listing in people.json by submitting a pull request for approval. After the PR is merged, the CNCF site will reflect the update within 10 min.

The listings include:

- [Ambassadors](https://www.cncf.io/people/ambassadors/)
- [Governing Board](https://www.cncf.io/people/governing-board/)
- [Staff](https://www.cncf.io/people/staff/)
- [Technical Oversight Committee](https://www.cncf.io/people/technical-oversight-committee/)

## Requesting access to CNCF repositories using CLOWarden and config.yaml

The CNCF has centralized access control for repos in this org using CLOWarden [src](https://github.com/cncf/clowarden) [site](https://clowarden.io/audit/).

To request access to a repository

- For team maintainers, first invite the user to join the CNCF org
- then submit a pull request to modify [config.yaml](./config.yaml) file as described below

Your submitted changes will be checked and validated on the Pull Request by CLOWarden.

If there are problems with your changes, you will receive clear instructions from CLOWarden on how to fix them.

The access rules contained in config.yaml are the single source of truth that document who has access to repos in the CNCF Org on GitHub.
After each merged pull request config.yaml is read and processed automatically by CLOWarden to grant the stated access.

In the config.yaml file there are two ways to grant repo access to a community member

- add their GitHub username to a repository entry
  
  OR

- add them to a team and then add the team to a repository entry

```yaml
repositories:
  - name: REPO_NAME
    external_collaborators:
      GITHUB_USERNAME_1: read | triage | write | maintain | admin
              :
              :
      GITHUB_USERNAME_N: read | triage | write | maintain | admin
    teams:
      TEAM_NAME_1: read | triage | write | maintain | admin
              :
      TEAM_NAME_N: read | triage | write | maintain | admin
    # Optional repository settings
    settings:
      has_wiki: true|false # Default is false
    visibility: public | private # Default is public
```

> [!IMPORTANT]
>
> - Invite users to join the CNCF Org *before you add them via a PR* to config.yaml
> - GitHub usernames are case sensitive, mixed case usernames *should match* how they appear in their GitHub profile page
> - If you grant access to a repo by any other means (via the GitHub web app, updating settings.yml in a repository's .github directory) and the access granted is not already described in the config.yaml file here, then CLOWarden will revert the access granted outside of CLOWarden each time it checks the config.yaml file.

> [!NOTE]
>
> - CLOWarden will check your Pull Request changes to config.yaml and report any errors before they are merged and The CNCF Projects Team are here to help.
> - Having ```name: REPO_NAME``` appear as the first key in an repository array entry makes it easier to find and read the entry. Placing it elsewhere in the entry is valid YAML but if you want to make it easier to update we suggest you add the name field first.

Named teams referenced in an entry under ```repositories``` are also defined in config.yaml under ```teams```. (much further down the file, beyond line 10,000)

```yaml
teams:
  - name: TEAM_NAME
    displayName: You can add a full team name here with spaces.
    maintainers:
      - GITHUB_USERNAME_1
               |
               |
      - GITHUB_USERNAME_N
    members:
      has_wiki: true|false
    secret: {true|false} # Hidden GitHub Team
```

## Notes

After your PR is merged to main, CLOWarden will apply changes you have requested and then report the access changes made taken on [clowarden.io/audit](https://clowarden.io/audit/?page=1)

Changes are applied within an hour of being merged.

### people.json is used to generate listings on CNCF Web sites

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

Project names must exactly match [the landscape listing](https://landscape.cncf.io/?group=projects-and-products&view-mode=card&project=cncf).  

The ```category``` value is an array that can contain the following elements which determine where the entry for the person is rendered on the cncf.io site.

- "Ambassadors",
- "Governing Board"
- "Marketing Committee"
- "Staff"
- "Technical Oversight Committee"

Here is an sample entry:

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

- To find your Slack ID for the CNCF slack, please follow this [guide](https://slack.com/intl/en-ie/help/articles/221769328-Locate-your-Slack-URL-or-ID)
- When adding your email, please follow the same format used within [devstats](https://github.com/cncf/devstats):

  ```shell
  email!address.xyz
  ```

## Images

Upload your headshot image to the `/images/` directory with a filename made up of your name.  Images should be at least 500x500px, 72dpi, and should be in JPG format with file size less than 100kB.
