import functools
import os
from contextlib import contextmanager

from sqlalchemy import Column, Float, ForeignKey, Integer, MetaData, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.session import Session


@functools.cache
def get_engine():
    return create_engine(os.environ["DB_CONNECTION_STRING"])


@contextmanager
def session_scope():
    session = Session(get_engine())
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=meta)


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Video(Base):
    __tablename__ = "videos"

    video_id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey("courses.course_id"), nullable=False)

    title = Column(String, nullable=False)
    duration = Column(Float, nullable=False)  # in seconds

    video_url = Column(String, nullable=False)

    course = relationship("Course", backref="videos")


class TranscriptionChunk(Base):
    __tablename__ = "transcription_chunks"

    transcript_chunk_id = Column(Integer, primary_key=True)
    video_id = Column(ForeignKey("videos.video_id"), nullable=False)

    start_time = Column(Float, nullable=False)  # in seconds
    end_time = Column(Float, nullable=False)  # in seconds

    speaker = Column(String, nullable=True)
    text = Column(String, nullable=False)

    video = relationship("Video", backref="transcription_chunks", order_by="TranscriptionChunk.start_time.asc()")
