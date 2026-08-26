# OpsPilot Architecture

## 1. Project Overview

OpsPilot is an AI-powered operations copilot designed to help teams
investigate operational issues, retrieve relevant organizational
knowledge, use approved tools, and recommend actions.

The system is designed around a human-in-the-loop approach.

AI assists with investigation and recommendations, while humans
remain responsible for consequential actions.

---

## 2. Problem Statement

Modern engineering and operations teams often need to investigate
incidents using information spread across multiple sources.

Examples include:

- application logs
- incident reports
- internal documentation
- runbooks
- service information
- deployment information
- previous incidents

Finding and connecting this information manually can be slow.

OpsPilot aims to provide a single AI-assisted interface for
investigating operational problems and producing structured,
evidence-based recommendations.

---

## 3. Primary User

The primary user is an engineering or operations team member
investigating an operational issue.

Example:

"Our payment API is returning HTTP 500 errors after the latest
deployment."

The user should be able to provide this problem to OpsPilot and
receive a structured investigation.

---

## 4. Core Capabilities

OpsPilot will eventually support:

1. Incident analysis
2. Knowledge retrieval
3. Tool usage
4. Structured AI outputs
5. Evidence-based recommendations
6. Human approval for consequential actions
7. Conversation and investigation history
8. Evaluation of AI responses
9. Observability and logging

---

## 5. High-Level Architecture

```text
                         USER
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |     API     |
                    +------+------+
                           |
                           v
                  +------------------+
                  | Agent Orchestrator|
                  +--------+---------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        +---------+    +---------+   +---------+
        |   RAG   |    |  Tools  |   | Memory |
        +----+----+    +----+----+   +----+----+
             |              |              |
             v              v              v
        Documents       External       Database
        /Knowledge      Services
             |
             v
        Vector Store

                           |
                           v
                    +-------------+
                    | AI Model    |
                    +------+------+
                           |
                           v
                  Structured Result
                           |
                           v
                    Human Review