import React, { useState } from "react";
import { Link } from "react-router-dom";

const timeDisplay = (seconds) => {
  return new Date(seconds * 1000).toISOString().substr(11, 8);
};

const Video = ({ video }) => {
  return (
    <div class="card">
      <h3>{video["title"]}</h3>
      {video["hits"].map((hit) => (
        <div>
          <p>
            <Link
              to={`/course/${video["course_id"]}/video/${video["video_id"]}/watch?t=${hit["start_time"]}`}
            >
              {hit["speaker"]} at {timeDisplay(hit["start_time"])}:
            </Link>{" "}
            <span
              dangerouslySetInnerHTML={{
                __html: ("..." + hit["snippet"] + "...")
                  .replace("<<<", "<b>")
                  .replace(">>>", "</b>"),
              }}
            />
          </p>
        </div>
      ))}
    </div>
  );
};

const SearchItem = ({ name, videos }) => {
  function makeVideos(items) {
    const elements = items.map((item) => <Video video={item} />);
    return elements;
  }

  return (
    <div>
      <h4>{name}</h4>
      <br></br>
      {makeVideos(videos)}
    </div>
  );
};

export default SearchItem;
