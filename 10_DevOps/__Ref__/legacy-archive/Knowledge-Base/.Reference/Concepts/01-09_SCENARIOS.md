# SCENARIOS - Modules 01-09 (Combined)

Real-world problem-solving scenarios across all Foundation modules.

---

## Module 01: LINUX BASICS

### Scenario 1: The Disappeared Files

**Problem:** User reports all files in `/home/user/project` disappeared after running a script.
**Investigation:** Find what happened, recover files if possible.
**Solution:** Check `.bash_history`, look in trash, check backups, examine script for `rm` commands.

### Scenario 2: Permission Denied Everywhere

**Problem:** After security update, user can't access their own files.
**Task:** Fix permissions without compromising security.
**Solution:** `sudo chown -R user:user /home/user`, verify with `ls -la`.

### Scenario 3: Disk Full But Where?

**Problem:** System says disk full but `df` shows 50% free.
**Task:** Find what's using space.
**Solution:** Check inodes `df -i`, find large deleted files still held by processes `lsof | grep deleted`.

### Scenario 4: Zombie Process Outbreak

**Problem:** System slow, `ps aux` shows 100+ zombie processes.
**Task:** Clean up zombies, prevent recurrence.
**Solution:** Find parent process `ps -ef | grep Z`, kill parent, fix application bug.

### Scenario 5: Cron Job Not Running

**Problem:** Backup script works manually but not via cron.
**Task:** Debug cron job.
**Solution:** Check cron logs, verify PATH in cron, redirect output to file, check permissions.

---

## Module 02: GIT & GITHUB

### Scenario 1: Accidental Force Push

**Problem:** Junior dev force-pushed and overwrote team's work.
**Task:** Recover lost commits.
**Solution:** Use `git reflog` on affected developers' machines, cherry-pick lost commits, create branch protection rules.

### Scenario 2: Merge Conflict Hell

**Problem:** Feature branch has 50+ conflicts with main after 2 months of development.
**Task:** Resolve conflicts without losing work.
**Solution:** Create backup branch, rebase iteratively, use `git mergetool`, test thoroughly after each resolution.

### Scenario 3: Sensitive Data in History

**Problem:** API key committed 20 commits ago, now in production.
**Task:** Remove from history completely.
**Solution:** Regenerate API key immediately, use `git filter-branch` or BFG Repo-Cleaner, force push, notify team.

### Scenario 4: Detached HEAD State

**Problem:** Developer lost work after being in detached HEAD.
**Task:** Recover commits.
**Solution:** `git reflog`, find lost commits, create branch from commit hash.

### Scenario 5: Massive Repository Size

**Problem:** Git repo is 5GB, clones take 30 minutes.
**Task:** Reduce repository size.
**Solution:** Find large files `git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -10)"`, remove with BFG, use Git LFS for large files.

---

## Module 03: NETWORKING

### Scenario 1: Website Down - DNS or Server?

**Problem:** Company website unreachable. Boss is furious.
**Task:** Diagnose and fix ASAP.
**Solution:** `ping domain` (check if resolves), `dig domain` (check DNS), `curl -I http://domain` (check web server), check server logs.

### Scenario 2: Intermittent Connection Drops

**Problem:** API fails randomly, users complain.
**Task:** Find cause.
**Solution:** `mtr` to check packet loss, review firewall rules, check load balancer health, examine application logs for timeouts.

### Scenario 3: Port 80 Already in Use

**Problem:** Can't start web server, port 80 in use.
**Task:** Find what's using it, free the port.
**Solution:** `sudo netstat -tulpn | grep :80` or `sudo lsof -i :80`, kill process or change port.

### Scenario 4: DNS Propagation Delay

**Problem:** Changed DNS records 2 hours ago, still pointing to old server.
**Task:** Verify change, help users access new server.
**Solution:** Check TTL, flush DNS cache `sudo systemd-resolve --flush-caches`, test with different DNS servers `dig @8.8.8.8 domain`.

### Scenario 5: Network Segmentation Issue

**Problem:** Container can't reach database on different subnet.
**Task:** Fix connectivity.
**Solution:** Check routing tables, verify firewall rules, test with `telnet`, configure Docker networks properly.

---

## Module 04: HTML/CSS/JS

