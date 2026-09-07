from sqlalchemy import create_engine, select
from sqlalchemy.orm import mapped_column, sessionmaker, DeclarativeBase, Mapped


engine = create_engine(url="sqlite:///requests.db")

session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class ChatRequests(Base):
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]


def get_user_requests(ip_address: str) -> list[ChatRequests]:
    with session() as new_session:
        query = select(ChatRequests).filter_by(ip_address=ip_address)
        result = new_session.execute(query)
        return result.scalars().all() # type: ignore


def add_requests_data(ip_address: str, promt: str, response: str) -> None:
    with session() as new_session:
        new_request = ChatRequests(
            ip_address=ip_address,
            prompt=promt,
            response=response,
        )
        new_session.add(new_request)
        new_session.commit()