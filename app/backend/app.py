from flask import Flask, request, send_from_directory, url_for
from flask_cors import CORS
from sqlalchemy.sql import func

from models import Course, TranscriptionChunk, Video, get_engine, meta, session_scope

app = Flask(__name__)
CORS(app)
app.config["JSON_SORT_KEYS"] = False


def generate_error(code, message):
    return {"error": message}, code


@app.route("/")
def index():
    with session_scope() as session:
        return str(session.execute("SELECT 'test';"))
    return "Lecturoar"


def _search(
    query,
    filter_func=lambda query: query,
    next_rank=None,
    page_size=100,
    regconfig="english",
    tri_similarity_threshold=0.6,
):
    with session_scope() as session:
        # set up postgres search stuff
        text = func.coalesce(TranscriptionChunk.text, "")
        sim = func.word_similarity(func.unaccent(query), func.unaccent(text))
        rank = sim.label("rank")
        tsq = func.websearch_to_tsquery(regconfig, query)
        snippet = func.ts_headline(regconfig, text, tsq, "StartSel=<<<,StopSel=>>>").label("snippet")

        # run actual search
        results = (
            filter_func(
                session.query(TranscriptionChunk, Video, Course, rank, snippet)
                .join(Video, Video.video_id == TranscriptionChunk.video_id)
                .join(Course, Course.course_id == Video.course_id)
            )
            .filter(sim > tri_similarity_threshold)
            .filter(rank <= next_rank if next_rank is not None else True)
            .order_by(rank.desc())
            .limit(page_size + 1)
            .all()
        )

        # order results according to course, class, then by rank
        # this is a bit manual and annoying
        courses = {}
        videos = {}
        # ids in correct order (dicts aren't ordered)
        course_ordering = []
        video_ordering = []

        for chunk, video, course, rank, snippet in results:
            if course.course_id not in courses.keys():
                courses[course.course_id] = {
                    "course_id": course.course_id,
                    "name": course.name,
                    "description": course.description,
                    "videos": [],
                }
                course_ordering.append(course.course_id)

            if video.video_id not in videos.keys():
                videos[video.video_id] = {
                    "video_id": video.video_id,
                    "course_id": video.course_id,
                    "title": video.title,
                    "duration": video.duration,
                    "video_url": url_for("video", video_name=video.video_url),
                    "transcript_url": url_for("transcript", course_id=video.course_id, video_id=video.video_id),
                    "hits": [],
                }
                video_ordering.append(video.video_id)

            videos[video.video_id]["hits"].append(
                {
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "speaker": chunk.speaker,
                    "text": chunk.text,
                    "rank": rank,
                    "snippet": snippet,
                }
            )

        # stitch it all together...
        for video_id in video_ordering:
            courses[videos[video_id]["course_id"]]["videos"].append(videos[video_id])

        # ...and send away
        return {"query": query, "courses": [courses[course_id] for course_id in course_ordering]}


def _serialize_course_and_videos(course, videos):
    return {
        "courses": [
            {
                "course_id": course.course_id,
                "name": course.name,
                "description": course.description,
                "videos": [
                    {
                        "video_id": video.video_id,
                        "course_id": video.course_id,
                        "title": video.title,
                        "duration": video.duration,
                        "video_url": url_for("video", video_name=video.video_url),
                        "transcript_url": url_for("transcript", course_id=video.course_id, video_id=video.video_id),
                    }
                    for video in videos
                ],
            }
        ]
    }


@app.route("/api/search")
def search():
    query = request.args.get("query", "")
    if len(query) < 3:
        return generate_error(400, "Query too short, needs to be at least 3 characters")
    return _search(query)


@app.route("/api/course/<int:course_id>")
def course(course_id):
    with session_scope() as session:
        course = session.query(Course).filter(Course.course_id == course_id).one_or_none()
        if not course:
            return generate_error(404, "Course not found.")
        return _serialize_course_and_videos(course, course.videos)


@app.route("/api/course/<int:course_id>/search")
def search_course(course_id):
    query = request.args.get("query", "")
    if len(query) < 3:
        return generate_error(400, "Query too short, needs to be at least 3 characters")

    def filter_func(query):
        return query.filter(Video.course_id == course_id)

    return _search(query, filter_func)


@app.route("/api/course/<int:course_id>/video/<int:video_id>")
def course_video(course_id, video_id):
    with session_scope() as session:
        res = (
            session.query(Course, Video)
            .join(Course, Course.course_id == Video.course_id)
            .filter(Course.course_id == course_id)
            .filter(Video.video_id == video_id)
            .one_or_none()
        )
        if not res:
            return generate_error(404, "Video not found.")
        course, video = res
        return _serialize_course_and_videos(course, [video])


@app.route("/api/course/<int:course_id>/video/<int:video_id>/search")
def search_video(course_id, video_id):
    query = request.args.get("query", "")
    if len(query) < 3:
        return generate_error(400, "Query too short, needs to be at least 3 characters")

    def filter_func(query):
        return query.filter(Video.course_id == course_id).filter(Video.video_id == video_id)

    return _search(query, filter_func)


@app.route("/api/course/<int:course_id>/video/<int:video_id>/transcript")
def transcript(course_id, video_id):
    with session_scope() as session:
        video = (
            session.query(Video)
            .join(Course, Course.course_id == Video.course_id)
            .filter(Course.course_id == course_id)
            .filter(Video.video_id == video_id)
            .one_or_none()
        )
        if not video:
            return generate_error(404, "Video not found.")
        return {
            "video_id": video.video_id,
            "chunks": [
                {
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "speaker": chunk.speaker,
                    "text": chunk.text,
                }
                for chunk in video.transcription_chunks
            ],
        }


@app.route("/videos/<video_name>")
def video(video_name):
    try:
        return send_from_directory("content/", filename=video_name, conditional=True, mimetype="video/mp4")
    except FileNotFoundError:
        return generate_error(404, "Video not found.")


meta.create_all(get_engine())
