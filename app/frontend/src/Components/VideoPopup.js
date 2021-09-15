import React from "react";
import "./video.css"; // import css
import { Player } from "video-react";

const VideoPopup = (props) => {
  return (
    <div className="popup-box">
      <div className="box">
        <span className="close-icon" onClick={props.handleClose}>
          x
        </span>
        {props.content}
        <VideoPlayer start={props.startTime} />
      </div>
    </div>
  );
};

const VideoPlayer = (start) => {
  return (
    <Player
      playsInline
      poster="./video.jpg"
      src="https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4"
      startTime={start}
      autoplay
    />
  );
};

export default VideoPopup;
