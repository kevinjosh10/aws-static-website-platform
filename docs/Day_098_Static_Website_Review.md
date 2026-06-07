# Day 098 – Week 14 Review: Static Website with Full Stack

**Date:** 07 June 2026  
**Duration:** ~2 Hours  
**Focus:** S3, CloudFront, Route 53, ACM, Python Boto3 Automation, GitHub Actions CI/CD, FinOps

---

## 🎯 Objective

Build a complete, production-grade static website hosting platform on AWS, incorporating global edge delivery, continuous deployment, and programmatic infrastructure automation.

Learn & Practice:
- S3 Static Hosting and Bucket Policies
- CloudFront CDN and HTTPS via ACM
- Route 53 custom domain management and Health Checks
- S3 Lifecycle Policies for cost optimization
- Boto3 scripting for infrastructure automation
- GitHub Actions for CI/CD

---

# 🏗️ 66. Full Production-Grade Static Hosting Pattern

The foundation of modern web hosting on AWS without managing servers.

Architecture:
```text
Route 53 (DNS)
      ↓
CloudFront (CDN + HTTPS)
      ↓
S3 (Static Origin)
```

Key Components:
- **S3 (Origin):** Stores the static HTML/CSS/JS files.
- **CloudFront (CDN):** Caches files globally at Edge Locations for single-digit millisecond latency.
- **Route 53 (Custom Domain):** Translates human-readable domains (e.g., example.com) to the CloudFront distribution.
- **ACM (SSL Certificate):** Provisions free SSL/TLS certificates attached to CloudFront to enforce HTTPS.

---

# 🗑️ 67. S3 Lifecycle Policy for Access Logs

Practicing real-world log retention and FinOps (cost control).

Goal: Manage S3 server access logs automatically.

Policy Rules:
1. **Transition to Glacier:** Move logs to cheaper `Glacier Flexible Retrieval` storage after 30 days.
2. **Expiration:** Permanently delete the logs after 1 year (365 days).

Benefits:
- Meets compliance requirements for 1-year log retention.
- Drastically reduces S3 storage costs by transitioning "cold" logs to Glacier.

---

# 🐍 68. Boto3 Infrastructure Automation

Replacing manual AWS Console clicks with programmatic Infrastructure as Code using the AWS SDK for Python (`boto3`).

### Script 1: `create_s3_static_site.py`
Automates the origin creation:
- Creates the S3 bucket.
- Removes the Public Access Block.
- Applies a `PublicReadGetObject` Bucket Policy.
- Enables Static Website Hosting.
- Uploads `index.html` and `style.css` with correct MIME types.

### Script 2: `invalidate_cloudfront.py`
Automates edge cache clearing:
- Takes the CloudFront Distribution ID.
- Creates an invalidation batch for `/*`.
- Forces edge servers worldwide to fetch the newest files from S3.

---

# ⚙️ 69. GitHub Actions CI/CD Workflow

Connecting the code repository to the cloud for continuous deployment.

Trigger:
```text
on:
  push:
    branches:
      - main
```

Workflow Steps:
1. **Checkout Code:** Pulls the latest repository files.
2. **Configure AWS Credentials:** Securely authenticates using GitHub Secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).
3. **Sync to S3:** Runs `aws s3 sync website/ s3://my-bucket --delete` to push new files.
4. **Invalidate Cache:** Runs `aws cloudfront create-invalidation` to instantly update the live site.

Result: Zero-touch deployments. Code pushed to `main` is live globally in under 10 seconds.

---

# ❤️ 70. Route 53 Health Checks & Active Recall

### Boto3 Route 53 Health Checks
Automating global monitoring for running EC2 instances:
- Wrote a boto3 script to query all running EC2 instances.
- For each instance, created a Route 53 Health Check pointing to its public IP.
- Enables automatic failover routing if an instance goes down.

### Anki Flashcards Added
To reinforce active recall, added cards for:
- **S3 Storage Classes:** Standard, IA, Glacier, Deep Archive, Intelligent-Tiering.
- **CloudFront Behaviors:** Viewer Protocol Policies, Allowed HTTP Methods, Cache TTLs.
- **Route 53 Routing Policies:** Simple, Weighted, Latency, Failover, Geolocation, Geoproximity, Multivalue Answer.

---

# ✅ Day 098 Summary

Today was a comprehensive review day where I tied together everything learned in Week 14. I built a complete, highly-available AWS static website platform leveraging S3, CloudFront, ACM, and Route 53. 

I moved beyond the AWS Management Console by writing Python (`boto3`) scripts to automate the provisioning of the bucket and the invalidation of the CDN cache. I then fully automated the deployment lifecycle by building a GitHub Actions CI/CD pipeline, and enforced FinOps best practices using S3 Lifecycle rules to manage server logs. Finally, I solidified my networking knowledge by programmatically creating Route 53 health checks and creating Anki flashcards for long-term retention.
