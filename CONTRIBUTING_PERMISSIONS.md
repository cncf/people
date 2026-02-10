# Contributing to CLOWarden Permissions

## Getting Started

This guide helps you contribute to the CLOWarden permissions configuration for CNCF repositories.

## Prerequisites

- GitHub account
- Basic understanding of YAML
- Familiarity with GitHub permissions model
- Access to CNCF organization (for internal contributors)

## Making Changes

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR-USERNAME/people.git
cd people
```

### 2. Create Feature Branch

```bash
git checkout -b add-permissions-for-project-x
```

### 3. Edit Configuration

Edit `config.yaml` to add or modify permissions:

```yaml
repositories:
  - name: your-project
    teams:
      cncf-projects: admin
    external_collaborators:
      your-username: maintain
```

### 4. Validate Changes

Before submitting, validate your changes:

```bash
# Check YAML syntax
yamllint config.yaml

# Validate against schema (if available)
# Check for common issues
```

### 5. Commit and Push

```bash
git add config.yaml
git commit -m "Add permissions for project-x

- Add admin access for cncf-projects team
- Add maintain access for external contributor
- Enable wiki for project documentation

Fixes #issue-number"

git push origin add-permissions-for-project-x
```

### 6. Create Pull Request

1. Go to GitHub and create a pull request
2. Use the provided template
3. Fill in all required information
4. Request review from appropriate team

## Permission Request Process

### For New Repositories

1. **Repository Creation**: Ensure repository exists
2. **Team Assignment**: Identify appropriate teams
3. **Permission Level**: Choose minimum necessary permissions
4. **Settings Configuration**: Configure repository settings
5. **Documentation**: Update relevant documentation

### For Existing Repositories

1. **Current State**: Review existing permissions
2. **Justification**: Provide reason for changes
3. **Impact Assessment**: Consider security implications
4. **Approval**: Get approval from repository maintainers

## Pull Request Template

```markdown
## Permission Change Request

### Repository: [repository-name]

### Type of Change
- [ ] New repository permissions
- [ ] Modify existing permissions
- [ ] Add external collaborator
- [ ] Team changes
- [ ] Settings update

### Changes Made
- List specific changes
- Include permission levels
- Mention affected users/teams

### Justification
- Why are these changes needed?
- What problem does this solve?
- Security considerations addressed?

### Testing
- [ ] YAML syntax validated
- [ ] Permissions tested in staging
- [ ] Documentation updated

### Checklist
- [ ] Followed security guidelines
- [ ] Used minimum necessary permissions
- [ ] Updated documentation if needed
- [ ] Requested appropriate reviews
```

## Review Process

### Automatic Checks

1. **YAML Validation**: Syntax and structure
2. **Schema Validation**: Against defined schema
3. **Security Scan**: Permission level appropriateness
4. **Duplicate Check**: No conflicting permissions

### Manual Review

1. **Security Review**: By security team
2. **Technical Review**: By automation team
3. **Project Review**: By project maintainers
4. **Final Approval**: By designated approvers

## Common Scenarios

### Adding New Project Maintainer

```yaml
repositories:
  - name: my-project
    external_collaborators:
      new-maintainer: maintain  # Not admin unless necessary
```

### Creating Project Team

```yaml
teams:
  - name: my-project-team
    maintainers:
      - project-lead
    members:
      - contributor1
      - contributor2
    displayName: "My Project Team"
```

### Repository Settings Update

```yaml
repositories:
  - name: my-project
    settings:
      has_wiki: true      # Enable project wiki
      has_issues: true    # Enable issue tracking
```

## Security Guidelines

### Permission Levels

- **admin**: Only for repository owners and senior maintainers
- **maintain**: For active maintainers who need management access
- **write**: For regular contributors who need push access
- **read**: For reviewers and observers
- **triage**: For issue managers without code access

### External Collaborators

- Minimize external collaborators
- Regular audit and cleanup
- Time-bound access when possible
- Clear justification required

### Team Management

- Use teams instead of individual permissions
- Clear team purposes and responsibilities
- Regular team membership review
- Proper team hierarchy

## Troubleshooting

### Common Issues

**YAML Syntax Error**
```bash
# Check syntax
yamllint config.yaml
```

**Permission Denied**
- Verify you have necessary GitHub permissions
- Check if you're member of required teams
- Contact automation team for access

**Team Not Found**
- Verify team exists in organization
- Check team name spelling
- Ensure team is not secret (if accessing externally)

**Invalid User**
- Verify GitHub username
- Check if user exists
- Ensure user has accepted organization invitation

### Getting Help

1. **Documentation**: Check existing documentation first
2. **Issues**: Search existing GitHub issues
3. **Slack**: Contact #cncf-automation channel
4. **Email**: Reach out to automation team
5. **Office Hours**: Attend weekly office hours

## Best Practices

### Configuration Management

- Keep changes small and focused
- One logical change per pull request
- Clear commit messages
- Proper branch naming

### Documentation

- Update documentation with changes
- Include examples for complex configurations
- Maintain changelog for major changes
- Keep README up to date

### Testing

- Validate YAML syntax
- Test permissions in staging environment
- Verify team memberships
- Check external collaborator access

### Security

- Follow principle of least privilege
- Regular permission audits
- Secure handling of sensitive repositories
- Proper access controls

## Resources

- [CLOWarden Documentation](CLOWARDEN_PERMISSIONS.md)
- [GitHub Permissions Guide](https://docs.github.com/en/organizations/managing-access-to-your-organizations-repositories)
- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)
- [CNCF Security Guidelines](https://github.com/cncf/foundation/blob/master/security-guidelines.md)