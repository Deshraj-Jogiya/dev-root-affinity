# CurioSync Daily Publisher System Architecture

This note outlines the architectural design of **CurioSync**, an automated daily publisher system. It highlights the stateless deployment model utilizing GitHub Actions as a runner and an in-memory SQLite database, which eliminates hosting costs.

## System Block Diagram
```
[RSS News Sources] ---> [CurioSync Engine]
                             |
                             v
                  [Deduplication & Filter]
                             |
                             v
                 [Gemini LLM Fallback Chain]
                             |
                             v
                 [Pillow Visual Rendering]
                             |
                             v
                 [LinkedIn API Publishing]
```

## Core Stateless In-Memory Loader
To avoid hosting a persistent SQL server, the system loads environment secrets inside the GitHub runner, initializes an in-memory database schema, seeds the user record, and executes the entire publishing pipeline in-memory:

```python
import asyncio
from datetime import datetime, timedelta
from app.database import init_db, async_session
from app.models.user import User
from app.models.token import OAuthToken
from app.services.scheduler_service import run_daily_pipeline

async def run_stateless_job(access_token, sub_urn, fernet_key):
    # 1. Initialize tables in-memory (sqlite+aiosqlite:///:memory:)
    await init_db()
    
    # 2. Seed active OAuth credentials
    encrypted = OAuthToken.encrypt_token(access_token, fernet_key)
    async with async_session() as session:
        user = User(
            linkedin_sub=sub_urn.replace("urn:li:person:", ""),
            name="Cloud Runner Bot",
            email="actions@github.local"
        )
        session.add(user)
        await session.flush()
        
        token = OAuthToken(
            user_id=user.id,
            encrypted_access_token=encrypted,
            token_type="Bearer",
            expires_at=datetime.utcnow() + timedelta(days=60)
        )
        session.add(token)
        await session.commit()
        
        user_id = user.id

    # 3. Trigger publishing orchestration
    result = await run_daily_pipeline(user_id=user_id, run_type="github_actions_cron")
    return result
```

## Pillow Graphic Synthesis
The system uses the Pillow library to draw a horizontal slate-indigo gradient, maps the text metrics using system TrueType fonts, wraps the parsed bullets automatically, and draws a connectivity node graph representing the AI/ML framework.
- Canvas dimensions: 1200x628 pixels (LinkedIn's optimal post image card format).
- Design system: custom colors tailored to slate/dark themes matching modern UI designs.
