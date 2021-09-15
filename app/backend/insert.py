"""
Stuff to insert data into the db
"""

from models import Course, TranscriptionChunk, Video, get_engine, meta, session_scope
from parsers import webvtt


def add_course(name, description):
    with session_scope() as session:
        course = Course(
            name=name,
            description=description,
        )
        session.add(course)
        session.flush()
        return course.course_id


def add_zoom_video(course_id, title, duration, video_url, transcript_path):
    with open(transcript_path, "r") as transcript_file:
        transcript_lines = webvtt.parse_zoom_vtt(transcript_file.read())

    with session_scope() as session:
        video = Video(
            course_id=course_id,
            title=title,
            duration=duration,
            video_url=video_url,
        )
        session.add(video)
        session.flush()

        for (start_time, end_time, speaker, text) in transcript_lines:
            session.add(
                TranscriptionChunk(
                    video_id=video.video_id,
                    start_time=start_time,
                    end_time=end_time,
                    speaker=speaker,
                    text=text,
                )
            )

        session.flush()

        return video.video_id
