# CLOWarden Workflow Guide

## Overview

This document describes the complete workflow for managing permissions using CLOWarden, from initial request to final implementation.

## Workflow Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Permission    │    │   Create PR     │    │   Review &      │
│   Request       │───▶│   with Changes  │───▶│   Validation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLOWarden     │    │   Merge PR      │    │   Approval      │
│   Applies       │◀───│   to Main       │◀───│   Process       │
│   Changes       │    │   Branch        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Detailed Process

### 1. Permission Request Phase

#### 1.1 Identify Need
- New repository created
- Team member changes
- External collaborator request
- Permission level adjustment

#### 1.2 Gather Information
- Repository name
- Required permission level
- Justification for access
- Duration (if temporary)
- Security considerations

#### 1.3 Check Current State
```bash
# Review current config.yaml
grep -A 10 "name: repository-name" config.yaml
```

### 2. Configuration Phase

#### 2.1 Fork Repository
```bash
git clone https://github.com/YOUR-USERNAME/people.git
cd people
git checkout -b permission-update-YYYYMMDD
```

#### 2.2 Edit Configuration
```yaml
# Example: Adding new repository
repositories:
  - name: new-project
    teams:
      cncf-projects: admin
      project-team: maintain
    external_collaborators:
      expert-contributor: write
    settings:
      has_wiki: true
      has_issues: true
    visibility: public
```

#### 2.3 Validate Changes
```bash
# Check YAML syntax
yamllint config.yaml

# Validate structure
python validate_config.py config.yaml
```

### 3. Pull Request Phase

#### 3.1 Commit Changes
```bash
git add config.yaml
git commit -m "Add permissions for new-project

- Grant admin access to cncf-projects team
- Grant maintain access to project-team
- Add expert-contributor as external collaborator
- Enable wiki and issues

Addresses: #issue-number"
```

#### 3.2 Push and Create PR
```bash
git push origin permission-update-YYYYMMDD
# Create PR on GitHub with proper template
```

#### 3.3 PR Template Usage
```markdown
## Permission Change Request

### Repository: new-project
### Type: New repository permissions

### Changes:
- Added cncf-projects team with admin access
- Added project-team with maintain access  
- Added expert-contributor as external collaborator
- Enabled wiki and issues

### Justification:
New CNCF project requiring standard permission structure
for project governance and external expert collaboration.

### Security Review:
- Follows principle of least privilege
- External collaborator has legitimate need
- Standard CNCF project setup
```

### 4. Review Phase

#### 4.1 Automated Checks
- YAML syntax validation
- Schema compliance check
- Security policy validation
- Duplicate permission check

#### 4.2 Manual Reviews

**Security Review Checklist:**
- [ ] Appropriate permission levels
- [ ] Justified external collaborators
- [ ] No excessive admin access
- [ ] Follows security guidelines

**Technical Review Checklist:**
- [ ] Correct YAML structure
- [ ] Valid team/user names
- [ ] Proper repository settings
- [ ] No configuration conflicts

**Project Review Checklist:**
- [ ] Project maintainer approval
- [ ] Legitimate business need
- [ ] Temporary access documented
- [ ] Compliance with project policies

### 5. Approval Phase

#### 5.1 Required Approvals
- **Security Team**: For external collaborators
- **Automation Team**: For technical correctness
- **Project Maintainers**: For project-specific changes
- **TOC Members**: For sensitive repositories

#### 5.2 Approval Matrix

| Change Type | Security | Automation | Project | TOC |
|-------------|----------|------------|---------|-----|
| New repo | ✓ | ✓ | ✓ | - |
| External collab | ✓ | ✓ | ✓ | - |
| Admin access | ✓ | ✓ | ✓ | ✓ |
| Team changes | - | ✓ | ✓ | - |
| Settings only | - | ✓ | - | - |

### 6. Implementation Phase

#### 6.1 Merge Process
```bash
# After all approvals
git checkout main
git pull origin main
git merge --no-ff permission-update-YYYYMMDD
git push origin main
```

#### 6.2 CLOWarden Execution
- Automatic trigger on main branch update
- Reads updated config.yaml
- Applies changes to GitHub repositories
- Generates execution report

#### 6.3 Verification
```bash
# Check applied permissions
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/cncf/repository-name/collaborators

# Verify team access
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/cncf/repository-name/teams
```

## Emergency Procedures

### Urgent Access Request

#### Fast-Track Process
1. **Immediate Need**: Security incident, critical bug fix
2. **Temporary Access**: Grant minimal required access
3. **Documentation**: Create issue with full justification
4. **Follow-up**: Regular process within 24 hours

#### Emergency Contacts
- **Security Team**: security@cncf.io
- **Automation Team**: automation@cncf.io
- **On-call Engineer**: Check current rotation

### Access Revocation

#### Immediate Revocation
```yaml
# Remove from config.yaml
repositories:
  - name: repository-name
    external_collaborators:
      # removed-user: permission  # REMOVED
```

#### Bulk Revocation
```bash
# Script for multiple repositories
./scripts/revoke_user_access.sh username
```

## Monitoring and Auditing

### Regular Audits

#### Monthly Reviews
- External collaborator access
- Admin permission holders
- Inactive team members
- Repository settings compliance

#### Quarterly Reviews
- Team structure optimization
- Permission level appropriateness
- Security policy compliance
- Access pattern analysis

### Monitoring Tools

#### Dashboard Metrics
- Permission change frequency
- External collaborator count
- Admin access distribution
- Repository compliance status

#### Alerts
- Unauthorized permission changes
- New external collaborators
- Admin access grants
- Policy violations

## Best Practices

### Configuration Management
- Small, focused changes
- Clear commit messages
- Proper branch naming
- Regular config backups

### Security Practices
- Principle of least privilege
- Regular access reviews
- Time-bound permissions
- Audit trail maintenance

### Process Efficiency
- Batch related changes
- Use templates consistently
- Automate validation
- Document decisions

## Troubleshooting

### Common Issues

#### Permission Not Applied
1. Check CLOWarden execution logs
2. Verify YAML syntax
3. Confirm user/team exists
4. Check GitHub API limits

#### Access Denied
1. Verify your GitHub permissions
2. Check organization membership
3. Confirm team membership
4. Contact automation team

#### Configuration Conflicts
1. Check for duplicate entries
2. Verify permission hierarchy
3. Review team inheritance
4. Validate against schema

### Resolution Steps

#### Issue Investigation
```bash
# Check recent changes
git log --oneline -10 config.yaml

# Verify current state
./scripts/audit_permissions.sh repository-name

# Check CLOWarden logs
kubectl logs -n clowarden deployment/clowarden
```

#### Rollback Procedure
```bash
# Emergency rollback
git revert HEAD
git push origin main

# Targeted rollback
git checkout HEAD~1 -- config.yaml
git commit -m "Rollback permissions for repository-name"
git push origin main
```

## Integration Points

### GitHub Integration
- Repository creation hooks
- Team membership sync
- Permission change notifications
- Audit log integration

### CNCF Systems
- LF Identity integration
- Slack notifications
- ServiceNow integration
- Compliance reporting

### Monitoring Systems
- Prometheus metrics
- Grafana dashboards
- Alert manager rules
- Log aggregation

## Future Enhancements

### Planned Features
- Self-service permission requests
- Automated approval workflows
- Advanced audit capabilities
- Integration with more systems

### Roadmap Items
- Machine learning for access patterns
- Predictive permission management
- Enhanced security scanning
- Mobile approval interface