### Scenario 1: Layout Broken on Mobile

**Problem:** Website looks perfect on desktop, broken on phones.
**Task:** Make responsive.
**Solution:** Add viewport meta tag, use media queries, test with Chrome DevTools mobile view, use Flexbox/Grid for layout.

### Scenario 2: Form Submission Fails Silently

**Problem:** Users click submit, nothing happens, no errors.
**Task:** Debug and fix.
**Solution:** Check browser console, add event listener logging, verify form action/method, test validation, check CORS.

### Scenario 3: Page Load is 10 Seconds

**Problem:** Homepage takes forever to load.
**Task:**Improve performance.
**Solution:** Compress images, minify CSS/JS, use CDN, lazy load images, remove render-blocking resources, check Lighthouse report.

### Scenario 4: JavaScript Error in Production Only

**Problem:** Works in development, errors in production.
**Task:** Debug production issue.
**Solution:** Check browser compatibility, verify environment variables, test minified code, review error tracking (Sentry), enable source maps.

### Scenario 5: Cross-Browser Styling Issues

**Problem:** Site looks different in Chrome vs Firefox vs Safari.
**Task:** Achieve consistency.
**Solution:** Use CSS reset/normalize, test vendor prefixes, check Can I Use, use polyfills, test in Browserstack.

---

## Module 05: DOCKER

### Scenario 1: Container Keeps Restarting

**Problem:** Docker container in restart loop, application won't start.
**Task:** Fix and keep running.
**Solution:** `docker logs container`, check application logs, verify environment variables, test locally, check resource limits.

### Scenario 2: Image Build Takes 30 Minutes

**Problem:** Dockerfile build is painfully slow.
**Task:** Optimize build time.
**Solution:** Reorder Dockerfile layers, use `.dockerignore`, leverage build cache, use multi-stage builds, consider smaller base image.

### Scenario 3: Container Can't Connect to Database

**Problem:** Application container can't reach MySQL container.
**Task:** Fix networking.
**Solution:** Verify both on same network, check container names vs IPs, test with `docker exec -it app ping db`, review docker-compose networking.

### Scenario 4: Running Out of Disk Space

**Problem:** Server disk full from Docker.
**Task:** Clean up and prevent.
**Solution:** `docker system prune -af`, remove old images, use volumes wisely, set up log rotation, monitor disk usage.

### Scenario 5: Environment Variables Not Working

**Problem:** App can't read env vars in container.
**Task:** Fix configuration.
**Solution:** Check docker run -e, verify docker-compose env_file, use .env correctly, check application reads ENV correctly.

---

## Module 06: CI/CD

### Scenario 1: GitHub Actions Failing on Main

**Problem:** CI passes on feature branch, fails on main branch.
**Task:** Fix broken pipeline.
**Solution:** Check workflow triggers, verify secrets available on main, review branch protection rules, check for hardcoded values.

### Scenario 2: Tests Pass Locally, Fail in CI

**Problem:** "Works on my machine" syndrome.
**Task:** Achieve consistency.
**Solution:** Match CI environment locally, use Docker for tests, verify Node/Python versions match, check for timing issues, review test dependencies.

### Scenario 3: Deployment Times Out

**Problem:** Deploy job runs for 60 minutes then times out.
**Task:** Speed up deployment.
**Solution:** Optimize Docker builds, cache dependencies, parallelize jobs, use artifacts instead of rebuilding, review deploy script efficiency.

### Scenario 4: Secrets Exposed in Logs

**Problem:** API key visible in build logs.
**Task:** Remove and prevent.
**Solution:** Rotate secret immediately, use `::add-mask::`, review workflow for echo statements, use secret management properly.

### Scenario 5: Matrix Build One Combination Fails

**Problem:** Tests pass on Node 18, fail on Node 20.
**Task:** Support all versions.
**Solution:** Check API changes between versions, update dependencies, use compatibility tools, consider dropping old version support.

---

## Module 07: WEB SERVERS (NGINX)

### Scenario 1: 502 Bad Gateway

**Problem:** NGINX shows 502, application is running.
**Task:** Fix proxy issue.
**Solution:** Check backend is listening, verify proxy_pass URL, review upstream configuration, check firewall, examine error logs.

