import requests

# Transcript API
def get_transcript_content(meeting_ID, transcript_ID, token):
    endpoint = "https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting}/transcripts/{transcript}/content?$format=text/vtt".format(meeting = meeting_ID, transcript = transcript_ID)
    api_result = requests.get(
        endpoint,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).text
    return api_result

# Attendees API
def get_attendees_list(meeting_ID, report_ID, token):
    endpoint = "https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting}/attendanceReports/{report}/attendanceRecords".format(meeting = meeting_ID, report = report_ID)
    api_result = requests.get(
        endpoint,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()

    attendance_values = api_result["value"]
    email_list = []
    for attendee in attendance_values:
        if attendee["emailAddress"]:
            email_list.append(attendee["emailAddress"])
    return email_list