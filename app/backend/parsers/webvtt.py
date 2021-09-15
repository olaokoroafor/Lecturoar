from io import StringIO

import webvtt


def parse_zoom_vtt_line(line):
    try:
        speaker, text = line.text.split(": ", 1)
    except Exception as e:
        speaker, text = None, line.text
    return (line.start_in_seconds, line.end_in_seconds, speaker, text)


def parse_zoom_vtt(data):
    """
    Parses a zoom webvtt file, returning a list of tuples of the form

    (start_time, end_time, speaker, text)

    Times in doubles
    """
    buffer = StringIO(data)
    return list(map(parse_zoom_vtt_line, webvtt.read_buffer(buffer)))
