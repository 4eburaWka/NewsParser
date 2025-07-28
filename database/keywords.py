from sqlalchemy import select, delete, insert

from database.database import AsyncSession
from models.db.Keyword import UserKeywords


async def get_user_keywords(session: AsyncSession, user_id: int) -> UserKeywords:
    query = (
        select(UserKeywords)
        .where(UserKeywords.user_id == user_id)
    )
    
    result = (await session.execute(query)).scalars().one()
    
    return result


async def set_user_keywords(session: AsyncSession, user_id: int, keywords: list[str], normalized_keywords: list[str]):
    del_query = (
        delete(UserKeywords)
        .where(UserKeywords.user_id == user_id)
    )
    
    try:
        await session.execute(del_query)
    except Exception:
        pass
    
    user_keywords = UserKeywords(user_id=user_id, keywords=','.join(keywords), normalized_keywords=','.join(normalized_keywords))
    
    session.add(user_keywords)
    await session.commit()