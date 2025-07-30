from sqlalchemy import select, delete, insert

from database.database import AsyncSession
from models.db.Keyphrase import UserKeyphrases


async def get_user_keyphrases(session: AsyncSession, user_id: int) -> UserKeyphrases:
    query = (
        select(UserKeyphrases)
        .where(UserKeyphrases.user_id == user_id)
    )
    
    result = (await session.execute(query)).scalars().one()
    
    return result


async def set_user_keyphrases(session: AsyncSession, user_id: int, keyphrases: list[str], normalized_keyphrases: list[str]):
    del_query = (
        delete(UserKeyphrases)
        .where(UserKeyphrases.user_id == user_id)
    )
    
    try:
        await session.execute(del_query)
    except Exception:
        pass
    
    user_keyphrases = UserKeyphrases(user_id=user_id, keyphrases=','.join(keyphrases), normalized_keyphrases=','.join(normalized_keyphrases))
    
    session.add(user_keyphrases)
    await session.commit()