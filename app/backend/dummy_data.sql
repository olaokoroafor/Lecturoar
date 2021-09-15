insert into courses(name, description) values ('Test course', 'This is just a test course for lecturoar');
insert into courses(name, description) values ('Test course 2', 'Another test course for lecturoar');

insert into videos(course_id, title, duration, video_url, transcript_url) values
(1,'Lecture 1',95,'/videos/1.mp4','/transcripts/1.json'),
(1,'Lecture 2',110,'/videos/2.mp4','/transcripts/2.json'),
(1,'Lecture 3',80,'/videos/3.mp4','/transcripts/3.json'),
(1,'Lecture 4',70,'/videos/4.mp4','/transcripts/4.json'),
(2,'Recording 1',66,'/videos/5.mp4','/transcripts/5.json'),
(2,'Recording 2',68,'/videos/6.mp4','/transcripts/6.json'),
(2,'Recording 3',54,'/videos/7.mp4','/transcripts/7.json');
