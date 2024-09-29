from session_backend import create_session, update_livestream, update_livestream_status

session_id, session_name = create_session()

if session_id:
    stream_url = "rtmp://162.243.166.134:1935/live_321"
    stream_key = "live_321"
    page_url = "http://localhost:3000/"
    update_livestream(session_id, stream_url, stream_key, page_url)
    update_livestream_status(session_id, stream_url, stream_key, page_url)