### Scenario 2: SSL Certificate Expired
**Problem:** Website shows "Not Secure", cert expired yesterday.
**Task:** Renew certificate.
**Solution:** Run `certbot renew`, verify auto-renewal cron job, check domain DNS, test HTTPS, set up monitoring for expiry.

### Scenario 3: High Response Times

**Problem:** Pages take 5+ seconds to load.
**Task:** Optimize NGINX.
**Solution:** Enable gzip, configure caching, adjust worker processes, use HTTP/2, offload static files to CDN, check backend performance.

### Scenario 4: Rate Limiting Not Working

**Problem:** API being abused, rate limit config ignored.
**Task:** Enforce rate limits.
**Solution:** Review `limit_req_zone` configuration, check zone size, verify location block usage, test with curl, check logs.

### Scenario 5: Configuration Syntax Error

**Problem:** NGINX won't start after config change.
**Task:** Fix and prevent.
**Solution:** `nginx -t` to test config, review recent changes, use version control for configs, implement pre-deployment testing.

---

## Module 08: DEPLOYMENT

### Scenario 1: Deployment Caused Downtime

**Problem:** Normal deployment took site offline for 5 minutes.
**Task:** Implement zero-downtime deployment.
**Solution:** Use blue-green deployment, implement health checks, use load balancer, graceful shutdown, test rollback procedure.

### Scenario 2: Database Migration Failed Mid-Deployment

**Problem:** New code deployed but DB migration failed.
**Task:** Recover and prevent.
**Solution:** Rollback code and DB to previous state, make migrations backward compatible, use transaction, test migrations in staging first.

### Scenario 3: Environment Variables Mismatch

**Problem:** Production using staging database.
**Task:** Fix and prevent.
**Solution:** Verify .env files, use different variable names, implement environment checks, automate environment setup, use secret management.

### Scenario 4: Can't Rollback Deployment

**Problem:** New version has bugs, can't rollback easily.
**Task:** Implement rollback.
**Solution:** Tag releases, keep previous version running, use feature flags, implement automated rollback, test rollback regularly.

### Scenario 5: Post-Deploy Monitoring Shows Issues

**Problem:** Deploy succeeded but monitoring shows errors.
**Task:** Investigate and fix.
**Solution:** Check application logs, review recent changes, verify all services started, check database connections, review health checks.

---

## Module 09: MONITORING

### Scenario 1: High CPU but Can't Find Cause

**Problem:** Server at 90% CPU, unclear which process.
**Task:** Identify and fix.
**Solution:** `top -c` for processes, `iotop` for disk I/O, check cron jobs, review application logs, use profiling tools.

### Scenario 2: Disk Filling Up Mysteriously

**Problem:** Disk usage grows 10GB per day.
**Task:** Find and stop.
**Solution:** `du -sh /*` to find large directories, check log files, review log rotation, find large deleted files `lsof +L1`, implement monitoring alerts.

### Scenario 3: Memory Leak in Production

**Problem:** App uses more memory over time, eventually crashes.
**Task:** Identify and fix leak.
**Solution:** Monitor with `top`, use heap profiling, review recent code changes, check for event listener leaks, implement memory limits and restarts.

### Scenario 4: Alerts Fatigue

**Problem:** Getting 100+ alerts per day, team ignoring them.
**Task:** Improve alerting.
**Solution:** Review and tune thresholds, implement alert aggregation, use different severities, create runbooks, reduce false positives.

### Scenario 5: Logs Missing for Critical Period

**Problem:** Need logs from yesterday's incident, but they're gone.
**Task:** Recover and prevent.
**Solution:** Check log rotation settings, restore from backups if available, implement centralized logging, increase retention period, set up log archival.

---

## 🎯 How to Use These Scenarios

1. **Read scenario** without looking at solution
2. **Plan approach** - how would you solve it?
3. **Try solving** on your own system
4. **Compare** with provided solution
5. **Document** what you learned

---

## 💡 Scenario-Based Learning Tips

- Create your own scenarios from real issues
- Practice with teammates
- Time yourself solving scenarios
- Build a troubleshooting playbook
- Share solutions with team

---

> **Master these scenarios → Real-world DevOps skills!** 🔥
