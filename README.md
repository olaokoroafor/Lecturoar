# Lecturoar

## Overview

Recording search thingomagy:

1. We upload video + transcript
2. (Ingestor): handle video upload + parse the transcript + ingest into db
3. (Backend proper): search transcripts and return useful info about where the results are
4. (Frontend): nice display with jumping to video, etc

Also need static files or something to get videos from.

## Division of labor

* Aapeli (@aapeliv): backend
* Ethan (@ethanzhang02): backend
* Ola (@olaokoroafor): frontend
* Patrick (@ptongx): frontend

## Stack

* database: postgres
* backend: python + sqlalchemy + flask
* frontend: react + video-react
* api: rest + json

## DB schema

* Courses table: `(id, name, description)`
* Videos table: `(id, course_id, url, duration?)`
* Transcriptions table: `(id, video_id, start_time, end_time, speaker_name, text)`

## API

### Search endpoint

`GET /api/search?query=...`
`GET /api/course/583/search?query=...`
`GET /api/course/583/video/952/search?query=...`

* Search everywhere
* Search within course
* Search within video

* Give freeform text, get ranked results

### Course info

`GET /api/course/583`

* Basically dumps course table + videos table

### Video info

`GET /api/course/583/video/952`

* Basically dumps video table

### Transcript retrieval

`GET /api/course/583/video/952/transcript`

* Get whole video transcript

## Screens

**Every page has a search bar that searches within that entity (e.g. everywhere, course, video, etc)**

### Welcome screen

* Extra big search bar (google style?)
* List of courses

### Search results screen

* List of results with highlighted bits and link to jump to that video at that time

### Courses screen

* List of videos + basic info

### Video screen

* Video
* Transcript
* Extra search bar to search within


## Result JSON

`GET /api/search?query=binary+heap`:

```json
{
  "query": "binary heap",
  "courses": [
    {
      "id": 583,
      "relevance": 5.3,
      "name": "Data structures and algorithms in Java",
      "description": "Some lecturer droning on about heaps and shit",
      "videos": [
        {
          "id": 952,
          "relevance": 2.1,
          "course_id": 583,
          "title": "Lecture 23",
          "hits": [
            {
              "relevance": 1.6,
              "start_time": 94,
              "end_time": 103,
              "speaker_name": "Paul",
              "transcript": "and now we're going to talk about fibonacci and binary heaps and other important stuff",
              "snippet": "...going to talk about fibonacci and **binary heaps** and..."
            },
            {
              "relevance": 1.21,
              "start_time": 143,
              "end_time": 160,
              "speaker_name": "Paul",
              "transcript": "so let's now look at how a binary heap actually works.",
              "snippet": "...look at how a **binary heap** actually works..."
            },
            {
              "relevance": 0.85,
              "start_time": 201,
              "end_time": 213,
              "speaker_name": "Ola",
              "transcript": "can you say binary heap one more time so we get more search results, please?",
              "snippet": "...you say **binary heap** one more time..."
            }
          ]
        },
        {
          "id": 955,
          "relevance": 2.1,
          "course_id": 583,
          "title": "Lecture 25",
          "hits": [
            {
              "relevance": 0.8,
              "start_time": 23,
              "end_time": 43,
              "speaker_name": "Paul",
              "transcript": "today we're going to go on some more about binary heaps and stuff",
              "snippet": "...more about **binary heaps** and stuff..."
            }
          ]
        }
      ]
    }
  ]
}
```

`GET /api/course/583/search?query=binary+heap`:

```json
{
  "courses": [
    {
      "id": 583,
      "name": "Data structures and algorithms in Java",
      "description": "Some lecturer droning on about heaps and shit",
      "videos": [
        {
          "id": 921,
          "course_id": 583,
          "title": "Lecture 1"
        },
        // ...
        {
          "id": 955,
          "course_id": 583,
          "title": "Lecture 25"
        }
      ]
    }
  ]
}
```

`GET /api/course/583/video/952`

```json
{
  "courses": [
    {
      "id": 583,
      "name": "Data structures and algorithms in Java",
      "description": "Some lecturer droning on about heaps and shit",
      "videos": [
        {
          "id": 952,
          "course_id": 583,
          "title": "Lecture 23",
          "video_url": "/videos/952.mp4",
          "transcript_url": "/api/course/583/video/952/transcript"
        }
      ]
    }
  ]
}
```

`GET /api/course/583/video/952/transcript`

```json
// ???
```
For Video Player stuff, need to install stuff using this line: npm install --save video-react react react-dom redux
