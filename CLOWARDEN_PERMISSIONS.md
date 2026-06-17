# CLOWarden Permissions Documentation

## Overview

CLOWarden is an automation tool that manages GitHub repository permissions for the CNCF organization. It reads configuration from `config.yaml` and automatically applies permissions to repositories, teams, and external collaborators.

## Permission Levels

### Repository Permission Levels

| Permission | Description | Capabilities |
|------------|-------------|--------------|
| `admin` | Full repository access | All repository actions including settings, security, and deletion |
| `maintain` | Manage repository | Manage issues, PRs, and some settings (no sensitive actions) |
| `write` | Push access | Read, clone, and push to repository |
| `read` | Pull access | Read and clone repository only |
| `triage` | Issue management | Manage issues and pull requests without code access |

### Team vs External Collaborators

- **Teams**: GitHub teams within the CNCF organization
- **External Collaborators**: Individual users outside the organization

## Configuration Structure

### Basic Repository Configuration

```yaml
repositories:
  - name: repository-name
    teams:
      team-name: permission-level
    external_collaborators:
      username: permission-level
    settings:
      has_wiki: true/false
    visibility: public/private/internal
```

### Example Configuration

```yaml
repositories:
  - name: example-project
    teams:
      cncf-automation: admin
      landscapers: write
    external_collaborators:
      johndoe: maintain
      janedoe: read
    settings:
      has_wiki: true
    visibility: public
```

## Team Management

### Defining Teams

```yaml
teams:
  - name: team-name
    maintainers:
      - username1
      - username2
    members:
      - username3
      - username4
    displayName: "Human Readable Team Name"
    secret: true/false
```

### Team Example

```yaml
teams:
  - name: cncf-projects
    maintainers:
      - jeefy
      - krook
    members:
      - caniszczyk
      - castrojo
    displayName: "CNCF Projects Team"
    secret: false
```

## Repository Settings

### Available Settings

- `has_wiki`: Enable/disable repository wiki
- `has_issues`: Enable/disable issues
- `has_projects`: Enable/disable projects
- `allow_squash_merge`: Allow squash merging
- `allow_merge_commit`: Allow merge commits
- `allow_rebase_merge`: Allow rebase merging

### Settings Example

```yaml
repositories:
  - name: my-project
    settings:
      has_wiki: true
      has_issues: true
      allow_squash_merge: true
      allow_merge_commit: false
```

## Best Practices

### Security Guidelines

1. **Principle of Least Privilege**: Grant minimum necessary permissions
2. **Regular Audits**: Review permissions quarterly
3. **Team-based Access**: Prefer teams over individual collaborators
4. **External Collaborator Limits**: Minimize external collaborators

### Configuration Guidelines

1. **Consistent Naming**: Use clear, consistent repository and team names
2. **Documentation**: Comment complex configurations
3. **Validation**: Test changes in staging environment
4. **Backup**: Keep configuration backups

## Common Use Cases

### Adding a New Repository

```yaml
repositories:
  - name: new-project
    teams:
      cncf-projects: admin
      project-maintainers: maintain
    settings:
      has_wiki: true
    visibility: public
```

### Adding External Collaborator

```yaml
repositories:
  - name: existing-project
    external_collaborators:
      new-contributor: write
```

### Creating a New Team

```yaml
teams:
  - name: new-team
    maintainers:
      - team-lead
    members:
      - member1
      - member2
    displayName: "New Team"
    secret: false
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Check if user has necessary GitHub permissions
2. **Team Not Found**: Verify team exists in organization
3. **Invalid Permission Level**: Use only valid permission levels
4. **Syntax Errors**: Validate YAML syntax

### Validation

Before applying changes:
1. Validate YAML syntax
2. Check all usernames exist
3. Verify team names are correct
4. Test with dry-run if available

## Related Documentation

- [Contributing Guide](CONTRIBUTING_PERMISSIONS.md)
- [Quick Reference](docs/PERMISSIONS_QUICK_REFERENCE.md)
- [Workflow Guide](docs/CLOWARDEN_WORKFLOW.md)
- [Checklist](docs/PERMISSIONS_CHECKLIST.md)

## Support

For questions or issues:
1. Check existing GitHub issues
2. Review documentation
3. Contact CNCF automation team
4. Create new issue with detailed description