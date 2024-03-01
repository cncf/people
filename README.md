# CNCF People Overview

This repo stores the data that

1. populates various people listing pages on the cncf.io website
2. grants access to repositories in the CNCF GitHub Org

## Update your listing(s) on the cncf.io website pages with people.json

You can update your listing in people.json by submitting a pull request for approval. After the PR is merged, the CNCF site will reflect the update within 10 min.

The listings include:

- [Ambassadors](https://www.cncf.io/people/ambassadors/)
- [Governing Board](https://www.cncf.io/people/governing-board/)
- [Staff](https://www.cncf.io/people/staff/)
- [Technical Oversight Committee](https://www.cncf.io/people/technical-oversight-committee/)

## Requesting access to CNCF repositories using CLOWarden and config.yaml

The CNCF has centralized access control for repos in this org using a application called CLOWarden [src](https://github.com/cncf/clowarden) [site](https://clowarden.io/audit/).

Submitting Pull request to change config.yaml is how you request repo access.

Your submitted changes will be validated on the Pull Request by CLOWarden. If there are any problems with your request, you will receive clear instructions from CLOWarden on how to fix them.

The rules contained in config.yaml are the single source of truth that document who has access to repos in the CNCF Org on Github and represent the desired state that is read by CLOWarden. 

If you grant access to a repo by any other means (manually using the GitHub web app, updating settings.yml in a repos .github directory) and the access granted is not already described in the config.yaml file here, then CLOWarden will revert the access granted each time it checks the config.yaml file.

There are two ways to grant repo access to a community member in config.yaml. You can add their Github Profile to a repo entry or a named team. If you add them to a repo entry then the user will be granted the stated permission level to just that repo.
If you add them to a named team then any repo that that team has access to will be conferred to the newly added team member. Teams can contain sub teams.

```yaml
repositories:
  - name: REPO_NAME
    external_collaborators:
      GITHUB_PROFILE_1: read | triage | write | maintain | admin
              |
              |
      GITHUB_PROFILE_N: read | triage | write | maintain | admin
    teams:
      team_name_1: read | triage | write | maintain | admin
              |
      team_name_n: read | triage | write | maintain | admin
    # Optional repository settings
    settings:
      has_wiki: true|false # Default is false
    visibility: public | private # Default is public
```

Note: the ```name: REPO_NAME``` does not necessarily appear as the first field in a repositories entry which can be confusing.

Named teams referenced in a ```repository``` entry are also defined in config.yaml under ```teams```. (much further down the file, beyond line 10,000)

```yaml
teams:
  - name: TEAM_NAME
    displayName: You can add a full team name here with spaces.
    maintainers:
      - github_profile_1
               |
      - github_profile_n
    members:
      has_wiki: true|false
    secret: {true|false} # Hidden GitHub Team
```

## Notes

CLOWarden periodically reads config.yaml on the main branch to apply the permissions to repos in the CNCF orgs.

Changes are applied within an hour of being merged.

You can monitor the application of your changes on [clowarden.io/audit](https://clowarden.io/audit/?page=1)

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

Upload your headshot image to the `/images/` directory with a filename made up of your name.  Images should be at least 500x500px, 72dpi, and should be in JPG format with file size less than 100kB.

## Team Management

Also within this repo is a YAML file used by our [automation tooling](https://github.com/electron/sheriff) to help us manage access to resources for teams. This tooling takes advantage of data in [people.json](people.json) such as the `email` and `slack_id` fields. This will allow us to add maintainers to different properties only using their GitHub handle.

- To find your Slack ID for the CNCF slack, please follow this [guide](https://slack.com/intl/en-ie/help/articles/221769328-Locate-your-Slack-URL-or-ID)

- When adding your email, please follow the same format used within [devstats](https://github.com/cncf/devstats):

  ```shell
  email!address.xyz
  ```
