# AWS Static Website Platform — Production-Grade Hosting & CI/CD

A complete AWS production-style static website deployment platform featuring secure HTTPS delivery, CDN acceleration, infrastructure automation, and continuous deployment.

## Project Overview
Production-grade static website hosting on AWS using S3, CloudFront, ACM, boto3 automation, lifecycle policies, and GitHub Actions CI/CD.

## Architecture Diagram

```mermaid
flowchart TD
    User([User]) --> CF[CloudFront Distribution \n HTTPS]
    CF --> S3[Amazon S3 Bucket \n Static Website Files]
    
    GH[GitHub Actions] -.-> |Deploy| S3
    GH -.-> |Invalidate Cache| CF
```
