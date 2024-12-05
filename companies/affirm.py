import json
import requests

from . import base


class Affirm(base.Company):

    NAME = "Affirm"
    LIST_URL = "https://boards-api.greenhouse.io/v1/boards/affirm/jobs/"
    JOB_DESC_URL = "https://job-boards.greenhouse.io/affirm/jobs/%s"
    LOCATION = "Remote US"
    CATEGORY = "Engineering"
    PAGE_SIZE = 20

    def get_headers(self):
        return {
            "accept": "application/json",
            "content-type": "application/json",
        }

    def get_data(self, offset=None):
        return {
            "appliedFacets": {
                "jobFamilyGroup": ["f4d09ae81507102da2509648ba482a8e"],
                "locations": [
                    "c9856d3fa53601f8de3201b8a0010cb4",
                    "f9d9c61ccfac105075aae3e09e9a7ea2",
                ],
            },
            "limit": self.PAGE_SIZE,
            "offset": offset or 0,
            "searchText": "",
        }

    def pull(self, include_all=False):
        if include_all:
            seen = set()
        else:
            seen = self.load_seen()

        self.logger.log(f"Starting {self.NAME}. (include_all={include_all})\n")
        self.logger.log(f"Seen: {seen}\n")

        new_jobs = []
        response = requests.get(
            self.LIST_URL, headers=self.get_headers()
        )
        response_json = json.loads(response.content)
        for item in response_json.get("jobs"):
            job_id = item.get("internal_job_id")
            location = item.get("location", {}).get("name")
            if any([
                item.get("metadata")[0].get('value') != self.CATEGORY,
                location != self.LOCATION
            ]):
                continue

            if str(job_id) not in seen:
                new_jobs.append(
                    {
                        "id": job_id,
                        "title": item.get("title"),
                        "href": item.get("absolute_url"),
                        "location": item.get("location", {}).get("name"),
                        "posted": item.get("updated_at"),
                    }
                )
                self.mark_seen(str(job_id))

        return new_jobs

    def summarize(self, job):
        return """<ul>
    <li>Id: {id}</li>
    <li>Title: {title}</li>
    <li>Location: {location}</li>
    <li>Posted: {posted}</li>
    <li>URL: <a clicktracking="off" href="{url}">{title}</a></li>
    </ul>""".format(
            id=job.get("id"),
            title=job.get("title").strip(),
            location=job.get("location"),
            posted=job.get("posted"),
            url=job.get("href"),
        )
