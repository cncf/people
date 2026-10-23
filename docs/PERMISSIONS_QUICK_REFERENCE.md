# CLOWarden Permissions Quick Reference

## Permission Levels

| Level | Code | Description |
|-------|------|-------------|
| Admin | `admin` | Full repository access |
| Maintain | `maintain` | Manage without sensitive actions |
| Write | `write` | Push access |
| Read | `read` | Pull access only |
| Triage | `triage` | Issue/PR management |

## Basic Syntax

### Repository with Team Access
```yaml
repositories:
  - name: repo-name
    teams:
      team-name: permission-level
```

### Repository with External Collaborator
```yaml
repositories:
  - name: repo-name
    external_collaborators:
      username: permission-level
```

### Repository with Settings
```yaml
repositories:
  - name: repo-name
    settings:
      has_wiki: true
      has_issues: true
    visibility: public
```

### Team Definition
```yaml
teams:
  - name: team-name
    maintainers:
      - username1
    members:
      - username2
    displayName: "Display Name"
    secret: false
```

## Common Commands

### Add New Repository
```yaml
repositories:
  - name: new-project
    teams:
      cncf-projects: admin
    settings:
      has_wiki: true
```

### Add External Collaborator
```yaml
# Add to existing repository entry
external_collaborators:
  new-user: write
```

### Create New Team
```yaml
teams:
  - name: new-team
    maintainers:
      - lead-user
    members:
      - member1
      - member2
```

## Validation Checklist

- [ ] Valid YAML syntax
- [ ] Correct permission levels
- [ ] Existing usernames
- [ ] Valid team names
- [ ] Proper indentation
- [ ] No duplicate entries

## Common Patterns

### Standard Project Setup
```yaml
repositories:
  - name: project-name
    teams:
      cncf-projects: admin
      project-maintainers: maintain
    external_collaborators:
      external-expert: write
    settings:
      has_wiki: true
      has_issues: true
    visibility: public
```

### Private Repository
```yaml
repositories:
  - name: private-project
    teams:
      core-team: admin
    visibility: private
```

### Archive Repository
```yaml
repositories:
  - name: archived-project
    teams:
      cncf-projects: admin
    settings:
      archived: true
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| YAML syntax error | Check indentation and colons |
| User not found | Verify GitHub username |
| Team not found | Check team exists in org |
| Permission denied | Verify your access level |
| Invalid permission | Use valid permission levels |

## Quick Links

- [Full Documentation](../CLOWARDEN_PERMISSIONS.md)
- [Contributing Guide](../CONTRIBUTING_PERMISSIONS.md)
- [Workflow Guide](CLOWARDEN_WORKFLOW.md)
- [Checklist](PERMISSIONS_CHECKLIST.md)